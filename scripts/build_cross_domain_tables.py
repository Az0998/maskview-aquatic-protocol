"""Synthesize frozen lake + ocean Mask-View tables (standalone repo)."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(ROOT))
from config import FIGURES, LAKE, OCEAN, TABLES

SHARED = ["point", "block_time", "sensor", "station", "mixed"]


def df_md(df: pd.DataFrame) -> str:
    cols = list(df.columns)
    lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join("---" for _ in cols) + " |"]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[c]) for c in cols) + " |")
    return "\n".join(lines)


def lake_winners() -> pd.DataFrame:
    mae = pd.read_csv(LAKE / "table_mae_by_pattern_avg.csv", index_col=0)
    abl = pd.read_csv(LAKE / "ablation_mae_by_pattern.csv", index_col=0)
    rows = []
    for pat in SHARED:
        col = mae[pat]
        simple = float(col.loc["Linear"])
        learned = float(col.loc["MaskView-ST"])
        recipe = float(abl.loc["spatial_plus_l0", pat]) if "spatial_plus_l0" in abl.index else learned
        brits = float(col.loc["BRITS"])
        winner = col.idxmin()
        rows.append(
            {
                "pattern": pat,
                "medium": "lake_dianchi",
                "metric": "std_MAE",
                "simple_Linear": round(simple, 4),
                "learned_MaskViewST": round(learned, 4),
                "recipe_spatial_plus_l0": round(recipe, 4),
                "BRITS": round(brits, 4),
                "winner_default_grid": winner,
                "learned_beats_Linear": learned < simple,
                "recipe_beats_Linear": recipe < simple,
            }
        )
    return pd.DataFrame(rows)


def ocean_winners() -> pd.DataFrame:
    raw = json.loads((OCEAN / "maskview_ablation.json").read_text(encoding="utf-8"))
    dense = next(r for r in raw if r["sparse"] == "none")
    dense_rmse = float(dense["lead1_st_rmse"])
    fair_path = OCEAN / "fair_sparse_baselines.csv"
    fair = pd.read_csv(fair_path) if fair_path.exists() else None
    rows = []
    for r in raw:
        pat = r["sparse"]
        st = float(r["lead1_st_rmse"])
        deg = (st - dense_rmse) / dense_rmse
        locf = clim = spatial = keep = None
        if fair is not None:
            sub = fair[(fair.pattern == pat) & (fair.lead == 1)]
            if not sub.empty:
                keep = float(sub.keep_frac.iloc[0])
                if (sub.model == "persist_locf").any():
                    locf = float(sub.loc[sub.model == "persist_locf", "RMSE"].iloc[0])
                if (sub.model == "climatology").any():
                    clim = float(sub.loc[sub.model == "climatology", "RMSE"].iloc[0])
                if (sub.model == "spatial_linear").any():
                    spatial = float(sub.loc[sub.model == "spatial_linear", "RMSE"].iloc[0])
        rows.append(
            {
                "pattern": pat,
                "medium": "ocean_ecs",
                "metric": "lead1_RMSE_umolkg",
                "keep_frac": round(keep, 3) if keep is not None else "",
                "persist_locf": locf,
                "spatial_linear": spatial,
                "clim_RMSE": clim,
                "ST_RMSE": round(st, 3),
                "lead1_best": r["lead1_best"],
                "lead2_best": r["lead2_best"],
                "lead1_F1": round(float(r["lead1_st_f1"]), 3),
                "degradation_vs_dense": round(deg, 3),
                "st_margin_vs_clim": round(clim - st, 3) if clim is not None else "",
                "lead2_falls_to_climatology": r["lead2_best"] == "climatology",
            }
        )
    return pd.DataFrame(rows)


def rank_reversal(lake: pd.DataFrame, ocean: pd.DataFrame) -> pd.DataFrame:
    o = ocean.set_index("pattern")
    simple = None
    simple_path = OCEAN / "ocean_simple_vs_learned.csv"
    if simple_path.exists():
        simple = pd.read_csv(simple_path)
        s1 = simple[(simple["lead"] == 1)]
    rows = []
    for _, r in lake.iterrows():
        pat = r["pattern"]
        if pat not in o.index:
            continue
        oc = o.loc[pat]
        persist = clim = st = locf = None
        if simple is not None:
            sub = s1[s1["pattern"] == pat]
            if not sub.empty:
                persist = float(sub.loc[sub.model == "persistence", "RMSE"].iloc[0]) if (sub.model == "persistence").any() else None
                clim = float(sub.loc[sub.model == "climatology", "RMSE"].iloc[0]) if (sub.model == "climatology").any() else None
                st = float(sub.loc[sub.model == "st_transformer", "RMSE"].iloc[0]) if (sub.model == "st_transformer").any() else None
        fair_path = OCEAN / "fair_sparse_baselines.csv"
        if fair_path.exists():
            f = pd.read_csv(fair_path)
            f1 = f[(f.lead == 1) & (f.pattern == pat)]
            if not f1.empty and (f1.model == "persist_locf").any():
                locf = float(f1.loc[f1.model == "persist_locf", "RMSE"].iloc[0])
        rows.append(
            {
                "pattern": pat,
                "lake_winner": r["winner_default_grid"],
                "lake_recipe_beats_Linear": bool(r["recipe_beats_Linear"]),
                "ocean_lead1_best": oc["lead1_best"],
                "ocean_lead2_best": oc["lead2_best"],
                "ocean_lead1_degradation": oc["degradation_vs_dense"],
                "ocean_persist_unmasked_RMSE": persist,
                "ocean_persist_locf_RMSE": locf,
                "ocean_clim_RMSE": clim,
                "ocean_ST_RMSE": st,
                "ocean_ST_beats_clim": (st is not None and clim is not None and st < clim),
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    TABLES.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    lake = lake_winners()
    ocean = ocean_winners()
    rr = rank_reversal(lake, ocean)
    lake.to_csv(TABLES / "lake_pattern_winners.csv", index=False)
    ocean.to_csv(TABLES / "ocean_pattern_winners.csv", index=False)
    rr.to_csv(TABLES / "rank_reversal_shared_patterns.csv", index=False)

    wins = json.loads((LAKE / "paper_tables_summary.json").read_text(encoding="utf-8"))
    abl = json.loads((LAKE / "ablation_summary.json").read_text(encoding="utf-8"))
    summary = {
        "standalone": True,
        "claim": "ranking is protocol-dependent across two aquatic media",
        "lake_setting_wins": wins.get("wins"),
        "lake_overall_MAE": wins.get("mean_mae_by_model"),
        "spatial_plus_l0_overall_MAE": abl.get("overall_mae", {}).get("spatial_plus_l0"),
        "shared_patterns": SHARED,
        "ocean_dense_lead1_ST_RMSE": float(ocean.loc[ocean.pattern == "none", "ST_RMSE"].iloc[0]),
        "ocean_argo_lead1_ST_RMSE": float(ocean.loc[ocean.pattern == "argo", "ST_RMSE"].iloc[0]),
        "data": "data/frozen (no sibling checkout required)",
    }
    (TABLES / "protocol_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    parts = [
        "# Cross-domain Mask-View rank reversal",
        "",
        "This repository is standalone. Numbers come from `data/frozen/`.",
        "",
        "## Lake (standardized MAE)",
        df_md(lake),
        "",
        "## Ocean (lead-1 RMSE µmol kg⁻¹)",
        df_md(ocean),
        "",
        "## Shared patterns",
        df_md(rr),
        "",
        "Do not compare MAE to µmol kg⁻¹. Compare **who wins**.",
        "Ocean `persist_unmasked` ignores the mask; use `persist_locf` as the fair persistence analog.",
        "",
        "## Dual protocol vs EcoInf 2025",
        "",
    ]
    eco = LAKE / "ecoinf_dual_protocol.md"
    if eco.exists():
        parts.append(eco.read_text(encoding="utf-8"))
    else:
        parts.append("_ecoinf_dual_protocol.md not frozen yet._")
    nat = LAKE / "natural_missing_replay.md"
    parts += ["", "## Natural missingness"]
    if nat.exists():
        parts.append(nat.read_text(encoding="utf-8"))
    (TABLES / "CROSS_DOMAIN.md").write_text("\n".join(parts), encoding="utf-8")
    print("Wrote", TABLES)


if __name__ == "__main__":
    main()

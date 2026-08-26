"""Self-contained paths. Clone-and-run; no sibling repos required."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FROZEN = ROOT / "data" / "frozen"
LAKE = FROZEN / "lake"
OCEAN = FROZEN / "ocean"
RESULTS = ROOT / "results"
TABLES = RESULTS / "tables"
FIGURES = RESULTS / "figures"

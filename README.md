# Mask-View：湖泊水质插值可行性证书

**个人兴趣自学项目 · 无导师指导 · EMS 审稿中（尚未录用）**

作者：张森捷（Senjie Zhang），兰州大学 · `3079099853@qq.com`  
仓库：https://github.com/Az0998/maskview-aquatic-protocol

## 这个项目在做什么

自动水质站的缺失往往是**整段宕机、整路传感器失效、整站掉线**，不是随机挖洞。很多插补论文却只在「随机缺失 / 周尺度缺口」上评模型，于是线性插值看起来很好——但那恰恰不是业务上最常见的失败模式。

本仓库提出一个**只依赖缺失掩码**的插值可行性证书 **ρ**：

- 若被遮住的格点，在评估窗内同一站–同一指标仍有观测邻居，则视为可插值；
- **ρ ≥ 0.5** 时，滇池 15 组 Mask-View 情景上，线性插值正好是重建赢家（15/15）；
- 传感器 / 整站失效时 **ρ = 0**，此时若仍按「随机缺失表」去部署线性插值，**低氧与总氮预警 CSI 可降到 0**；深度插补（如 BRITS）能把 TN 预警 CSI 拉回约 0.72–0.74。

贡献不在「再发明一个插补网络」，而在：**先算 ρ，再决定能不能用线性插值；并用下游预警，而不是只比重建 MAE。**

## 推荐阅读（写得最完整的文稿）

| 材料 | 说明 | 链接 |
|------|------|------|
| **英文手稿（在线可读）** | 与投稿稿同叙事的 Markdown 全文 | [paper/manuscript_draft.md](./paper/manuscript_draft.md) |
| **EMS 投稿 Word** | *Environmental Modelling & Software* 投稿版 | [paper/EMS_interpolability_certificate_manuscript.docx](./paper/EMS_interpolability_certificate_manuscript.docx) |
| **Cover letter** | 一页讲清贡献 | [paper/cover_letter_ems.txt](./paper/cover_letter_ems.txt) |
| **Highlights** | 5 条要点 | [paper/highlights.txt](./paper/highlights.txt) |
| **图形摘要** | 投稿用 GA | [paper/figures/graphical_abstract.png](./paper/figures/graphical_abstract.png) |
| **冻结证据表** | ρ / 预警 CSI / 海洋部署规则 | [`data/frozen/`](./data/frozen/) |

> 说明：仓库里若还有 `JHI_*` / `ECOINF_*` Word，属于早期叙事存档，**请以 EMS 稿与 `manuscript_draft.md` 为准**。

## 核心结果（冻结表）

1. **ρ 与线性赢家一致**：15/15 Mask-View 情景；Wu et al. (2025) 随机/周缺口库 ρ ≥ 0.998，故线性插值全胜——符合「可插值库」。
2. **预警翻转**：sensor / station 下线性插值预警 CSI = 0；BRITS 恢复 TN CSI ≥ 0.72；point 缺失下线性插值 DO 预警仍可优于 BRITS。
3. **东海陆架氧（姊妹实验）**：lead-1 倾向 Transformer；lead-2 缺氧 F1 多数情形倾向气候态（block-time 除外）。

## 姊妹项目（同一兴趣线）

| 仓库 | 一句话 |
|------|--------|
| [forecast-information-value](https://github.com/Az0998/forecast-information-value) | 嵌套站网：上游站/降水对流量预报还有没有信息价值（曾投 HSJ，后改 HESS 叙事） |
| [ocean-do-forecast](https://github.com/Az0998/ocean-do-forecast) | 东海溶解氧 1–3 个月预见期预报 + 稀疏观测压力测试 |
| [hydro-ml-paper](https://github.com/Az0998/hydro-ml-paper) | 多预见期流量预报早期实验仓 |

## 快速复现

```bash
git clone https://github.com/Az0998/maskview-aquatic-protocol.git
cd maskview-aquatic-protocol
pip install -r requirements.txt
python scripts/build_cross_domain_tables.py
python scripts/plot_pattern_bank.py
python scripts/plot_rank_reversal.py
python scripts/plot_keep_ratio_tax.py
python scripts/plot_graphical_abstract.py
python scripts/build_ems_docx.py
```

目录：`data/frozen/` 冻结结果 · `scripts/` 出表出图 · `paper/` 投稿包 · `results/` 生成物。

训练引擎若需重跑，见实验仓 `water-ai-do-forecast` / `ocean-do-forecast`；本仓是**论文开放合成与冻结证据**。

## License

MIT

---

# Mask-View interpolability certificate (English)

Standalone open synthesis for the EMS manuscript. Frozen tables live in `data/frozen/`.

**Author:** Senjie Zhang, Lanzhou University (`3079099853@qq.com`)  
**Best entry points:** [`paper/manuscript_draft.md`](./paper/manuscript_draft.md) · [`paper/EMS_interpolability_certificate_manuscript.docx`](./paper/EMS_interpolability_certificate_manuscript.docx)

A mask-only interpolability certificate ρ states when linear interpolation is admissible. Deploying Linear because an MCAR or week-gap table said so changes DO-drop and TN-exceedance warning CSI when a sensor or station is dark.

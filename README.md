<div align="center">

# AT82.03 — Stock Trend Predictor (NVDA, Next‑Hour)

Predict **NVDA’s next‑hour direction (UP/DOWN)** from an hourly, multi‑source dataset  
(price, technicals, market context, sentiment, insiders).

<!-- HERO: only ONE clean image row -->
<p>
  <img src="Documents/dashboard.png.jpg" alt="Forecasting dashboard" width="78%">
</p>

</div>

---

## Results (from report)
| Item | Value |
|---|---:|
| Horizon | 1 hour |
| Best validation accuracy | **0.569** (Random Forest) |
| Deployment model | **LightGBM** |
| Model size | **0.3–0.6 MB** |
| Inference latency | **5–15 ms** |
| Best lookback window | **16 hours** |

---

## What matters (quick insights)
- **Price + technical indicators** are the strongest hourly signals  
- **Market context** adds small but measurable gains  
- **Sentiment / insider features** were negligible at the 1‑hour horizon (in this setup)

---

## Data preparation (why we clean the spikes)
Hourly OHLC can contain **extreme wicks/spikes** that distort volatility‑sensitive features.  
We correct these outliers before building features.

<img src="Documents/outlier_fix.png" alt="Extreme wick correction (before/after)" width="300">
<img src="Documents/spikes.png" alt="Extreme wick correction (before/after)" width="700">

---

## Pipeline (how data becomes an hourly dataset)
All sources are aligned onto a single **NVDA‑centric hourly timeline** (timezone normalization + aggregation).

<img src="Documents/pipeline.png" alt="Dataset preparation pipeline" width="900">

---

## Experiments (ablation results)
We measure the marginal value of each feature group using a stepwise ablation design.

<img src="Documents/accuracy_by_group.png" alt="Validation accuracy by feature group" width="900">

---

## Setup (dev)

### Requirements
- Python 3.10+
- `uv`
- TA‑Lib (system library)

```bash
uv --version
python -c "import talib; print('TA-Lib OK')"
uv sync
```

---

## Run
```bash
uv run python src/app.py
```

or notebooks:
```bash
uv run jupyter lab
```

---

## License
AIT coursework — **AT82.03 Machine Learning** (educational/portfolio use).

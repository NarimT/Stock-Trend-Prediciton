<div align="center">

# AT82.03 — Stock Trend Predictor (NVDA, Next-Hour)

A practical ML pipeline to predict **NVDA’s next-hour direction (UP/DOWN)** using **time-aligned multi-source signals**  
(price action, market context, technical indicators, sentiment, and insider activity).

<!-- Badges (optional) -->
<!--
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](#)
[![uv](https://img.shields.io/badge/uv-enabled-111827?style=flat-square&logo=python&logoColor=white)](#)
-->

</div>

---

## ✨ Highlights

- **Target:** next-hour price direction classification (**UP/DOWN**) for NVDA
- **Robust preprocessing:** outlier correction (extreme wick cleanup) + strict timezone alignment
- **Experiments:** stepwise ablation across feature groups (baseline → market context → technical/sentiment/insiders → final)
- **Deployment-ready model:** lightweight + low-latency tree model (e.g., LightGBM) for real-time inference

---

## 🧭 Project Snapshot (add your final numbers here)

> Replace the placeholders after you finalize results.

| Item | Value |
|------|------:|
| Prediction horizon | 1 hour |
| Best validation accuracy | **TBD** |
| Best test accuracy | **TBD** |
| Best model | **TBD** (e.g., LightGBM) |
| Best lookback window | **TBD** (e.g., 16 hours) |

---

## 🧱 Method Overview

### 1) Preprocessing & Alignment
All sources are mapped onto a unified **NVDA-centric hourly timeline**:
- Fix extreme candles / spikes (MAD-based correction)
- Convert and align timezones (ET / UTC / etc.)
- Aggregate sources to the hourly granularity

> Add your pipeline figure here:
- `docs/images/pipeline.png` (recommended)

### 2) Feature Groups
The project evaluates multiple feature groups:
- **Price features (OHLCV)**: lagged close/volume, returns, etc.
- **Market context**: related tickers / indices / macro proxies
- **Technical indicators**: EMA, RSI, MACD, Bollinger Bands, Stochastic
- **Sentiment**: aggregated hourly sentiment scores
- **Insider activity**: engineered signals from disclosures

### 3) Stepwise Experiments (Ablation)
We measure incremental value by adding feature groups gradually:
1. **Experiment 1:** price-only baseline  
2. **Experiment 2:** + market context  
3. **Experiment 3:** + (technical / sentiment / insiders)  
4. **Experiment 4:** handpicked best mix from earlier stages

---

## 📂 Repository Structure

> Update to match your repo exactly (keep it short and accurate).

```text
src/                 # application / utilities
notebooks/           # research notebooks by phase
Documents/           # project reports / presentations (optional)
Dockerfile           # container build
pyproject.toml       # project metadata + dependencies
uv.lock              # reproducible dependency lockfile
```

---

## ✅ Setup (Development)

### 0) Prerequisites
- **Python**: 3.10+ recommended  
- **uv**: dependency manager  
- **TA‑Lib**: required system library for technical indicators

---

### 1) Install `uv`
Official docs: https://docs.astral.sh/uv/

Verify:
```bash
uv --version
```

---

### 2) Install TA‑Lib (system dependency)
TA‑Lib is a native (C/C++) dependency. The Python package will fail without it.

Install instructions: https://ta-lib.org/install/

- **macOS:** follow the macOS section
- **Windows:** download the installer and install normally
- **Linux:** build/install using your package manager or source build

Quick sanity check after installing dependencies:
```bash
python -c "import talib; print('TA-Lib OK')"
```

---

### 3) Create the environment
```bash
uv sync
```

---

## ▶️ Run

> Fill in the correct command for your app (choose one and delete the rest).

### Option A — Run the app entry point
```bash
uv run python src/app.py
```

### Option B — Run notebooks
```bash
uv run jupyter lab
```

### Option C — Docker
```bash
docker build -t stock-trend-predictor .
docker run --rm -p 8501:8501 stock-trend-predictor
```

---

## 📊 Results (add your figures here)

Create a folder like `docs/images/` and drop images there, then reference them:

- Pre/post outlier fix  
- Dataset preparation pipeline  
- Accuracy by feature group / window size  
- Deployment comparison table  
- UI dashboard screenshots  

Example template:

```text
docs/images/
  outlier_fix.png
  pipeline.png
  accuracy_by_group.png
  window_size.png
  deployment_table.png
  dashboard.png
```

Then embed:

```markdown
![Preprocessing: extreme wick cleanup](docs/images/outlier_fix.png)
![Dataset preparation pipeline](docs/images/pipeline.png)
![Validation accuracy by feature group](docs/images/accuracy_by_group.png)
![Window size analysis](docs/images/window_size.png)
![Dashboard](docs/images/dashboard.png)
```

---

## ⚠️ Notes & Reproducibility

- Use **chronological splits** (walk-forward / time-based validation) to reduce leakage.
- Ensure **all features are computed using only past information** relative to the prediction timestamp.
- For any external APIs (news/sentiment), document rate limits and caching strategy.

---

## 🗺️ Roadmap (optional)

- [ ] Add a single command to reproduce the full pipeline (download → preprocess → train → evaluate)
- [ ] Add a minimal sample dataset for quick tests
- [ ] Add backtesting metrics (PnL with costs, drawdown)
- [ ] Add CI to run lint + unit tests

---

## 📄 License
Choose one:
- MIT / Apache-2.0 / GPL-3.0, etc. (add a `LICENSE` file)

---

## 🙌 Acknowledgements
- TA‑Lib: https://ta-lib.org/
- Any data sources you used (Alpha Vantage, etc.)


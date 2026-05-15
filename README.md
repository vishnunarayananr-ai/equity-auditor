# 📊 Equity Auditor
### Real-Time Intelligence · RAG · Multi-Agent · Financial Modelling

> A near-production HNI Investment Intelligence Platform that combines live market data, technical indicators, NLP sentiment analysis, RAG pipelines, and ML-based financial modelling into a single Streamlit dashboard.

**Built by:** Vishnu Narayanan R  
**Assessor:**  Prasad Jay — Veltech Solutions  
**Stack:** Python · Streamlit · yfinance · scikit-learn · Plotly · SentenceTransformers

---

## 🚀 Features

| Feature | Description |
|---|---|
| 🏥 Company Health Audit | Overall health score (%) with Score Breakdown, Pros & Cons |
| 📈 Price Chart | Live candlestick chart with volume |
| 📉 Technical Indicators | RSI(14), MACD with signal line, Bollinger Bands |
| 🧠 RAG Strategic Briefing | Semantic search across Financial Health, Revenue & Growth, Risk Assessment, Future Outlook |
| 📰 News Sentiment Analysis | NLP-based sentiment scoring — Positive, Negative, Neutral headlines |
| 📊 Analyst Ratings | Strong Buy / Buy / Hold / Sell / Strong Sell breakdown |
| 🔍 Market Screener | 4-tier market cap ranking (Mag 7, >$500B, $100B–$500B, <$100B) |
| 🔁 Backtesting | MA Crossover vs Buy & Hold with verdict |
| 📉 Linear Regression | Trend direction + 10-day price prediction + R² score |
| ⚠️ Stress Test | Crash scenario analysis (Mild -10% → Extreme -50%) |
| 🔵 Outlier Detection | Unusual price movements, max single day drop/gain |
| 🤖 Multi-Agent System | 4 agents running in clean separation |

---

## 🖥️ Screenshots

### 🏥 Company Health Audit — Key Metrics & Health Score
![Company Health Audit](https://github.com/vishnunarayananr-ai/equity-auditor/raw/main/Outputs/Compnay_audit_health1_1.jpg)

### 📊 Health Score Gauge & Pros/Cons Analysis
![Health Score Gauge](https://github.com/vishnunarayananr-ai/equity-auditor/raw/main/Outputs/Compnay_audit_health1_2.jpg)

### 🧠 AI Strategic Briefing — RAG & News Sentiment
![RAG Briefing](https://github.com/vishnunarayananr-ai/equity-auditor/raw/main/Outputs/Compnay_audit_health1_3.jpg)

### 📈 Price Chart & Technical Indicators Overview
![Price and Technical](https://github.com/vishnunarayananr-ai/equity-auditor/raw/main/Outputs/Compnay_audit_health1_4.jpg)

### 📈 AAPL — Price & Volume Chart
![Price Chart](https://github.com/vishnunarayananr-ai/equity-auditor/raw/main/Outputs/Charts/Price_chart_AAPL.png)

### 📉 RSI (14) — Overbought/Oversold
![RSI](https://github.com/vishnunarayananr-ai/equity-auditor/raw/main/Outputs/Charts/Technical_Indicators_1_1.png)

### 📉 MACD — Signal Line & Histogram
![MACD](https://github.com/vishnunarayananr-ai/equity-auditor/raw/main/Outputs/Charts/Technical_Indicators_1_2.png)

### 📉 Bollinger Bands
![Bollinger Bands](https://github.com/vishnunarayananr-ai/equity-auditor/raw/main/Outputs/Charts/Technical_Indicators_1_3.png)

### 🔁 Backtesting — MA Strategy vs Buy & Hold
![Backtest Chart](https://github.com/vishnunarayananr-ai/equity-auditor/raw/main/Outputs/Charts/BACKTESTING___MA_CROSSOVER_STRATEGY1_1.png)

### ⚠️ Stress Test — Crash Scenarios
![Stress Test](https://github.com/vishnunarayananr-ai/equity-auditor/raw/main/Outputs/Charts/BACKTESTING___MA_CROSSOVER_STRATEGY1_2.png)

### 🔍 Market Screener — Magnificent Seven
![Screener Mag7](https://github.com/vishnunarayananr-ai/equity-auditor/raw/main/Outputs/Market_Screener1_1.jpg)

### 🔍 Market Screener — $100B–$500B & Under $100B
![Screener Tiers](https://github.com/vishnunarayananr-ai/equity-auditor/raw/main/Outputs/Market_Screener1_2.jpg)

### 🔍 Market Screener — All Tiers
![Screener All](https://github.com/vishnunarayananr-ai/equity-auditor/raw/main/Outputs/Market_Screener1_3.jpg)

### 🔁 Backtest & Stress Test Overview
![Backtest Overview](https://github.com/vishnunarayananr-ai/equity-auditor/raw/main/Outputs/Backtest_Stress_test1_1.jpg)

### ⚠️ Outlier Detection
![Outlier Detection](https://github.com/vishnunarayananr-ai/equity-auditor/raw/main/Outputs/Backtest_Stress_test1_2.jpg)

---

## 🏗️ Project Structure

```
equity_auditor/
│
├── main.py                        ← Entry point — Streamlit app (3 tabs)
├── requirements.txt               ← All dependencies
│
├── agents/
│   ├── data_agent.py              ← Live + historical stock data (yfinance)
│   ├── news_agent.py              ← News scraper (Google News + RSS)
│   ├── rag_agent.py               ← RAG pipeline & semantic search
│   └── sentiment_agent.py         ← Sentiment scoring (TextBlob + NLP)
│
├── modules/
│   ├── indicators.py              ← RSI, MACD, Bollinger Bands
│   ├── health_score.py            ← Company health % + Pros & Cons
│   ├── screener.py                ← 4-tier market cap screener
│   └── financial_model.py         ← Linear regression, backtesting, stress test, outlier detection
│
├── ui/
│   ├── charts.py                  ← All Plotly chart functions
│   └── components.py              ← Reusable Streamlit UI components
│
├── utils/
│   └── helpers.py                 ← Shared utility functions
│
└── Outputs/
    ├── Charts/                    ← Exported chart images
    │   ├── Price_chart_AAPL.png
    │   ├── Technical_Indicators_1_1.png
    │   ├── Technical_Indicators_1_2.png
    │   ├── Technical_Indicators_1_3.png
    │   ├── BACKTESTING___MA_CROSSOVER_STRATEGY1_1.png
    │   └── BACKTESTING___MA_CROSSOVER_STRATEGY1_2.png
    ├── Compnay_audit_health1_1.jpg
    ├── Compnay_audit_health1_2.jpg
    ├── Compnay_audit_health1_3.jpg
    ├── Compnay_audit_health1_4.jpg
    ├── Market_Screener1_1.jpg
    ├── Market_Screener1_2.jpg
    ├── Market_Screener1_3.jpg
    ├── Backtest_Stress_test1_1.jpg
    └── Backtest_Stress_test1_2.jpg
```

---

## 🤖 Multi-Agent Architecture

```
┌──────────────────────────────────────────────┐
│                 main.py (UI)                 │
│   Tab 1: Health Audit | Tab 2: Screener      │
│   Tab 3: Backtest & Stress Test              │
└───────────────────┬──────────────────────────┘
                    │
       ┌────────────┼─────────────┐
       │            │             │
┌──────▼──┐  ┌──────▼──┐  ┌──────▼──┐  ┌──────────┐
│  Data   │  │  News   │  │Sentiment│  │   RAG    │
│  Agent  │  │  Agent  │  │  Agent  │  │  Agent   │
└─────────┘  └─────────┘  └─────────┘  └──────────┘
       │            │             │           │
       └────────────┴─────────────┴───────────┘
                    │
       ┌────────────┼─────────────┐
       │            │             │
┌──────▼──┐  ┌──────▼──┐  ┌──────▼──────────┐
│Indicator│  │ Health  │  │ Financial Model  │
│ Module  │  │  Score  │  │ (ML/Backtest)    │
└─────────┘  └─────────┘  └─────────────────┘
```

**Active Agents:**
- `DataAgent` — market data
- `NewsAgent` — scraper
- `SentimentAgent` — NLP
- `RAGAgent` — embeddings

**Active Modules:**
- `IndicatorModule` — RSI/MACD
- `HealthScoreModule` — scoring
- `ScreenerModule` — screener
- `FinancialModel` — ML/backtest

---

## 🛠️ Technology Stack

| Technology | Purpose | Why Chosen |
|---|---|---|
| Python 3.14 | Core language | Industry standard |
| Streamlit | Web dashboard UI | Fast, no HTML needed |
| yfinance | Stock & financial data | Free, reliable API |
| pandas | Data manipulation | Industry standard |
| numpy | Numerical computing | Fast array operations |
| ta | Technical indicators | RSI, MACD built-in |
| plotly | Interactive charts | Better than matplotlib |
| sentence-transformers | RAG embeddings | State-of-art NLP model |
| scikit-learn | ML models, outlier detection | Industry standard |
| scipy | Statistical analysis | Advanced math functions |
| textblob | Sentiment analysis | Simple, effective NLP |
| beautifulsoup4 | News scraping | Reliable HTML parser |
| requests | HTTP calls | Standard Python library |

---

## ⚙️ How to Run

**1. Clone the repo:**
```bash
git clone https://github.com/vishnunarayananr-ai/equity-auditor.git
cd equity-auditor
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

**3. Run the app:**
```bash
streamlit run main.py
```

**4. Open in browser:** `http://localhost:8501`

**5. Enter any ticker** (e.g. `AAPL`, `NVDA`, `TSLA`) → click **RUN FULL AUDIT**

---

## 📋 Assignment Coverage

| Requirement | Covered By |
|---|---|
| Data pipeline (live + historical) | `agents/data_agent.py` |
| Data preprocessing | `agents/data_agent.py` + `utils/helpers.py` |
| Outlier detection | `modules/financial_model.py` |
| Financial modelling (ML/Stat) | `modules/financial_model.py` |
| RSI, MACD, Volatility, KPIs | `modules/indicators.py` |
| Industry comparison | `modules/screener.py` |
| Macroeconomic impact | `agents/data_agent.py` |
| Management quality (analyst ratings) | `agents/data_agent.py` |
| RAG context addition | `agents/rag_agent.py` |
| Multi-agent separation | `agents/` folder (4 agents) |
| Backtesting | `modules/financial_model.py` |
| Stress testing | `modules/financial_model.py` |
| Visual charts & tables | `ui/charts.py` |
| Health score % output | `modules/health_score.py` |
| Pros & Cons | `modules/health_score.py` |
| Magnificent Seven | `modules/screener.py` |
| Market cap tiers — Part 1 | `modules/screener.py` |
| Single company audit — Part 2 | `main.py` Tab 1 |
| Code on GitHub | ✅ This repo |

---

## 👤 Author

**Vishnu Narayanan R**  
AI / Data Science — Junior Financial Analyst Intern  
📧 vishnu.r.narayanana25@gmail.com  
🔗 [LinkedIn](https://linkedin.com/in/vishnu-narayanan-r)  
🐙 [GitHub](https://github.com/vishnunarayananr-ai)

---

*Built as part of an AI internship assessment — Veltech Solutions, May 2026*

# main.py
# Entry point — ties all agents, modules and UI together
# Run with: streamlit run main.py

import warnings
warnings.filterwarnings("ignore")

import streamlit as st
import matplotlib
matplotlib.use("Agg")

# ── Import All Agents ─────────────────────────────────────────────────
from agents.data_agent      import DataAgent
from agents.news_agent      import NewsAgent
from agents.sentiment_agent import SentimentAgent
from agents.rag_agent       import RAGAgent

# ── Import All Modules ────────────────────────────────────────────────
from modules.indicators     import IndicatorModule
from modules.health_score   import HealthScoreModule
from modules.screener       import ScreenerModule
from modules.financial_model import FinancialModel

# ── Import UI ─────────────────────────────────────────────────────────
from ui.components import UIComponents
from ui.charts     import ChartModule

# ── Import Helpers ────────────────────────────────────────────────────
from utils.helpers import (
    format_currency,
    format_percentage,
    get_change_color,
    get_arrow,
    timestamp_now,
)


# =============================================================================
# PAGE CONFIG
# =============================================================================

st.set_page_config(
    page_title="AI Strategic Equity Auditor",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

UIComponents.inject_css()


# =============================================================================
# SIDEBAR + HEADER
# =============================================================================

ticker_input, run_audit = UIComponents.render_sidebar("AAPL")
UIComponents.render_header()


# =============================================================================
# TABS
# =============================================================================

tab1, tab2, tab3 = st.tabs([
    "🏥 Company Health Audit",
    "📊 Market Screener",
    "⚗️  Backtest & Stress Test",
])


# =============================================================================
# TAB 1 — COMPANY HEALTH AUDIT (Part 2)
# =============================================================================

with tab1:

    if not run_audit:
        UIComponents.render_idle_screen()
        st.stop()

    # ── Step 1: Fetch Data ────────────────────────────────────────────
    with st.spinner(f"Running full audit for {ticker_input}..."):

        # Agent 1 — Data
        data_agent  = DataAgent(ticker_input)

        if not data_agent.is_valid():
            st.warning(f"⚠️ No data found for **{ticker_input}**. Check the ticker.")
            st.stop()

        price_df    = data_agent.fetch_price_data(period="3mo")
        company     = data_agent.fetch_company_info()
        financials  = data_agent.fetch_financials()
        ratings     = data_agent.fetch_analyst_ratings()

        # Agent 2 — News
        news_agent  = NewsAgent(ticker_input)
        headlines   = news_agent.get_headlines()

        # Agent 3 — Sentiment
        sentiment_agent   = SentimentAgent(headlines)
        sentiment_summary = sentiment_agent.get_summary()

        # Agent 4 — RAG
        rag_agent    = RAGAgent(headlines)
        rag_findings = rag_agent.run_full_pipeline()
        rag_score    = rag_agent.get_rag_score_0_100()

        # Module 1 — Indicators
        indicator_module = IndicatorModule(price_df)
        indicators       = indicator_module.get_all_indicators()

        # Module 2 — Health Score
        health_module = HealthScoreModule(
            price_data      = price_df,
            indicators      = indicators,
            financials      = financials,
            sentiment_score = sentiment_summary["score_0_100"],
            rag_score       = rag_score,
        )
        health_report = health_module.get_full_report()

        # Charts
        charts = ChartModule()

    # ── Step 2: Key Metrics Row ───────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    UIComponents.render_section_title("KEY METRICS")

    close_vals  = price_df["Close"].to_numpy()
    last_price  = float(close_vals[-1])
    prev_price  = float(close_vals[-2]) if close_vals.size > 1 else last_price
    month_open  = float(close_vals[0])
    daily_chg   = (last_price - prev_price) / prev_price * 100
    monthly_chg = (last_price - month_open) / month_open * 100
    vol_ratio   = indicators.get("volume_ratio", 1.0)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        UIComponents.render_metric_card(
            "Last Price",
            format_currency(last_price),
            f"{company.get('name','—')} · {company.get('sector','—')}",
        )
    with c2:
        UIComponents.render_metric_card(
            "Daily Change",
            f"{get_arrow(daily_chg)} {abs(daily_chg):.2f}%",
            "vs previous close",
            get_change_color(daily_chg),
        )
    with c3:
        UIComponents.render_metric_card(
            "3-Month Return",
            f"{get_arrow(monthly_chg)} {abs(monthly_chg):.2f}%",
            "90-day performance",
            get_change_color(monthly_chg),
        )
    with c4:
        UIComponents.render_metric_card(
            "Volume Ratio",
            f"{vol_ratio:.2f}x",
            f"Mkt Cap {company.get('market_cap_fmt','—')}",
            "#3fb950" if vol_ratio > 1.2 else "#7d8590",
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Step 3: Health Score ──────────────────────────────────────────
    UIComponents.render_section_title("COMPANY HEALTH SCORE")

    h_col1, h_col2 = st.columns([1, 2])

    with h_col1:
        UIComponents.render_health_badge(
            health_report["score"],
            health_report["label"],
            health_report["color"],
        )
        st.plotly_chart(
            charts.plot_health_gauge(
                health_report["score"],
                health_report["label"],
                health_report["color"],
            ),
            use_container_width=True
        )

    with h_col2:
        st.markdown("**Score Breakdown:**")
        UIComponents.render_breakdown_bars(health_report["breakdown"])

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Step 4: Pros & Cons ───────────────────────────────────────────
    UIComponents.render_section_title("PROS & CONS ANALYSIS")
    UIComponents.render_pros_cons(
        health_report["pros"],
        health_report["cons"]
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")

    # ── Step 5: Price Chart ───────────────────────────────────────────
    UIComponents.render_section_title(f"PRICE CHART — {ticker_input}")
    st.plotly_chart(
        charts.plot_price_chart(price_df, ticker_input),
        use_container_width=True
    )

    # ── Step 6: Technical Indicators ─────────────────────────────────
    UIComponents.render_section_title("TECHNICAL INDICATORS")

    ind_col1, ind_col2 = st.columns(2)
    with ind_col1:
        st.markdown(f"**RSI Signal:** `{indicators.get('rsi_signal','—')}`")
        st.plotly_chart(
            charts.plot_rsi(indicators["rsi"], ticker_input),
            use_container_width=True
        )
    with ind_col2:
        st.markdown(f"**MACD Signal:** `{indicators.get('macd_signal','—')}`")
        st.plotly_chart(
            charts.plot_macd(indicators["macd"], ticker_input),
            use_container_width=True
        )

    st.plotly_chart(
        charts.plot_bollinger(price_df, indicators["bollinger"], ticker_input),
        use_container_width=True
    )

    st.markdown("---")

    # ── Step 7: RAG Intelligence ──────────────────────────────────────
    UIComponents.render_section_title("AI STRATEGIC BRIEFING — RAG")
    UIComponents.render_rag_findings(rag_findings)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Step 8: Sentiment ─────────────────────────────────────────────
    UIComponents.render_section_title("NEWS SENTIMENT ANALYSIS")

    s = sentiment_summary
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        UIComponents.render_metric_card(
            "Overall Sentiment",
            s["overall_label"],
            f"Avg score: {s['average_score']}",
        )
    with s2:
        UIComponents.render_metric_card(
            "Positive Headlines",
            str(s["positive_count"]),
            f"out of {s['total']}",
            "#3fb950"
        )
    with s3:
        UIComponents.render_metric_card(
            "Negative Headlines",
            str(s["negative_count"]),
            f"out of {s['total']}",
            "#f85149"
        )
    with s4:
        UIComponents.render_metric_card(
            "Neutral Headlines",
            str(s["neutral_count"]),
            f"out of {s['total']}",
            "#d29922"
        )

    # ── Step 9: Analyst Ratings ───────────────────────────────────────
    if ratings:
        st.markdown("<br>", unsafe_allow_html=True)
        UIComponents.render_section_title("ANALYST RATINGS")
        r1, r2, r3, r4, r5 = st.columns(5)
        with r1:
            UIComponents.render_metric_card(
                "Strong Buy", str(ratings.get("strong_buy", 0)),
                "", "#3fb950"
            )
        with r2:
            UIComponents.render_metric_card(
                "Buy", str(ratings.get("buy", 0)),
                "", "#58a6ff"
            )
        with r3:
            UIComponents.render_metric_card(
                "Hold", str(ratings.get("hold", 0)),
                "", "#d29922"
            )
        with r4:
            UIComponents.render_metric_card(
                "Sell", str(ratings.get("sell", 0)),
                "", "#f0883e"
            )
        with r5:
            UIComponents.render_metric_card(
                "Strong Sell", str(ratings.get("strong_sell", 0)),
                "", "#f85149"
            )

    # ── Step 10: Raw News Feed ────────────────────────────────────────
    with st.expander(f"📰 RAW NEWS — {len(headlines)} headlines"):
        for i, h in enumerate(headlines):
            st.markdown(
                f'<div style="padding:0.4rem 0;'
                f'border-bottom:1px solid #21262d;'
                f'font-size:0.73rem; color:#8b949e">'
                f'<span style="color:#58a6ff">#{i+1:02d}</span>'
                f' &nbsp; {h}</div>',
                unsafe_allow_html=True
            )

    st.markdown(
        f'<div style="font-size:0.6rem; color:#484f58;'
        f'text-align:right; margin-top:1rem">'
        f'Last updated: {timestamp_now()}</div>',
        unsafe_allow_html=True
    )


# =============================================================================
# TAB 2 — MARKET SCREENER (Part 1)
# =============================================================================

with tab2:
    UIComponents.render_section_title("MARKET SCREENER — ALL TIERS")

    st.info("⏳ Click **▶ RUN FULL AUDIT** in the sidebar to load screener data.")

    if run_audit:
        screener = ScreenerModule()
        charts   = ChartModule()

        with st.spinner("Scanning market tiers..."):

            # Magnificent Seven
            UIComponents.render_section_title("🌟 MAGNIFICENT SEVEN")
            mag7 = screener.get_magnificent_seven()
            if mag7:
                st.plotly_chart(
                    charts.plot_screener_table(mag7, "Magnificent Seven"),
                    use_container_width=True
                )

            st.markdown("---")

            # > $500B
            UIComponents.render_section_title("🏆 MARKET CAP > $500B — TOP 5")
            top500 = screener.get_top_500b_plus()
            if top500:
                st.plotly_chart(
                    charts.plot_screener_table(
                        top500, "Best 5 — Market Cap > $500B"
                    ),
                    use_container_width=True
                )

            st.markdown("---")

            # $100B–$500B
            UIComponents.render_section_title("📈 MARKET CAP $100B–$500B — TOP 7")
            mid = screener.get_top_100_500b()
            if mid:
                st.plotly_chart(
                    charts.plot_screener_table(
                        mid, "Best 7 — Market Cap $100B–$500B"
                    ),
                    use_container_width=True
                )

            st.markdown("---")

            # < $100B
            UIComponents.render_section_title("🚀 MARKET CAP < $100B — TOP 10")
            small = screener.get_top_under_100b()
            if small:
                st.plotly_chart(
                    charts.plot_screener_table(
                        small, "Best 10 — Market Cap < $100B"
                    ),
                    use_container_width=True
                )


# =============================================================================
# TAB 3 — BACKTEST & STRESS TEST
# =============================================================================

with tab3:
    UIComponents.render_section_title("BACKTEST & STRESS TEST")

    st.info("⏳ Click **▶ RUN FULL AUDIT** in the sidebar to load analysis.")

    if run_audit:
        charts = ChartModule()

        with st.spinner("Running financial models..."):
            price_df_long = data_agent.fetch_price_data(period="1y")
            fin_model     = FinancialModel(price_df_long)
            full_analysis = fin_model.get_full_analysis()

        # Regression
        UIComponents.render_section_title("📉 LINEAR REGRESSION TREND")
        reg = full_analysis.get("regression", {})
        if reg:
            r1, r2, r3 = st.columns(3)
            with r1:
                UIComponents.render_metric_card(
                    "Trend Direction",
                    reg.get("direction", "—"), ""
                )
            with r2:
                UIComponents.render_metric_card(
                    "Predicted Price (10d)",
                    f"${reg.get('predicted_price','—')}",
                    f"Current: ${reg.get('current_price','—')}"
                )
            with r3:
                UIComponents.render_metric_card(
                    "R² Score",
                    str(reg.get("r_squared", "—")),
                    "Model fit quality"
                )

        st.markdown("---")

        # Backtest
        UIComponents.render_section_title("🔁 BACKTESTING — MA CROSSOVER STRATEGY")
        backtest = full_analysis.get("backtest", {})
        if backtest and "error" not in backtest:
            b1, b2, b3 = st.columns(3)
            with b1:
                UIComponents.render_metric_card(
                    "Market Return",
                    f"{backtest.get('market_return','—')}%",
                    "Buy & Hold",
                    "#3fb950"
                )
            with b2:
                UIComponents.render_metric_card(
                    "Strategy Return",
                    f"{backtest.get('strategy_return','—')}%",
                    "MA Crossover",
                    "#58a6ff"
                )
            with b3:
                UIComponents.render_metric_card(
                    "Verdict",
                    "✅ Beat" if backtest.get("outperformed") else "❌ Lagged",
                    backtest.get("verdict", ""),
                )
            st.plotly_chart(
                charts.plot_backtest(backtest, ticker_input),
                use_container_width=True
            )

        st.markdown("---")

        # Stress Test
        UIComponents.render_section_title("⚠️ STRESS TEST — CRASH SCENARIOS")
        stress = full_analysis.get("stress_test", {})
        if stress:
            UIComponents.render_metric_card(
                "Stock Beta",
                str(stress.get("beta", "—")),
                "Market sensitivity"
            )
            st.plotly_chart(
                charts.plot_stress_test(stress, ticker_input),
                use_container_width=True
            )

        st.markdown("---")

        # Outliers
        UIComponents.render_section_title("🔍 OUTLIER DETECTION")
        outliers = full_analysis.get("outliers", {})
        if outliers:
            o1, o2, o3 = st.columns(3)
            with o1:
                UIComponents.render_metric_card(
                    "Outliers Detected",
                    str(outliers.get("outlier_count", 0)),
                    "Unusual price movements"
                )
            with o2:
                UIComponents.render_metric_card(
                    "Max Single Day Drop",
                    f"{outliers.get('max_drop','—')}%",
                    "Worst daily return",
                    "#f85149"
                )
            with o3:
                UIComponents.render_metric_card(
                    "Max Single Day Gain",
                    f"{outliers.get('max_gain','—')}%",
                    "Best daily return",
                    "#3fb950"
                )

        # Sharpe Ratio
        sharpe = full_analysis.get("sharpe", 0)
        sharpe_color = (
            "#3fb950" if sharpe > 1
            else "#d29922" if sharpe > 0
            else "#f85149"
        )
        UIComponents.render_metric_card(
            "Sharpe Ratio",
            str(sharpe),
            "Risk-adjusted return · >1 = Good · >2 = Excellent",
            sharpe_color
        )
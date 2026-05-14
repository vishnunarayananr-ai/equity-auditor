# ui/components.py
# Responsible for ALL reusable Streamlit UI components
# Single responsibility: UI COMPONENTS ONLY — no logic, no data

import streamlit as st

# ── CUSTOM CSS ────────────────────────────────────────────────────────

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Syne:wght@700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Mono', monospace;
    background-color: #0a0e14;
    color: #c9d1d9;
}
.main-header {
    font-family: 'Syne', sans-serif;
    font-size: 2.4rem;
    font-weight: 800;
    letter-spacing: -1px;
    background: linear-gradient(90deg, #58a6ff, #79c0ff, #a8d8ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem;
}
.sub-header {
    font-size: 0.72rem;
    color: #58a6ff;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 2rem;
}
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: #e6edf3;
    letter-spacing: 1px;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid #21262d;
    margin-bottom: 1.2rem;
}
.metric-card {
    background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
    border: 1px solid #21262d;
    border-left: 3px solid #58a6ff;
    border-radius: 8px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
}
.metric-label {
    font-size: 0.62rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #58a6ff;
    margin-bottom: 0.4rem;
}
.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: #e6edf3;
}
.metric-sub {
    font-size: 0.68rem;
    color: #7d8590;
    margin-top: 0.3rem;
}
.finding-card {
    background: #0d1117;
    border: 1px solid #21262d;
    border-radius: 6px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
}
.finding-category {
    font-size: 0.6rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.finding-text {
    font-size: 0.76rem;
    color: #c9d1d9;
    line-height: 1.6;
}
.signal-badge {
    display: inline-block;
    font-size: 0.58rem;
    padding: 2px 10px;
    border-radius: 20px;
    letter-spacing: 2px;
    margin-top: 0.6rem;
    border: 1px solid;
}
.health-card {
    background: #0d1117;
    border: 1px solid #21262d;
    border-radius: 8px;
    padding: 1.5rem;
    text-align: center;
    margin-bottom: 1rem;
}
.pros-cons-card {
    background: #0d1117;
    border: 1px solid #21262d;
    border-radius: 8px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
}
.status-online {
    display: inline-block;
    background: rgba(63,185,80,0.1);
    border: 1px solid #3fb950;
    color: #3fb950;
    font-size: 0.62rem;
    padding: 4px 12px;
    border-radius: 20px;
    letter-spacing: 2px;
}
[data-testid="stSidebar"] {
    background: #0d1117;
    border-right: 1px solid #21262d;
}
[data-testid="stSidebar"] .stTextInput input {
    background: #161b22;
    border: 1px solid #30363d;
    color: #e6edf3;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.1rem;
    letter-spacing: 3px;
    text-transform: uppercase;
}
[data-testid="stSidebar"] .stButton button {
    background: linear-gradient(135deg, #1f6feb, #388bfd);
    color: white;
    border: none;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    width: 100%;
    padding: 0.7rem;
    border-radius: 6px;
    transition: opacity 0.2s;
}
[data-testid="stSidebar"] .stButton button:hover { opacity: 0.82; }
hr { border-color: #21262d; }
</style>
"""


class UIComponents:
    """
    Reusable Streamlit UI building blocks.
    Single responsibility: UI RENDERING ONLY.
    """

    @staticmethod
    def inject_css() -> None:
        """Inject custom CSS into the Streamlit app."""
        st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    @staticmethod
    def render_header() -> None:
        """Render the main app header."""
        st.markdown(
            '<div class="main-header">📈 AI Strategic Equity Auditor</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="sub-header">Real-time Intelligence · RAG · Multi-Agent · Financial Modelling</div>',
            unsafe_allow_html=True,
        )

    @staticmethod
    def render_section_title(title: str) -> None:
        """Render a styled section title."""
        st.markdown(
            f'<div class="section-title">◈ {title}</div>',
            unsafe_allow_html=True,
        )

    @staticmethod
    def render_metric_card(
        label: str,
        value: str,
        sub: str = "",
        color: str = "#58a6ff"
    ) -> None:
        """
        Render a styled KPI metric card.

        Plain English:
        The little boxes at the top of the dashboard
        showing price, daily change, volume etc.
        """
        st.markdown(f"""
        <div class="metric-card" style="border-left-color:{color}">
            <div class="metric-label">{label}</div>
            <div class="metric-value" style="color:{color}">{value}</div>
            <div class="metric-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

    @staticmethod
    def render_health_badge(
        score: float,
        label: str,
        color: str
    ) -> None:
        """
        Render the health score badge.

        Plain English:
        Big colored number showing
        the overall company health %.
        """
        st.markdown(f"""
        <div class="health-card">
            <div style="font-size:0.62rem; letter-spacing:3px;
            color:#58a6ff; text-transform:uppercase;
            margin-bottom:0.5rem">Overall Health Score</div>
            <div style="font-family:Syne,sans-serif;
            font-size:3.5rem; font-weight:800;
            color:{color}">{score}%</div>
            <div style="font-size:0.8rem; color:{color};
            letter-spacing:2px; margin-top:0.3rem">{label}</div>
        </div>""", unsafe_allow_html=True)

    @staticmethod
    def render_pros_cons(pros: list, cons: list) -> None:
        """
        Render two-column pros and cons display.

        Plain English:
        Left column = green positive factors
        Right column = red negative factors
        """
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            <div class="pros-cons-card">
            <div style="font-size:0.62rem; letter-spacing:3px;
            color:#3fb950; text-transform:uppercase;
            margin-bottom:0.8rem">✅ PROS</div>
            """, unsafe_allow_html=True)
            for pro in pros:
                st.markdown(
                    f'<div style="font-size:0.75rem; '
                    f'color:#c9d1d9; padding:0.3rem 0; '
                    f'border-bottom:1px solid #21262d">'
                    f'{pro}</div>',
                    unsafe_allow_html=True
                )
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="pros-cons-card">
            <div style="font-size:0.62rem; letter-spacing:3px;
            color:#f85149; text-transform:uppercase;
            margin-bottom:0.8rem">❌ CONS</div>
            """, unsafe_allow_html=True)
            for con in cons:
                st.markdown(
                    f'<div style="font-size:0.75rem; '
                    f'color:#c9d1d9; padding:0.3rem 0; '
                    f'border-bottom:1px solid #21262d">'
                    f'{con}</div>',
                    unsafe_allow_html=True
                )
            st.markdown("</div>", unsafe_allow_html=True)

    @staticmethod
    def render_rag_findings(findings: list) -> None:
        """
        Render RAG result cards in 2-column grid.

        Plain English:
        Shows 4 cards — one for each category
        (Financial Health, Growth, Risk, Outlook)
        with the most relevant headline for each.
        """
        col_l, col_r = st.columns(2)
        for i, f in enumerate(findings):
            col = col_l if i % 2 == 0 else col_r
            confidence = int(f["score"] * 100)
            with col:
                st.markdown(f"""
                <div class="finding-card">
                    <div class="finding-category"
                    style="color:{f['color']}">
                        {f['icon']} {f['category']}
                    </div>
                    <div class="finding-text">{f['headline']}</div>
                    <span class="signal-badge"
                    style="color:{f['color']};
                    border-color:{f['color']};
                    background:rgba(0,0,0,0.3)">
                        {f['signal']} · {confidence}% RELEVANCE
                    </span>
                </div>""", unsafe_allow_html=True)

    @staticmethod
    def render_signal_badge(signal: str, color: str) -> None:
        """Render a small colored signal badge."""
        st.markdown(
            f'<span class="signal-badge" '
            f'style="color:{color}; border-color:{color}">'
            f'{signal}</span>',
            unsafe_allow_html=True
        )

    @staticmethod
    def render_sidebar(ticker_input: str) -> tuple:
        """
        Render the full sidebar with input and info.
        Returns (ticker, run_button_clicked).
        """
        with st.sidebar:
            st.markdown(
                '<div class="main-header" '
                'style="font-size:1.4rem">⬡ EQUITY<br>AUDITOR</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div class="sub-header">AI · RAG · Multi-Agent</div>',
                unsafe_allow_html=True,
            )

            ticker = st.text_input(
                "TICKER SYMBOL",
                ticker_input
            ).upper().strip()

            run = st.button("▶  RUN FULL AUDIT")

            st.markdown("---")
            st.markdown(
                '<div class="status-online">● ALL SYSTEMS ONLINE</div>',
                unsafe_allow_html=True
            )
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
            <div style='font-size:0.62rem;
            color:#7d8590; line-height:2'>
            ACTIVE AGENTS<br>
            ─────────────────<br>
            ✓ DataAgent · market data<br>
            ✓ NewsAgent · scraper<br>
            ✓ SentimentAgent · NLP<br>
            ✓ RAGAgent · embeddings<br>
            ─────────────────<br>
            ACTIVE MODULES<br>
            ─────────────────<br>
            ✓ IndicatorModule · RSI/MACD<br>
            ✓ HealthScoreModule · scoring<br>
            ✓ ScreenerModule · screener<br>
            ✓ FinancialModel · ML/backtest
            </div>
            """, unsafe_allow_html=True)

        return ticker, run

    @staticmethod
    def render_idle_screen() -> None:
        """Render the idle/welcome screen."""
        st.markdown("""
        <div style='background:#0d1117;
        border:1px solid #21262d;
        border-radius:8px; padding:2.5rem;
        text-align:center; margin-top:2rem;
        color:#7d8590; font-size:0.8rem;'>
        Enter a ticker symbol in the sidebar and click
        <b style='color:#58a6ff'>▶ RUN FULL AUDIT</b>
        to begin.<br><br>
        <span style='font-size:0.62rem;
        letter-spacing:4px; color:#30363d'>
        AAPL · TSLA · NVDA · MSFT · AMZN · GOOGL
        </span>
        </div>
        """, unsafe_allow_html=True)

    @staticmethod
    def render_breakdown_bars(breakdown: dict) -> None:
        """
        Render health score component breakdown
        as individual progress bars.

        Plain English:
        Shows how much each factor contributed
        to the final health score.
        """
        st.markdown("<br>", unsafe_allow_html=True)
        for component, score in breakdown.items():
            color = (
                "#3fb950" if score >= 70
                else "#d29922" if score >= 40
                else "#f85149"
            )
            st.markdown(f"""
            <div style="margin-bottom:0.6rem">
                <div style="display:flex;
                justify-content:space-between;
                font-size:0.65rem; color:#7d8590;
                margin-bottom:0.2rem">
                    <span>{component}</span>
                    <span style="color:{color}">{score:.1f}</span>
                </div>
                <div style="background:#21262d;
                border-radius:4px; height:6px">
                    <div style="background:{color};
                    width:{score}%; height:6px;
                    border-radius:4px"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
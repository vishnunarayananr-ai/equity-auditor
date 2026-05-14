# ui/charts.py
# Responsible for ALL chart and visualization functions
# Single responsibility: CHARTS ONLY — no data fetching, no logic

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class ChartModule:
    """
    Builds all interactive Plotly charts.
    Single responsibility: VISUALIZATION ONLY.
    """

    # Common dark theme colors
    BG_COLOR    = "#0d1117"
    GRID_COLOR  = "#21262d"
    TEXT_COLOR  = "#c9d1d9"
    BLUE        = "#58a6ff"
    GREEN       = "#3fb950"
    RED         = "#f85149"
    YELLOW      = "#d29922"

    def _base_layout(self, title: str) -> dict:
        """Base dark theme layout used by all charts."""
        return dict(
            title=dict(text=title, font=dict(color=self.TEXT_COLOR, size=14)),
            paper_bgcolor=self.BG_COLOR,
            plot_bgcolor=self.BG_COLOR,
            font=dict(color=self.TEXT_COLOR),
            xaxis=dict(gridcolor=self.GRID_COLOR, showgrid=True),
            yaxis=dict(gridcolor=self.GRID_COLOR, showgrid=True),
            margin=dict(l=40, r=40, t=50, b=40),
        )

    # ── 1. PRICE CHART ───────────────────────────────────────────────

    def plot_price_chart(
        self,
        df: pd.DataFrame,
        ticker: str
    ) -> go.Figure:
        """
        Candlestick price chart with volume bars.

        Plain English:
        Green candle = price went UP that day
        Red candle   = price went DOWN that day
        Volume bars  = how many shares were traded
        """
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            row_heights=[0.75, 0.25],
            vertical_spacing=0.02
        )

        close = df["Close"].to_numpy()
        open_ = df["Open"].to_numpy()
        high  = df["High"].to_numpy()
        low   = df["Low"].to_numpy()
        vol   = df["Volume"].to_numpy()
        dates = df.index

        # Candlestick
        fig.add_trace(go.Candlestick(
            x=dates,
            open=open_, high=high,
            low=low,    close=close,
            increasing_line_color=self.GREEN,
            decreasing_line_color=self.RED,
            name="Price"
        ), row=1, col=1)

        # Volume bars
        colors = [
            self.GREEN if close_value >= open_value
            else self.RED
            for close_value, open_value in zip(close, open_)
        ]
        fig.add_trace(go.Bar(
            x=dates, y=vol,
            marker_color=colors,
            name="Volume",
            opacity=0.6
        ), row=2, col=1)

        layout = self._base_layout(f"{ticker} — Price & Volume")
        layout["xaxis_rangeslider_visible"] = False
        layout["showlegend"] = False
        fig.update_layout(**layout)

        return fig

    # ── 2. RSI CHART ─────────────────────────────────────────────────

    def plot_rsi(
        self,
        rsi: pd.Series,
        ticker: str
    ) -> go.Figure:
        """
        RSI chart with overbought/oversold lines.

        Plain English:
        Red line at 70  = overbought zone (might drop)
        Green line at 30 = oversold zone (might rise)
        RSI line moving between = healthy
        """
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=rsi.index, y=rsi.values,
            line=dict(color=self.BLUE, width=2),
            name="RSI"
        ))

        # Overbought line
        fig.add_hline(
            y=70, line_dash="dash",
            line_color=self.RED,
            annotation_text="Overbought (70)"
        )

        # Oversold line
        fig.add_hline(
            y=30, line_dash="dash",
            line_color=self.GREEN,
            annotation_text="Oversold (30)"
        )

        # Middle line
        fig.add_hline(y=50, line_dash="dot",
                      line_color=self.GRID_COLOR)

        fig.update_layout(**self._base_layout(f"{ticker} — RSI (14)"))
        fig.update_yaxes(range=[0, 100])

        return fig

    # ── 3. MACD CHART ────────────────────────────────────────────────

    def plot_macd(
        self,
        macd_data: dict,
        ticker: str
    ) -> go.Figure:
        """
        MACD chart with signal line and histogram.

        Plain English:
        When MACD line crosses ABOVE signal = buy signal 🟢
        When MACD line crosses BELOW signal = sell signal 🔴
        Histogram shows the gap between them
        """
        fig = make_subplots(rows=2, cols=1,
                            shared_xaxes=True,
                            row_heights=[0.6, 0.4],
                            vertical_spacing=0.05)

        macd   = macd_data["macd"]
        signal = macd_data["signal"]
        hist   = macd_data["histogram"]

        # MACD and Signal lines
        fig.add_trace(go.Scatter(
            x=macd.index, y=macd.values,
            line=dict(color=self.BLUE, width=2),
            name="MACD"
        ), row=1, col=1)

        fig.add_trace(go.Scatter(
            x=signal.index, y=signal.values,
            line=dict(color=self.YELLOW, width=1.5),
            name="Signal"
        ), row=1, col=1)

        # Histogram
        colors = [
            self.GREEN if v >= 0 else self.RED
            for v in hist.values
        ]
        fig.add_trace(go.Bar(
            x=hist.index, y=hist.values,
            marker_color=colors,
            name="Histogram"
        ), row=2, col=1)

        fig.update_layout(**self._base_layout(f"{ticker} — MACD"))

        return fig

    # ── 4. HEALTH GAUGE ──────────────────────────────────────────────

    def plot_health_gauge(
        self,
        score: float,
        label: str,
        color: str
    ) -> go.Figure:
        """
        Circular gauge showing company health %.

        Plain English:
        Like a speedometer — shows how healthy
        the company is from 0% to 100%.
        Green = healthy, Red = unhealthy
        """
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=score,
            title=dict(
                text=f"Overall Health: {label}",
                font=dict(color=self.TEXT_COLOR, size=16)
            ),
            number=dict(
                suffix="%",
                font=dict(color=color, size=40)
            ),
            gauge=dict(
                axis=dict(
                    range=[0, 100],
                    tickcolor=self.TEXT_COLOR
                ),
                bar=dict(color=color),
                bgcolor=self.BG_COLOR,
                bordercolor=self.GRID_COLOR,
                steps=[
                    dict(range=[0,  35], color="#1a0a0a"),
                    dict(range=[35, 50], color="#1a1000"),
                    dict(range=[50, 65], color="#0a1a00"),
                    dict(range=[65, 80], color="#001a0a"),
                    dict(range=[80, 100], color="#001a10"),
                ],
                threshold=dict(
                    line=dict(color=color, width=4),
                    thickness=0.75,
                    value=score
                )
            )
        ))

        fig.update_layout(
            paper_bgcolor=self.BG_COLOR,
            font=dict(color=self.TEXT_COLOR),
            margin=dict(l=30, r=30, t=60, b=30),
            height=300
        )

        return fig

    # ── 5. BACKTEST CHART ────────────────────────────────────────────

    def plot_backtest(
        self,
        backtest_data: dict,
        ticker: str
    ) -> go.Figure:
        """
        Backtest performance chart.

        Plain English:
        Blue line  = how our MA strategy performed
        Green line = how just holding the stock performed
        If blue > green = our strategy was better!
        """
        fig = go.Figure()

        dates    = backtest_data.get("dates", [])
        market   = backtest_data.get("cumulative_market", [])
        strategy = backtest_data.get("cumulative_strategy", [])

        fig.add_trace(go.Scatter(
            x=dates, y=market,
            line=dict(color=self.GREEN, width=2),
            name="Buy & Hold"
        ))

        fig.add_trace(go.Scatter(
            x=dates, y=strategy,
            line=dict(color=self.BLUE, width=2),
            name="MA Strategy"
        ))

        fig.add_hline(y=1.0, line_dash="dot",
                      line_color=self.GRID_COLOR)

        fig.update_layout(
            **self._base_layout(f"{ticker} — Backtest: MA Strategy vs Buy & Hold")
        )

        return fig

    # ── 6. BOLLINGER BANDS ───────────────────────────────────────────

    def plot_bollinger(
        self,
        df: pd.DataFrame,
        bollinger: dict,
        ticker: str
    ) -> go.Figure:
        """
        Bollinger Bands chart.

        Plain English:
        Middle band = 20-day average price
        Upper band  = price is HIGH relative to average
        Lower band  = price is LOW relative to average
        Price touching upper = might drop
        Price touching lower = might rise
        """
        fig = go.Figure()

        close  = df["Close"].squeeze()
        dates  = df.index
        upper  = bollinger.get("upper",  pd.Series())
        middle = bollinger.get("middle", pd.Series())
        lower  = bollinger.get("lower",  pd.Series())

        # Shaded band area
        fig.add_trace(go.Scatter(
            x=list(dates) + list(dates[::-1]),
            y=list(upper) + list(lower[::-1]),
            fill="toself",
            fillcolor="rgba(88,166,255,0.05)",
            line=dict(color="rgba(0,0,0,0)"),
            name="Band Range"
        ))

        fig.add_trace(go.Scatter(
            x=dates, y=upper,
            line=dict(color=self.BLUE, width=1, dash="dash"),
            name="Upper Band"
        ))

        fig.add_trace(go.Scatter(
            x=dates, y=middle,
            line=dict(color=self.YELLOW, width=1.5),
            name="Middle (SMA20)"
        ))

        fig.add_trace(go.Scatter(
            x=dates, y=lower,
            line=dict(color=self.BLUE, width=1, dash="dash"),
            name="Lower Band"
        ))

        fig.add_trace(go.Scatter(
            x=dates, y=close,
            line=dict(color=self.TEXT_COLOR, width=2),
            name="Price"
        ))

        fig.update_layout(
            **self._base_layout(f"{ticker} — Bollinger Bands")
        )

        return fig

    # ── 7. STRESS TEST CHART ─────────────────────────────────────────

    def plot_stress_test(
        self,
        stress_data: dict,
        ticker: str
    ) -> go.Figure:
        """
        Stress test bar chart.

        Plain English:
        Shows how much the stock price would drop
        in each crash scenario.
        Taller red bar = bigger loss in that scenario.
        """
        scenarios = stress_data.get("scenarios", {})
        if not scenarios:
            return go.Figure()

        labels  = list(scenarios.keys())
        drops   = [
            float(v["stock_drop"].replace("%", ""))
            for v in scenarios.values()
        ]
        prices  = [v["projected_price"] for v in scenarios.values()]
        current = stress_data.get("current", 0)

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=labels,
            y=drops,
            marker_color=self.RED,
            text=[f"${p}" for p in prices],
            textposition="outside",
            name="Price Drop %"
        ))

        fig.update_layout(
            **self._base_layout(
                f"{ticker} — Stress Test "
                f"(Current: ${current}) | Beta: {stress_data.get('beta', '—')}"
            )
        )

        return fig

    # ── 8. SCREENER TABLE ────────────────────────────────────────────

    def plot_screener_table(
        self,
        companies: list,
        title: str
    ) -> go.Figure:
        """
        Company comparison table.

        Plain English:
        Shows all companies side by side in a table
        with their name, market cap, PE ratio, beta and score.
        """
        if not companies:
            return go.Figure()

        tickers   = [c.get("ticker",       "—") for c in companies]
        names     = [c.get("name",         "—") for c in companies]
        caps      = [c.get("market_cap_fmt","—") for c in companies]
        sectors   = [c.get("sector",       "—") for c in companies]
        pe_ratios = [str(c.get("pe_ratio", "—")) for c in companies]
        betas     = [str(c.get("beta",     "—")) for c in companies]
        scores    = [str(c.get("score",    "—")) for c in companies]
        prices    = [f"${c.get('price', '—')}"  for c in companies]

        fig = go.Figure(go.Table(
            header=dict(
                values=["Ticker", "Name", "Market Cap",
                        "Sector", "Price", "P/E", "Beta", "Score"],
                fill_color="#161b22",
                font=dict(color=self.BLUE, size=12),
                align="left",
                height=35
            ),
            cells=dict(
                values=[tickers, names, caps,
                        sectors, prices, pe_ratios, betas, scores],
                fill_color=self.BG_COLOR,
                font=dict(color=self.TEXT_COLOR, size=11),
                align="left",
                height=30
            )
        ))

        fig.update_layout(
            paper_bgcolor=self.BG_COLOR,
            margin=dict(l=0, r=0, t=40, b=0),
            title=dict(
                text=title,
                font=dict(color=self.TEXT_COLOR, size=14)
            )
        )

        return fig
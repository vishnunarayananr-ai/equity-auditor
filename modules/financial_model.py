# modules/financial_model.py
# Responsible for ALL financial modelling, backtesting, stress testing
# Single responsibility: MODELLING ONLY — no UI, no fetching

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

class FinancialModel:
    """
    Statistical & ML modelling, backtesting, stress testing.
    Single responsibility: FINANCIAL MODELLING ONLY.

    Plain English:
    - Detects outliers (unusual price movements)
    - Predicts price trend using linear regression
    - Backtests a simple MA crossover strategy
    - Stress tests portfolio under market crash scenarios
    """

    def __init__(self, df: pd.DataFrame):
        """
        Parameters
        ----------
        df : pd.DataFrame
            OHLCV DataFrame from DataAgent.fetch_price_data()
        """
        self.df    = df.copy()
        self.close = df["Close"].astype(float)
        self.dates = df.index

    # ── 1. OUTLIER DETECTION ─────────────────────────────────────────

    def detect_outliers(self) -> dict:
        """
        Detect unusual price movements using IQR and Z-Score.

        Plain English:
        IQR   = finds prices that are way above or below normal range
        Z-Score = finds prices that are statistically abnormal
        Both methods together = more reliable detection
        """
        try:
            returns = self.close.pct_change().dropna()

            # Method 1: IQR (Interquartile Range)
            Q1  = returns.quantile(0.25)
            Q3  = returns.quantile(0.75)
            IQR = Q3 - Q1
            iqr_outliers = returns[
                (returns < Q1 - 1.5 * IQR) |
                (returns > Q3 + 1.5 * IQR)
            ]

            # Method 2: Z-Score
            mean    = returns.mean()
            std     = returns.std()
            z_scores = (returns - mean) / std
            z_outliers = returns[abs(z_scores) > 2.5]

            return {
                "iqr_outliers":   iqr_outliers,
                "z_outliers":     z_outliers,
                "outlier_count":  len(iqr_outliers),
                "outlier_dates":  iqr_outliers.index.tolist(),
                "outlier_values": iqr_outliers.values.tolist(),
                "max_drop":       round(float(returns.min()) * 100, 2),
                "max_gain":       round(float(returns.max()) * 100, 2),
            }
        except Exception:
            return {}

    # ── 2. LINEAR REGRESSION TREND ───────────────────────────────────

    def linear_regression_trend(self) -> dict:
        """
        Predict price trend using Linear Regression.

        Plain English:
        Draws a straight line through all past prices.
        If line goes up = upward trend.
        If line goes down = downward trend.
        Then extends that line 10 days into the future.
        """
        try:
            close = self.close.dropna()
            X = np.arange(len(close)).reshape(-1, 1)
            y = close.values

            model = LinearRegression()
            model.fit(X, y.values if hasattr(y, 'values') else y)  # type: ignore

            # Predict next 10 days
            future_X     = np.arange(
                len(close), len(close) + 10
            ).reshape(-1, 1)
            future_prices = model.predict(future_X)
            trend_line    = model.predict(X)

            slope     = float(model.coef_[0])
            direction = "UPWARD ↑" if slope > 0 else "DOWNWARD ↓"

            return {
                "slope":          round(slope, 4),
                "direction":      direction,
                "r_squared": round(float(model.score(X, y.values if hasattr(y, 'values') else y)), 4),  # type: ignore
                "trend_line":     trend_line.tolist(),
                "future_prices":  future_prices.tolist(),
                "current_price":  round(float(close.iloc[-1]), 2),
                "predicted_price": round(float(future_prices[-1]), 2),
            }
        except Exception:
            return {}

    # ── 3. MOVING AVERAGE MODELS ─────────────────────────────────────

    def moving_averages(self) -> dict:
        """
        Simple Moving Average (SMA) and
        Exponential Moving Average (EMA).

        Plain English:
        SMA = average of last N days prices (equal weight)
        EMA = average but recent days count MORE than older days
        EMA reacts faster to price changes than SMA.=
        """
        try:
            sma_20  = self.close.rolling(window=20).mean()
            sma_50  = self.close.rolling(window=50).mean()
            ema_20  = self.close.ewm(span=20, adjust=False).mean()
            ema_50  = self.close.ewm(span=50, adjust=False).mean()

            # Signal: price above SMA = bullish
            latest_price = float(self.close.iloc[-1])
            latest_sma20 = float(sma_20.dropna().iloc[-1])
            signal = "BULLISH 🟢" if latest_price > latest_sma20 else "BEARISH 🔴"

            return {
                "sma_20":  sma_20,
                "sma_50":  sma_50,
                "ema_20":  ema_20,
                "ema_50":  ema_50,
                "signal":  signal,
                "latest_sma20": round(latest_sma20, 2),
                "latest_price": round(latest_price, 2),
            }
        except Exception:
            return {}

    # ── 4. BACKTESTING ───────────────────────────────────────────────

    def backtest_ma_strategy(self) -> dict:
        """
        Backtest a simple Moving Average Crossover strategy.

        Plain English:
        Strategy rule:
        - BUY when 20-day MA crosses ABOVE 50-day MA
        - SELL when 20-day MA crosses BELOW 50-day MA

        Then we compare:
        - How much money did this strategy make?
        - vs just holding the stock (buy and hold)

        This tells us if our strategy is actually useful.
        """
        try:
            df = pd.DataFrame({"close": self.close})
            df["sma20"] = df["close"].rolling(20).mean()
            df["sma50"] = df["close"].rolling(50).mean()
            df = df.dropna()

            if len(df) < 2:
                return {"error": "Not enough data for backtesting"}

            # Generate signals
            df["signal"]   = 0
            df.loc[df["sma20"] > df["sma50"], "signal"] = 1
            df.loc[df["sma20"] < df["sma50"], "signal"] = -1

            # Calculate returns
            df["daily_return"]    = df["close"].pct_change()
            df["strategy_return"] = df["signal"].shift(1) * df["daily_return"]

            # Cumulative performance
            df["cumulative_market"]   = (1 + df["daily_return"]).cumprod()
            df["cumulative_strategy"] = (1 + df["strategy_return"]).cumprod()

            market_return   = float(df["cumulative_market"].iloc[-1]  - 1) * 100
            strategy_return = float(df["cumulative_strategy"].iloc[-1] - 1) * 100
            outperformed    = strategy_return > market_return

            return {
                "market_return":      round(market_return,   2),
                "strategy_return":    round(strategy_return, 2),
                "outperformed":       outperformed,
                "verdict":            "✅ Strategy Beat Market" if outperformed else "❌ Buy & Hold Was Better",
                "cumulative_market":  df["cumulative_market"].tolist(),
                "cumulative_strategy": df["cumulative_strategy"].tolist(),
                "dates":              df.index.tolist(),
            }
        except Exception:
            return {}

    # ── 5. STRESS TESTING ────────────────────────────────────────────

    def stress_test(self) -> dict:
        """
        Simulate portfolio performance under market crash scenarios.

        Plain English:
        "What if the market dropped 10%, 20%, or 30% tomorrow?
        How much would THIS stock lose based on its beta?"

        Beta = how much a stock moves vs the market
        Beta 1.0 = moves exactly with market
        Beta 1.5 = moves 50% MORE than market (riskier)
        Beta 0.5 = moves 50% LESS than market (safer)
        """
        try:
            returns  = self.close.pct_change().dropna()
            beta     = float(returns.cov(returns) / returns.var()) if returns.var() != 0 else 1.0

            scenarios = {
                "Mild Crash (-10%)":    -0.10,
                "Moderate Crash (-20%)": -0.20,
                "Severe Crash (-30%)":  -0.30,
                "Extreme Crash (-50%)": -0.50,
            }

            results = {}
            current = float(self.close.iloc[-1])

            for scenario, market_drop in scenarios.items():
                # Stock drop = market drop × beta
                stock_drop     = market_drop * beta
                projected_price = current * (1 + stock_drop)
                loss_amount    = current - projected_price

                results[scenario] = {
                    "market_drop":      f"{market_drop * 100:.0f}%",
                    "stock_drop":       f"{stock_drop * 100:.1f}%",
                    "projected_price":  round(projected_price, 2),
                    "loss_amount":      round(loss_amount, 2),
                    "severity":         "HIGH" if abs(stock_drop) > 0.25 else "MEDIUM" if abs(stock_drop) > 0.15 else "LOW",
                }

            return {
                "beta":      round(beta, 3),
                "current":   round(current, 2),
                "scenarios": results,
            }
        except Exception:
            return {}

    # ── 6. SHARPE RATIO ──────────────────────────────────────────────

    def calculate_sharpe(self, risk_free_rate: float = 0.05) -> float:
        """
        Sharpe Ratio = risk-adjusted return.

        Plain English:
        "How much return are you getting per unit of risk?"
        Higher Sharpe = better investment
        Above 1.0 = good
        Above 2.0 = excellent
        Below 0   = not worth the risk
        """
        try:
            returns      = self.close.pct_change().dropna()
            excess       = returns - (risk_free_rate / 252)
            sharpe       = float(excess.mean() / excess.std()) * np.sqrt(252)
            return round(sharpe, 3)
        except Exception:
            return 0.0

    # ── 7. MASTER METHOD ─────────────────────────────────────────────

    def get_full_analysis(self) -> dict:
        """
        Master method — returns all models in one call.
        Used directly by main.py and ui/charts.py.
        """
        return {
            "outliers":    self.detect_outliers(),
            "regression":  self.linear_regression_trend(),
            "moving_avg":  self.moving_averages(),
            "backtest":    self.backtest_ma_strategy(),
            "stress_test": self.stress_test(),
            "sharpe":      self.calculate_sharpe(),
        }
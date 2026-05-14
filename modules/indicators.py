# modules/indicators.py
# Responsible for ALL technical indicator calculations
# Single responsibility: INDICATORS ONLY — no fetching, no UI

import pandas as pd
import numpy as np

class IndicatorModule:
    """
    Calculates all technical indicators from price data.
    Single responsibility: TECHNICAL INDICATORS ONLY.
    """

    def __init__(self, df: pd.DataFrame):
        """
        Parameters
        ----------
        df : pd.DataFrame
            OHLCV DataFrame from DataAgent.fetch_price_data()
        """
        self.df: pd.DataFrame = df.copy()
        self.close: pd.Series = df["Close"].astype(float)
        self.high: pd.Series = df["High"].astype(float)
        self.low: pd.Series = df["Low"].astype(float)
        self.volume: pd.Series = df["Volume"].astype(float)

    def calculate_rsi(self, period: int = 14) -> pd.Series:
        """
        Relative Strength Index (RSI).
        Above 70 = Overbought, Below 30 = Oversold.
        """
        try:
            delta  = self.close.diff()
            gain   = delta.clip(lower=0)
            loss   = -delta.clip(upper=0)
            avg_gain = gain.ewm(com=period - 1, min_periods=period).mean()
            avg_loss = loss.ewm(com=period - 1, min_periods=period).mean()
            rs  = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            return rsi.round(2)
        except Exception:
            return pd.Series(dtype=float)

    def calculate_macd(
        self,
        fast: int = 12,
        slow: int = 26,
        signal: int = 9
    ) -> dict:
        """
        MACD — Moving Average Convergence Divergence.
        Returns macd line, signal line, and histogram.
        """
        try:
            ema_fast   = self.close.ewm(span=fast,   adjust=False).mean()
            ema_slow   = self.close.ewm(span=slow,   adjust=False).mean()
            macd_line  = ema_fast - ema_slow
            signal_line = macd_line.ewm(span=signal, adjust=False).mean()
            histogram  = macd_line - signal_line

            return {
                "macd":      macd_line.round(4),
                "signal":    signal_line.round(4),
                "histogram": histogram.round(4),
            }
        except Exception:
            return {"macd": pd.Series(dtype=float),
                    "signal": pd.Series(dtype=float),
                    "histogram": pd.Series(dtype=float)}

    def calculate_bollinger(self, period: int = 20) -> dict:
        """
        Bollinger Bands.
        Upper/Lower bands = mean ± 2 standard deviations.
        """
        try:
            sma   = self.close.rolling(window=period).mean()
            std   = self.close.rolling(window=period).std()
            upper = sma + (2 * std)
            lower = sma - (2 * std)
            pct_b = (self.close - lower) / (upper - lower)

            return {
                "upper":  upper.round(4),
                "middle": sma.round(4),
                "lower":  lower.round(4),
                "pct_b":  pct_b.round(4),
            }
        except Exception:
            return {}

    def calculate_volatility(self, period: int = 20) -> pd.Series:
        """
        Rolling volatility — standard deviation of
        daily returns over a given period.
        """
        try:
            returns    = self.close.pct_change()
            volatility = returns.rolling(window=period).std() * np.sqrt(252)
            return volatility.round(4)
        except Exception:
            return pd.Series(dtype=float)

    def calculate_volume_ratio(self) -> float:
        """
        Latest volume vs 30-day average.
        Ratio > 1.2 means elevated activity.
        """
        try:
            avg = float(self.volume.mean())
            latest = float(self.volume.iloc[-1])
            return round(latest / avg, 2) if avg else 1.0
        except Exception:
            return 1.0

    def calculate_atr(self, period: int = 14) -> pd.Series:
        """
        Average True Range — measures market volatility.
        Higher ATR = more volatile price movement.
        """
        try:
            high_low   = self.high - self.low
            high_close = (self.high - self.close.shift()).abs()
            low_close  = (self.low  - self.close.shift()).abs()
            true_range = pd.concat(
                [high_low, high_close, low_close], axis=1
            ).max(axis=1)
            atr = true_range.ewm(span=period, adjust=False).mean()
            return atr.round(4)
        except Exception:
            return pd.Series(dtype=float)

    def get_rsi_signal(self) -> str:
        """Return human-readable RSI signal."""
        try:
            rsi = self.calculate_rsi()
            latest = float(rsi.dropna().iloc[-1])
            if latest >= 70:
                return f"OVERBOUGHT ({latest:.1f})"
            elif latest <= 30:
                return f"OVERSOLD ({latest:.1f})"
            return f"NEUTRAL ({latest:.1f})"
        except Exception:
            return "N/A"

    def get_macd_signal(self) -> str:
        """Return human-readable MACD signal."""
        try:
            macd = self.calculate_macd()
            latest_macd   = float(macd["macd"].dropna().iloc[-1])
            latest_signal = float(macd["signal"].dropna().iloc[-1])
            if latest_macd > latest_signal:
                return "BULLISH CROSSOVER"
            return "BEARISH CROSSOVER"
        except Exception:
            return "N/A"

    def get_all_indicators(self) -> dict:
        """
        Master method — returns all indicators in one call.
        Used by health_score.py and ui/charts.py.
        """
        rsi  = self.calculate_rsi()
        macd = self.calculate_macd()
        boll = self.calculate_bollinger()
        vol  = self.calculate_volatility()
        atr  = self.calculate_atr()

        latest_rsi = float(rsi.dropna().iloc[-1])  if not rsi.empty  else None
        latest_vol = float(vol.dropna().iloc[-1])  if not vol.empty  else None
        latest_atr = float(atr.dropna().iloc[-1])  if not atr.empty  else None

        return {
            "rsi":          rsi,
            "macd":         macd,
            "bollinger":    boll,
            "volatility":   vol,
            "atr":          atr,
            "volume_ratio": self.calculate_volume_ratio(),
            "latest_rsi":   latest_rsi,
            "latest_vol":   latest_vol,
            "latest_atr":   latest_atr,
            "rsi_signal":   self.get_rsi_signal(),
            "macd_signal":  self.get_macd_signal(),
        }
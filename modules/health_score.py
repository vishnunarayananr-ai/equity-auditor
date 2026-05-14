# modules/health_score.py
# Responsible for calculating overall company health score (%)
# Single responsibility: HEALTH SCORE ONLY — no fetching, no UI

from utils.helpers import safe_divide
import pandas as pd

class HealthScoreModule:
    """
    Calculates overall company health as a percentage (0-100%).
    Combines price, technical, financial, and sentiment signals.
    Single responsibility: HEALTH SCORING ONLY.
    """

    # Weight of each component in final score (must add to 100)
    WEIGHTS = {
        "price_momentum": 20,
        "rsi":            15,
        "volume":         10,
        "financials":     25,
        "sentiment":      15,
        "rag":            15,
    }

    def __init__(
        self,
        price_data:     pd.DataFrame,  # pd.DataFrame from DataAgent
        indicators:     dict,    # from IndicatorModule.get_all_indicators()
        financials:     dict,    # from DataAgent.fetch_financials()
        sentiment_score: float,  # from SentimentAgent.get_sentiment_score_0_100()
        rag_score:      float,   # from RAGAgent.get_rag_score_0_100()
    ):
        self.price_data      = price_data
        self.indicators      = indicators
        self.financials      = financials
        self.sentiment_score = sentiment_score
        self.rag_score       = rag_score

    # ── Individual Scorers (each returns 0–100) ───────────────────────

    def score_price_momentum(self) -> float:
        """Score based on 1-month price performance."""
        try:
            close_values = pd.Series(self.price_data["Close"])
            close_values = pd.to_numeric(close_values, errors="coerce").dropna()
            if len(close_values) < 2:
                return 50.0

            start = float(close_values.iloc[0])
            end   = float(close_values.iloc[-1])
            pct   = safe_divide(end - start, start) * 100

            if pct >= 20:   return 100.0
            elif pct >= 10: return 85.0
            elif pct >= 5:  return 70.0
            elif pct >= 0:  return 55.0
            elif pct >= -5: return 40.0
            elif pct >= -10: return 25.0
            return 10.0
        except Exception:
            return 50.0

    def score_rsi(self) -> float:
        """
        Score RSI — ideal RSI is between 40-60 (healthy momentum).
        Too high (>70) or too low (<30) reduces score.
        """
        try:
            rsi = self.indicators.get("latest_rsi")
            if rsi is None:
                return 50.0
            if 40 <= rsi <= 60:   return 100.0
            elif 30 <= rsi < 40:  return 75.0
            elif 60 < rsi <= 70:  return 75.0
            elif 20 <= rsi < 30:  return 40.0
            elif 70 < rsi <= 80:  return 40.0
            return 20.0
        except Exception:
            return 50.0

    def score_volume(self) -> float:
        """Score based on volume ratio vs 30-day average."""
        try:
            ratio = self.indicators.get("volume_ratio", 1.0)
            if 0.8 <= ratio <= 1.5:   return 80.0
            elif ratio > 1.5:         return 100.0
            return 50.0
        except Exception:
            return 50.0

    def score_financials(self) -> float:
        """
        Score based on profit margin and debt-to-equity.
        Strong financials = high score.
        """
        try:
            scores = []

            # Profit margin scoring
            margin = self.financials.get("profit_margin")
            if margin is not None:
                if margin >= 20:        scores.append(100.0)
                elif margin >= 10:      scores.append(80.0)
                elif margin >= 5:       scores.append(60.0)
                elif margin >= 0:       scores.append(40.0)
                else:                   scores.append(10.0)

            # Debt-to-equity scoring
            dte = self.financials.get("debt_to_equity")
            if dte is not None:
                if dte <= 0.5:          scores.append(100.0)
                elif dte <= 1.0:        scores.append(80.0)
                elif dte <= 2.0:        scores.append(60.0)
                elif dte <= 3.0:        scores.append(40.0)
                else:                   scores.append(20.0)

            # Free cash flow scoring
            fcf = self.financials.get("free_cashflow")
            if fcf is not None:
                if fcf > 0:             scores.append(80.0)
                else:                   scores.append(20.0)

            return round(sum(scores) / len(scores), 2) if scores else 50.0
        except Exception:
            return 50.0

    # ── Master Health Calculator ──────────────────────────────────────

    def calculate_health(self) -> float:
        """
        Weighted average of all component scores.
        Returns final health percentage (0-100%).
        """
        scores = {
            "price_momentum": self.score_price_momentum(),
            "rsi":            self.score_rsi(),
            "volume":         self.score_volume(),
            "financials":     self.score_financials(),
            "sentiment":      self.sentiment_score,
            "rag":            self.rag_score,
        }

        total_weight = sum(self.WEIGHTS.values())
        weighted_sum = sum(
            scores[k] * self.WEIGHTS[k]
            for k in scores
        )

        return round(weighted_sum / total_weight, 2)

    def get_health_label(self, score: float) -> dict:
        """Convert health % into label and color."""
        if score >= 80:
            return {"label": "EXCELLENT",  "color": "#3fb950"}
        elif score >= 65:
            return {"label": "GOOD",       "color": "#58a6ff"}
        elif score >= 50:
            return {"label": "MODERATE",   "color": "#d29922"}
        elif score >= 35:
            return {"label": "WEAK",       "color": "#f0883e"}
        return {"label": "POOR",           "color": "#f85149"}

    def get_pros_cons(self, score: float) -> dict:
        """
        Generate Pros and Cons list based on
        individual component scores.
        """
        pros = []
        cons = []

        # Price momentum
        p = self.score_price_momentum()
        if p >= 70:
            pros.append("✅ Strong positive price momentum")
        elif p <= 30:
            cons.append("❌ Negative price momentum recently")

        # RSI
        r = self.score_rsi()
        rsi_val = self.indicators.get("latest_rsi", 50)
        if r >= 75:
            pros.append(f"✅ RSI at healthy level ({rsi_val:.1f})")
        elif rsi_val > 70:
            cons.append(f"⚠️ RSI overbought — possible pullback ({rsi_val:.1f})")
        elif rsi_val < 30:
            cons.append(f"⚠️ RSI oversold — high downside risk ({rsi_val:.1f})")

        # Financials
        margin = self.financials.get("profit_margin")
        if margin is not None:
            if margin >= 10:
                pros.append(f"✅ Strong profit margin ({margin:.1f}%)")
            elif margin < 0:
                cons.append(f"❌ Company operating at a loss ({margin:.1f}%)")

        fcf = self.financials.get("free_cashflow")
        if fcf is not None:
            if fcf > 0:
                pros.append("✅ Positive free cash flow")
            else:
                cons.append("❌ Negative free cash flow")

        dte = self.financials.get("debt_to_equity")
        if dte is not None:
            if dte <= 1.0:
                pros.append(f"✅ Low debt-to-equity ratio ({dte:.2f})")
            elif dte > 2.0:
                cons.append(f"❌ High debt-to-equity ratio ({dte:.2f})")

        # Sentiment
        if self.sentiment_score >= 65:
            pros.append("✅ Positive news sentiment")
        elif self.sentiment_score <= 35:
            cons.append("❌ Negative news sentiment")

        # RAG
        if self.rag_score >= 65:
            pros.append("✅ Strategic outlook looks positive")
        elif self.rag_score <= 35:
            cons.append("❌ Strategic signals show risk")

        # Fallbacks
        if not pros:
            pros.append("⚠️ No strong positive signals detected")
        if not cons:
            cons.append("⚠️ No major risk signals detected")

        return {"pros": pros, "cons": cons}

    def get_full_report(self) -> dict:
        """
        Master method — returns everything in one call.
        Used directly by main.py.
        """
        score  = self.calculate_health()
        label  = self.get_health_label(score)
        pc     = self.get_pros_cons(score)

        return {
            "score":        score,
            "label":        label["label"],
            "color":        label["color"],
            "pros":         pc["pros"],
            "cons":         pc["cons"],
            "breakdown": {
                "Price Momentum": self.score_price_momentum(),
                "RSI Health":     self.score_rsi(),
                "Volume":         self.score_volume(),
                "Financials":     self.score_financials(),
                "Sentiment":      self.sentiment_score,
                "RAG Signals":    self.rag_score,
            }
        }
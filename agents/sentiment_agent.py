# agents/sentiment_agent.py
# Responsible for ALL sentiment analysis on news headlines
# Single responsibility: SENTIMENT ONLY — no fetching, no UI

from textblob import TextBlob

class SentimentAgent:
    """
    Analyses sentiment of news headlines using TextBlob.
    Single responsibility: SENTIMENT ANALYSIS ONLY.
    """

    def __init__(self, headlines: list):
        self.headlines = headlines

    def analyse_headline(self, headline: str) -> dict:
        """Analyse a single headline and return score + label."""
        try:
            analysis = TextBlob(headline)
            score = analysis.sentiment.polarity  # type: ignore[attr-defined]

            if score > 0.1:
                label = "POSITIVE"
                color = "#3fb950"
            elif score < -0.1:
                label = "NEGATIVE"
                color = "#f85149"
            else:
                label = "NEUTRAL"
                color = "#d29922"

            return {
                "headline": headline,
                "score":    round(score, 3),
                "label":    label,
                "color":    color,
            }
        except Exception:
            return {
                "headline": headline,
                "score":    0.0,
                "label":    "NEUTRAL",
                "color":    "#d29922",
            }

    def analyse_all(self) -> list:
        """Analyse all headlines and return list of results."""
        return [self.analyse_headline(h) for h in self.headlines]

    def get_average_score(self) -> float:
        """Return average sentiment score across all headlines."""
        results = self.analyse_all()
        if not results:
            return 0.0
        total = sum(r["score"] for r in results)
        return round(total / len(results), 3)

    def get_overall_label(self) -> str:
        """Return overall sentiment label based on average score."""
        avg = self.get_average_score()
        if avg > 0.1:
            return "POSITIVE"
        elif avg < -0.1:
            return "NEGATIVE"
        return "NEUTRAL"

    def get_sentiment_score_0_100(self) -> float:
        """
        Convert average polarity (-1 to 1) into
        a 0-100 scale for use in health score.
        """
        avg = self.get_average_score()
        return round((avg + 1) / 2 * 100, 2)

    def get_summary(self) -> dict:
        """Return full sentiment summary in one call."""
        results  = self.analyse_all()
        avg      = self.get_average_score()
        label    = self.get_overall_label()
        score    = self.get_sentiment_score_0_100()

        positive = sum(1 for r in results if r["label"] == "POSITIVE")
        negative = sum(1 for r in results if r["label"] == "NEGATIVE")
        neutral  = sum(1 for r in results if r["label"] == "NEUTRAL")

        return {
            "results":        results,
            "average_score":  avg,
            "overall_label":  label,
            "score_0_100":    score,
            "positive_count": positive,
            "negative_count": negative,
            "neutral_count":  neutral,
            "total":          len(results),
        }
# agents/rag_agent.py
# Responsible for ALL RAG pipeline operations
# Single responsibility: RAG ONLY — no fetching, no UI, no sentiment

from sentence_transformers import SentenceTransformer, util

class RAGAgent:
    """
    Retrieval-Augmented Generation pipeline.
    Embeds headlines and finds most relevant ones
    for each strategic category using semantic search.
    Single responsibility: RAG PIPELINE ONLY.
    """

    MODEL_NAME = "all-MiniLM-L6-v2"

    CATEGORIES = {
        "Financial Health": "indicators of debt, cash flow, stability, or earnings health",
        "Revenue & Growth": "sales performance, market share growth, and revenue projections",
        "Risk Assessment":  "lawsuits, regulatory issues, competition, or safety concerns",
        "Future Outlook":   "upcoming product launches, catalysts, and strategic guidance",
    }

    CATEGORY_ICONS = {
        "Financial Health": "💰",
        "Revenue & Growth": "📈",
        "Risk Assessment":  "⚠️",
        "Future Outlook":   "🔭",
    }

    SIGNAL_COLORS = {
        "CRITICAL": "#f85149",
        "NOTABLE":  "#d29922",
        "STABLE":   "#3fb950",
    }

    def __init__(self, headlines: list):
        self.headlines  = headlines
        self.model      = self._load_model()
        self.embeddings = self._embed_headlines()

    def _load_model(self) -> SentenceTransformer:
        """Load the SentenceTransformer model."""
        return SentenceTransformer(self.MODEL_NAME)

    def _embed_headlines(self):
        """Convert all headlines into vector embeddings."""
        if not self.headlines:
            return None
        return self.model.encode(self.headlines, convert_to_tensor=True)

    def _get_signal(self, score: float) -> str:
        """Convert relevance score into signal label."""
        if score > 0.45:
            return "CRITICAL"
        elif score > 0.30:
            return "NOTABLE"
        return "STABLE"

    def search(self, query: str) -> dict:
        """
        Search headlines for most relevant match
        to a given query using cosine similarity.
        """
        if self.embeddings is None:
            return {}

        query_embedding = self.model.encode(query, convert_to_tensor=True)
        hits = util.semantic_search(query_embedding, self.embeddings, top_k=1)

        best = hits[0][0]
        corpus_id = int(best["corpus_id"])
        headline = self.headlines[corpus_id]
        score = float(best["score"])
        signal = self._get_signal(score)

        return {
            "headline": headline,
            "score":    round(score, 3),
            "signal":   signal,
            "color":    self.SIGNAL_COLORS[signal],
        }

    def run_full_pipeline(self) -> list:
        """
        Run RAG across all 4 strategic categories.
        Returns list of findings with signal, score, headline.
        """
        findings = []

        for category, query in self.CATEGORIES.items():
            result = self.search(query)

            if not result:
                continue

            signal   = result["signal"]
            headline = result["headline"]
            score    = result["score"]

            if signal == "CRITICAL":
                summary = f"CRITICAL: {headline}"
            elif signal == "NOTABLE":
                summary = f"NOTABLE: {headline}"
            else:
                summary = f"STABLE: No major signal detected. Reference: {headline}"

            findings.append({
                "category": category,
                "icon":     self.CATEGORY_ICONS[category],
                "signal":   signal,
                "color":    result["color"],
                "headline": headline,
                "summary":  summary,
                "score":    score,
            })

        return findings

    def get_rag_score_0_100(self) -> float:
        """
        Convert RAG signals into a 0-100 score
        for use in the health score module.
        CRITICAL = 30, NOTABLE = 60, STABLE = 90
        """
        findings = self.run_full_pipeline()
        if not findings:
            return 50.0

        signal_scores = {"CRITICAL": 30, "NOTABLE": 60, "STABLE": 90}
        total = sum(signal_scores.get(f["signal"], 50) for f in findings)
        return round(total / len(findings), 2)
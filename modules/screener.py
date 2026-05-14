# modules/screener.py
# Responsible for filtering and ranking companies by market cap
# Single responsibility: SCREENING ONLY — no UI, no charts

import yfinance as yf
from utils.helpers import format_market_cap

# ── Predefined Company Lists ──────────────────────────────────────────

MAGNIFICENT_SEVEN = [
    "AAPL",   # Apple
    "MSFT",   # Microsoft
    "GOOGL",  # Alphabet
    "AMZN",   # Amazon
    "NVDA",   # NVIDIA
    "META",   # Meta
    "TSLA",   # Tesla
]

LARGE_CAP_CANDIDATES = [
    "BRK-B", "LLY",  "JPM",  "V",    "UNH",
    "XOM",   "MA",   "JNJ",  "PG",   "HD",
    "AVGO",  "MRK",  "COST", "ABBV", "CVX",
    "KO",    "PEP",  "BAC",  "WMT",  "MCD",
]

MID_CAP_CANDIDATES = [
    "NOW",  "SNOW", "UBER", "SQ",   "SHOP",
    "COIN", "RBLX", "DDOG", "ZS",   "NET",
    "CRWD", "MDB",  "TEAM", "OKTA", "ZM",
    "LYFT", "PINS", "SNAP", "TWLO", "U",
]

SMALL_CAP_CANDIDATES = [
    "IONQ",  "RXRX",  "ARKG", "ARKK", "BTBT",
    "CIFR",  "MARA",  "RIOT", "HUT",  "BITF",
    "SEER",  "OUST",  "LIDR", "AEVA", "INVZ",
    "ASTS",  "LUNR",  "RDW",  "SPIR", "MNTS",
]


class ScreenerModule:
    """
    Filters and ranks companies by market cap tier.
    Single responsibility: SCREENING ONLY.
    """

    def _fetch_company_data(self, ticker: str) -> dict:
        """
        Fetch basic data for a single company.
        Returns dict with ticker, name, market cap, score.
        """
        try:
            info = yf.Ticker(ticker).info
            market_cap  = info.get("marketCap",    None)
            name        = info.get("shortName",     ticker)
            sector      = info.get("sector",        "—")
            pe          = info.get("trailingPE",    None)
            beta        = info.get("beta",          None)
            volume      = info.get("averageVolume", None)
            price       = info.get("currentPrice",  None) or info.get("regularMarketPrice", None)

            if not market_cap:
                return {}

            # Simple ranking score based on available data
            score = 0.0
            if market_cap:  score += 40.0
            if pe and 0 < pe < 40: score += 20.0
            if beta and 0.5 < beta < 1.5: score += 20.0
            if volume and volume > 1_000_000: score += 20.0

            return {
                "ticker":       ticker,
                "name":         name,
                "sector":       sector,
                "market_cap":   market_cap,
                "market_cap_fmt": format_market_cap(market_cap),
                "pe_ratio":     round(pe, 2)   if pe   else None,
                "beta":         round(beta, 2) if beta else None,
                "price":        round(price, 2) if price else None,
                "score":        score,
            }
        except Exception:
            return {}

    def _rank(self, companies: list, top_n: int) -> list:
        """Sort companies by score and return top N."""
        valid = [c for c in companies if c]
        ranked = sorted(valid, key=lambda x: x.get("score", 0), reverse=True)
        return ranked[:top_n]

    def get_magnificent_seven(self) -> list:
        """
        Fetch and rank all 7 Magnificent Seven companies.
        Returns all 7 sorted by score.

        Plain English: Gets Apple, Microsoft, Google etc.
        and shows their current data side by side.
        """
        results = [self._fetch_company_data(t) for t in MAGNIFICENT_SEVEN]
        return self._rank(results, 7)

    def get_top_500b_plus(self) -> list:
        """
        Companies with market cap > $500B — Best 5.

        Plain English: Filters only the biggest companies
        in the world and picks the top 5.
        """
        results = []
        for ticker in LARGE_CAP_CANDIDATES:
            data = self._fetch_company_data(ticker)
            if data and data.get("market_cap", 0) > 500_000_000_000:
                results.append(data)
        return self._rank(results, 5)

    def get_top_100_500b(self) -> list:
        """
        Companies with market cap $100B–$500B — Best 7.

        Plain English: Mid-size giants — not the biggest
        but still very large and stable companies.
        """
        results = []
        for ticker in LARGE_CAP_CANDIDATES + MID_CAP_CANDIDATES:
            data = self._fetch_company_data(ticker)
            cap  = data.get("market_cap", 0) if data else 0
            if data and 100_000_000_000 <= cap <= 500_000_000_000:
                results.append(data)
        return self._rank(results, 7)

    def get_top_under_100b(self) -> list:
        """
        Companies with market cap < $100B — Best 10.

        Plain English: Smaller but fast-growing companies
        with high potential for returns.
        """
        results = []
        for ticker in MID_CAP_CANDIDATES + SMALL_CAP_CANDIDATES:
            data = self._fetch_company_data(ticker)
            cap  = data.get("market_cap", 0) if data else 0
            if data and 0 < cap < 100_000_000_000:
                results.append(data)
        return self._rank(results, 10)

    def get_all_tiers(self) -> dict:
        """
        Master method — returns all 4 tiers in one call.
        Used directly by main.py.
        """
        return {
            "magnificent_seven": self.get_magnificent_seven(),
            "above_500b":        self.get_top_500b_plus(),
            "between_100_500b":  self.get_top_100_500b(),
            "below_100b":        self.get_top_under_100b(),
        }
# agents/data_agent.py
# Responsible for ALL stock market data fetching (live + historical)

import yfinance as yf
import pandas as pd
from utils.helpers import format_market_cap, safe_divide

class DataAgent:
    """
    Fetches live and historical stock data.
    Single responsibility: DATA ONLY — no UI, no analysis.
    """

    def __init__(self, ticker: str):
        self.ticker = ticker.upper().strip()
        self._ticker_obj = yf.Ticker(self.ticker)

    def fetch_price_data(self, period: str = "1mo") -> pd.DataFrame:
        """Fetch OHLCV price data. Period: 1mo, 3mo, 6mo, 1y"""
        try:
            df = self._ticker_obj.history(period=period)
            return df if not df.empty else pd.DataFrame()
        except Exception:
            return pd.DataFrame()

    def fetch_company_info(self) -> dict:
        """Fetch company metadata — name, sector, market cap, PE ratio."""
        try:
            info = self._ticker_obj.info
            market_cap = info.get("marketCap", None)
            return {
                "name":         info.get("shortName", self.ticker),
                "sector":       info.get("sector", "—"),
                "industry":     info.get("industry", "—"),
                "market_cap":   market_cap,
                "market_cap_fmt": format_market_cap(float(market_cap)) if isinstance(market_cap, (int, float)) else None,
                "pe_ratio":     info.get("trailingPE", None),
                "eps":          info.get("trailingEps", None),
                "dividend":     info.get("dividendYield", None),
                "beta":         info.get("beta", None),
                "52w_high":     info.get("fiftyTwoWeekHigh", None),
                "52w_low":      info.get("fiftyTwoWeekLow", None),
                "avg_volume":   info.get("averageVolume", None),
                "employees":    info.get("fullTimeEmployees", None),
                "country":      info.get("country", "—"),
                "website":      info.get("website", "—"),
                "description":  info.get("longBusinessSummary", "—"),
            }
        except Exception:
            return {}

    def fetch_financials(self) -> dict:
        """Fetch revenue, profit, cash flow (annual)."""
        try:
            income   = self._ticker_obj.financials
            cashflow = self._ticker_obj.cashflow
            balance  = self._ticker_obj.balance_sheet

            result = {}

            if income is not None and not income.empty:
                result["total_revenue"]    = income.loc["Total Revenue"].iloc[0]    if "Total Revenue"    in income.index else None
                result["gross_profit"]     = income.loc["Gross Profit"].iloc[0]     if "Gross Profit"     in income.index else None
                result["net_income"]       = income.loc["Net Income"].iloc[0]       if "Net Income"       in income.index else None
                result["operating_income"] = income.loc["Operating Income"].iloc[0] if "Operating Income" in income.index else None

            if cashflow is not None and not cashflow.empty:
                result["free_cashflow"] = cashflow.loc["Free Cash Flow"].iloc[0]      if "Free Cash Flow"      in cashflow.index else None
                result["operating_cf"]  = cashflow.loc["Operating Cash Flow"].iloc[0] if "Operating Cash Flow" in cashflow.index else None

            if balance is not None and not balance.empty:
                result["total_debt"]   = balance.loc["Total Debt"].iloc[0]               if "Total Debt"               in balance.index else None
                result["total_assets"] = balance.loc["Total Assets"].iloc[0]             if "Total Assets"             in balance.index else None
                result["total_equity"] = balance.loc["Stockholders Equity"].iloc[0]      if "Stockholders Equity"      in balance.index else None

            revenue = result.get("total_revenue")
            profit  = result.get("net_income")
            debt    = result.get("total_debt")
            equity  = result.get("total_equity")

            result["profit_margin"]  = safe_divide(profit, revenue) * 100 if profit and revenue else None
            result["debt_to_equity"] = safe_divide(debt, equity)           if debt and equity   else None

            return result
        except Exception:
            return {}

    def fetch_analyst_ratings(self) -> dict:
        """Fetch analyst buy/sell/hold recommendations."""
        try:
            rec = self._ticker_obj.recommendations
            if rec is None or not isinstance(rec, pd.DataFrame) or rec.empty:
                return {}
            latest = rec.iloc[-5:]
            return {
                "strong_buy":  int(latest["strongBuy"].sum())  if "strongBuy"  in latest.columns else 0,
                "buy":         int(latest["buy"].sum())         if "buy"        in latest.columns else 0,
                "hold":        int(latest["hold"].sum())        if "hold"       in latest.columns else 0,
                "sell":        int(latest["sell"].sum())        if "sell"       in latest.columns else 0,
                "strong_sell": int(latest["strongSell"].sum())  if "strongSell" in latest.columns else 0,
            }
        except Exception:
            return {}

    def is_valid(self) -> bool:
        """Check if the ticker returned any usable data."""
        df = self.fetch_price_data()
        return not df.empty
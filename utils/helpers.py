# utils/helpers.py
# Common helper functions used across the entire project

import pandas as pd
from datetime import datetime

def format_currency(value: float) -> str:
    """Format a number as USD currency string."""
    if value is None:
        return "—"
    return f"${value:,.2f}"

def format_market_cap(value: float) -> str:
    """Format market cap into readable B/M/T format."""
    if value is None:
        return "—"
    if value >= 1e12:
        return f"${value / 1e12:.2f}T"
    elif value >= 1e9:
        return f"${value / 1e9:.2f}B"
    elif value >= 1e6:
        return f"${value / 1e6:.2f}M"
    return f"${value:,.0f}"

def format_percentage(value: float) -> str:
    """Format a float as a percentage string."""
    if value is None:
        return "—"
    return f"{value:.2f}%"

def get_change_color(value: float) -> str:
    """Return green or red color based on positive/negative value."""
    return "#3fb950" if value >= 0 else "#f85149"

def get_arrow(value: float) -> str:
    """Return up or down arrow based on value."""
    return "▲" if value >= 0 else "▼"

def safe_divide(a: float, b: float, fallback: float = 0.0) -> float:
    """Safe division that returns fallback if b is zero."""
    try:
        return a / b if b != 0 else fallback
    except Exception:
        return fallback

def timestamp_now() -> str:
    """Return current timestamp as readable string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
from __future__ import annotations

from typing import Any, Dict

import pandas as pd

LOW_REVENUE_THRESHOLD = 50


def recommend_action(row: pd.Series | Dict[str, Any]) -> Dict[str, Any]:
    recency = float(row.get("recency", 0))
    support_tickets = float(row.get("support_tickets", row.get("support_rate", 0)))
    revenue_bin = row.get("revenue_bin", 0)
    revenue_low = isinstance(revenue_bin, (int, float)) and revenue_bin == 0

    if recency > 45:
        return {"priority": "high", "action": "Send reactivation campaign with incentive", "reason": "High inactivity"}
    if support_tickets > 3:
        return {"priority": "high", "action": "Escalate to success manager", "reason": "Multiple support tickets"}
    if revenue_low:
        return {"priority": "medium", "action": "Offer discount bundle", "reason": "Low revenue segment"}
    return {"priority": "low", "action": "Use LLM suggestion", "reason": "No strong rule trigger"}


from __future__ import annotations

import os
from typing import Any, Dict, List

try:
    from openai import OpenAI
except Exception:  # pragma: no cover
    OpenAI = None  # type: ignore

SYSTEM_PROMPT = """
You are a churn analyst. Given churn probability and top feature drivers, explain why a user may churn and propose a concise retention action.
""".strip()

USER_TEMPLATE = """
User {{user_id}} has churn probability {{churn_prob}}.
Drivers: {{top_drivers}}
Suggest one concrete action.
""".strip()

FEW_SHOTS = [
    {
        "role": "user",
        "content": "User 101 has churn probability 0.82. Drivers: recency=60, session_rate=0.2, support_rate=0.05, revenue_bin=0. Suggest one concrete action.",
    },
    {
        "role": "assistant",
        "content": "User 101 shows high churn risk due to long inactivity and low engagement. Offer a reactivation email with a limited-time discount and in-app tips to restart usage.",
    },
    {
        "role": "user",
        "content": "User 202 has churn probability 0.35. Drivers: recency=10, session_rate=1.5, support_rate=0.0, revenue_bin=2. Suggest one concrete action.",
    },
    {
        "role": "assistant",
        "content": "Moderate risk mainly from recent inactivity. Send a personalized nudge highlighting new features and invite feedback.",
    },
]


def render_template(template: str, **kwargs) -> str:
    out = template
    for k, v in kwargs.items():
        out = out.replace(f"{{{{{k}}}}}", str(v))
    return out


def build_llm_payload(user_id: Any, churn_prob: float, top_drivers: Dict[str, Any], action: Dict[str, Any]):
    return {
        "user_id": user_id,
        "churn_prob": round(float(churn_prob), 4),
        "top_drivers": top_drivers,
        "recommended_action": action,
    }


def call_llm(user_id: Any, churn_prob: float, top_drivers: Dict[str, Any], action: Dict[str, Any]) -> Dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or OpenAI is None:
        return build_llm_payload(user_id, churn_prob, top_drivers, action)

    client = OpenAI(api_key=api_key)
    user_msg = render_template(USER_TEMPLATE, user_id=user_id, churn_prob=round(churn_prob, 3), top_drivers=top_drivers)
    messages: List[Dict[str, str]] = [{"role": "system", "content": SYSTEM_PROMPT}] + FEW_SHOTS + [{"role": "user", "content": user_msg}]
    resp = client.chat.completions.create(model="gpt-4o-mini", messages=messages, temperature=0.3)
    content = resp.choices[0].message.content
    return {
        "user_id": user_id,
        "churn_prob": round(float(churn_prob), 4),
        "top_drivers": top_drivers,
        "recommended_action": action,
        "llm_explanation": content,
    }


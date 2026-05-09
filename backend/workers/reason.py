import json

import anthropic

from app.config import get_settings

settings = get_settings()

SYSTEM_PROMPT = """You are Signal, an AI product intelligence analyst.
Your job is to read clusters of support tickets and identify the most important product insights for a product manager.

Rules:
- Surface 3 to 5 insights maximum. Fewer strong insights beat many weak ones.
- Every insight must be grounded in the ticket data provided. No speculation.
- Express uncertainty honestly using the confidence score (0.0–1.0).
- suggested_action must be concrete and actionable, not generic advice.
- evidence must cite real source_ids from the data you were given.

Respond with valid JSON only. No prose, no markdown fences."""

INSIGHT_SCHEMA = """
{
  "insights": [
    {
      "rank": 1,
      "category": "one of: recurring_pain | feature_gap | onboarding_friction | reliability_issue | workflow_blocker | churn_signal",
      "title": "Short title (max 10 words)",
      "explanation": "2-3 sentences explaining the pattern and why it matters to the product team",
      "suggested_action": "One concrete, specific action the PM should take — not generic advice",
      "confidence": 0.85,
      "affected_count": 12,
      "evidence": [
        {
          "source_id": "ticket id from the data",
          "excerpt": "short verbatim quote from the ticket",
          "url": "ticket url"
        }
      ]
    }
  ]
}"""


def generate_insights(cluster_summaries: list[dict], period_start: str, period_end: str) -> list[dict]:
    """
    Call Claude with cluster summaries and return structured insights.
    Uses prompt caching on the cluster data (large, static context).
    """
    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    cluster_text = json.dumps(cluster_summaries, indent=2)

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            f"Here are support ticket clusters from {period_start} to {period_end}.\n\n"
                            f"{cluster_text}"
                        ),
                        # Cache the cluster data — it's the expensive part
                        "cache_control": {"type": "ephemeral"},
                    },
                    {
                        "type": "text",
                        "text": f"Generate insights following this exact JSON schema:\n{INSIGHT_SCHEMA}",
                    },
                ],
            }
        ],
    )

    raw = response.content[0].text.strip()
    data = json.loads(raw)
    return data.get("insights", [])

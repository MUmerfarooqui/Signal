"""
Seed mock data for a given org (idempotent — safe to run multiple times).

Skips briefs if any already exist for the org.
Skips pulse items if any already exist for the org.

Usage:
    python seed.py                  # seeds first org found
    python seed.py <org_id>         # seeds specific org
    python seed.py --reset          # wipe existing seed data and re-seed (first org)
    python seed.py <org_id> --reset # wipe and re-seed for specific org
"""

import sys
import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import delete, func, select

from app.db.session import SessionLocal
from app.models.brief import Brief
from app.models.evidence_ref import EvidenceRef
from app.models.insight import Insight
from app.models.insight_feed_item import InsightFeedItem
from app.models.organization import Organization

# --------------------------------------------------------------------------- #
# Mock data                                                                    #
# --------------------------------------------------------------------------- #

PULSE_ITEMS = [
    {
        "signal_type": "spike",
        "category": "recurring_pain",
        "title": "Users unable to complete checkout on mobile Safari",
        "description": "14 tickets on this topic in the last 24 hours — 3.2× your daily average.",
        "severity": "high",
        "ticket_count": 14,
        "hours_ago": 2,
    },
    {
        "signal_type": "spike",
        "category": "reliability_issue",
        "title": "API returning 503 errors on data export endpoint",
        "description": "9 tickets on this topic in the last 24 hours — 2.1× your daily average.",
        "severity": "high",
        "ticket_count": 9,
        "hours_ago": 5,
    },
    {
        "signal_type": "spike",
        "category": "feature_gap",
        "title": "Customers asking for two-factor authentication support",
        "description": "7 tickets on this topic in the last 24 hours — 1.8× your daily average.",
        "severity": "medium",
        "ticket_count": 7,
        "hours_ago": 8,
    },
    {
        "signal_type": "spike",
        "category": "onboarding_friction",
        "title": "New users confused by workspace vs project distinction",
        "description": "5 tickets on this topic in the last 24 hours — 1.6× your daily average.",
        "severity": "medium",
        "ticket_count": 5,
        "hours_ago": 14,
    },
    {
        "signal_type": "spike",
        "category": "workflow_blocker",
        "title": "Calendar sync not reflecting recent changes",
        "description": "4 tickets on this topic in the last 24 hours — 1.5× your daily average.",
        "severity": "low",
        "ticket_count": 4,
        "hours_ago": 20,
    },
]

BRIEFS = [
    {
        "weeks_ago": 1,
        "insights": [
            {
                "rank": 1,
                "category": "recurring_pain",
                "title": "Password reset emails not arriving",
                "explanation": (
                    "47 tickets over the past 7 days report that password reset emails are "
                    "either not received or arrive after a 20–30 minute delay. The pattern "
                    "is concentrated on Gmail addresses and appears to have started after "
                    "the May 2nd infrastructure migration. Users are unable to self-serve "
                    "account recovery, driving repeat contacts to support."
                ),
                "suggested_action": (
                    "Audit email delivery logs for Gmail-specific SMTP rejections or spam "
                    "filtering. Check SPF/DKIM records post-migration. Target fix within 48h "
                    "given support volume impact."
                ),
                "confidence": 0.94,
                "affected_count": 47,
                "evidence": [
                    {
                        "excerpt": "I've been waiting 45 minutes for the reset email. Checked spam, nothing there. This is really frustrating.",
                        "url": "https://yourcompany.zendesk.com/tickets/10482",
                    },
                    {
                        "excerpt": "Password reset is broken for me too. Gmail account. Tried 3 times.",
                        "url": "https://yourcompany.zendesk.com/tickets/10491",
                    },
                    {
                        "excerpt": "Reset email arrived 25 minutes late. By then the link had expired. Needed to start over.",
                        "url": "https://yourcompany.zendesk.com/tickets/10504",
                    },
                ],
            },
            {
                "rank": 2,
                "category": "feature_gap",
                "title": "No bulk export for reports",
                "explanation": (
                    "22 tickets this week request the ability to export report data in bulk — "
                    "either as CSV or PDF. Current export functionality is limited to single "
                    "records. Enterprise customers are citing this as a blocker for their "
                    "internal reporting workflows and weekly executive reviews. Two accounts "
                    "explicitly mentioned evaluating alternatives."
                ),
                "suggested_action": (
                    "Prioritise bulk CSV export for the reports module. Start with the most "
                    "requested report type (usage summary based on ticket language). "
                    "Validate scope with the two at-risk enterprise accounts before scoping."
                ),
                "confidence": 0.87,
                "affected_count": 22,
                "evidence": [
                    {
                        "excerpt": "We need to export our monthly usage data for finance. Doing it one by one takes hours. Is bulk export on the roadmap?",
                        "url": "https://yourcompany.zendesk.com/tickets/10467",
                    },
                    {
                        "excerpt": "Our VP asks for a weekly report every Friday. I have to manually compile this. A CSV export would save me 2 hours a week.",
                        "url": "https://yourcompany.zendesk.com/tickets/10471",
                    },
                ],
            },
            {
                "rank": 3,
                "category": "onboarding_friction",
                "title": "Team invite flow confusing for new admins",
                "explanation": (
                    "18 tickets from new account admins in their first week describe confusion "
                    "around inviting team members. The most common issue is that the invite "
                    "button is only visible after navigating to Settings > Team, which is not "
                    "surfaced during onboarding. Several users assumed the feature didn't exist."
                ),
                "suggested_action": (
                    "Add a 'Invite your team' prompt to the onboarding checklist and to the "
                    "empty state of the Members page. Consider a tooltip on first login for "
                    "admin-role users pointing directly to team settings."
                ),
                "confidence": 0.82,
                "affected_count": 18,
                "evidence": [
                    {
                        "excerpt": "How do I add other users to my account? I can't find it anywhere on the dashboard.",
                        "url": "https://yourcompany.zendesk.com/tickets/10453",
                    },
                    {
                        "excerpt": "Spent 20 minutes looking for the invite link. Eventually found it buried in Settings. Would be good to make it more obvious.",
                        "url": "https://yourcompany.zendesk.com/tickets/10461",
                    },
                ],
            },
            {
                "rank": 4,
                "category": "reliability_issue",
                "title": "Dashboard loading slowly on large datasets",
                "explanation": (
                    "12 tickets from customers with over 10,000 records report the main "
                    "dashboard taking 8–15 seconds to load. Smaller accounts are not affected. "
                    "The pattern suggests a missing index or unoptimised query on the data "
                    "aggregation layer rather than a frontend issue."
                ),
                "suggested_action": (
                    "Profile the dashboard aggregation query with a large dataset in staging. "
                    "Check for missing indexes on org_id + created_at. This is likely a "
                    "quick database fix with significant perceived performance improvement for "
                    "high-value enterprise accounts."
                ),
                "confidence": 0.79,
                "affected_count": 12,
                "evidence": [
                    {
                        "excerpt": "The dashboard takes forever to load — sometimes over 10 seconds. We have a lot of data but this seems excessive.",
                        "url": "https://yourcompany.zendesk.com/tickets/10488",
                    },
                ],
            },
        ],
    },
    {
        "weeks_ago": 2,
        "insights": [
            {
                "rank": 1,
                "category": "churn_signal",
                "title": "Enterprise accounts frustrated with SSO limitations",
                "explanation": (
                    "9 tickets from enterprise tier customers over the past two weeks express "
                    "frustration that SSO is available but does not support SCIM provisioning. "
                    "Without SCIM, IT teams must manually manage user lifecycle (onboarding, "
                    "offboarding). Three customers have linked this gap directly to an internal "
                    "IT policy that would block continued use without automated provisioning."
                ),
                "suggested_action": (
                    "Treat SCIM provisioning as a high-priority enterprise feature. Engage "
                    "the three at-risk accounts directly to understand their deadline. Even a "
                    "basic SCIM implementation (create, deactivate users) would unblock them."
                ),
                "confidence": 0.91,
                "affected_count": 9,
                "evidence": [
                    {
                        "excerpt": "We need SCIM support. Our IT policy requires automated provisioning for all SaaS tools with more than 50 users.",
                        "url": "https://yourcompany.zendesk.com/tickets/10380",
                    },
                    {
                        "excerpt": "Love the product but SCIM is a blocker for us expanding the rollout. Is this on the roadmap for this year?",
                        "url": "https://yourcompany.zendesk.com/tickets/10392",
                    },
                ],
            },
            {
                "rank": 2,
                "category": "workflow_blocker",
                "title": "Mobile app missing key actions available on web",
                "explanation": (
                    "31 tickets this period reference missing functionality on the mobile app. "
                    "The top missing actions are: creating new items (mentioned in 19 tickets), "
                    "editing existing records (14 tickets), and accessing filters (11 tickets). "
                    "Users describe the mobile app as 'read-only' — useful for checking status "
                    "but not for getting work done on the go."
                ),
                "suggested_action": (
                    "Audit the delta between mobile and web functionality. Prioritise the "
                    "create and edit actions as they block async work from mobile. "
                    "Consider a 'mobile parity' sprint to close the most-cited gaps."
                ),
                "confidence": 0.88,
                "affected_count": 31,
                "evidence": [
                    {
                        "excerpt": "I travel a lot and can't create new projects from the app. Have to wait until I'm back at my laptop. Very limiting.",
                        "url": "https://yourcompany.zendesk.com/tickets/10344",
                    },
                    {
                        "excerpt": "The mobile app feels like a viewer only. I can't edit anything. Please add editing support.",
                        "url": "https://yourcompany.zendesk.com/tickets/10351",
                    },
                    {
                        "excerpt": "Where are the filters on mobile? I use them constantly on desktop but can't find them in the app.",
                        "url": "https://yourcompany.zendesk.com/tickets/10368",
                    },
                ],
            },
            {
                "rank": 3,
                "category": "feature_gap",
                "title": "Users want Slack notifications for key events",
                "explanation": (
                    "27 tickets request Slack integration specifically for notifications — "
                    "when a new item is assigned, a status changes, or a deadline is approaching. "
                    "Users are currently relying on email notifications which are described as "
                    "easy to miss. Slack is mentioned in 24 of 27 tickets; 3 mention Microsoft Teams."
                ),
                "suggested_action": (
                    "Build a Slack notification integration. Start with the three highest-volume "
                    "triggers: assignment, status change, deadline reminder. Use Slack's webhook "
                    "API for a lightweight first version before a full OAuth integration."
                ),
                "confidence": 0.85,
                "affected_count": 27,
                "evidence": [
                    {
                        "excerpt": "Please add Slack notifications. I miss email alerts constantly but I'm always in Slack.",
                        "url": "https://yourcompany.zendesk.com/tickets/10322",
                    },
                    {
                        "excerpt": "Our whole team lives in Slack. Email notifications just don't cut it for time-sensitive updates.",
                        "url": "https://yourcompany.zendesk.com/tickets/10339",
                    },
                ],
            },
        ],
    },
    {
        "weeks_ago": 3,
        "insights": [
            {
                "rank": 1,
                "category": "recurring_pain",
                "title": "File upload fails silently above 50MB",
                "explanation": (
                    "38 tickets over this period describe file uploads appearing to succeed — "
                    "the progress bar completes — but the file not appearing in the system. "
                    "This consistently occurs with files over 50MB. The silent failure means "
                    "users only discover the problem later when the file is missing, often at "
                    "a critical moment. Some users uploaded the same file multiple times before contacting support."
                ),
                "suggested_action": (
                    "Add explicit file size validation before upload begins with a clear error "
                    "message stating the limit. Separately, evaluate whether the 50MB limit is "
                    "appropriate for your user base — 3 tickets mention needing to upload "
                    "video files which regularly exceed this."
                ),
                "confidence": 0.96,
                "affected_count": 38,
                "evidence": [
                    {
                        "excerpt": "Uploaded a file, the bar went to 100%, said complete — but it's not in the system. Tried three times. 68MB PDF.",
                        "url": "https://yourcompany.zendesk.com/tickets/10201",
                    },
                    {
                        "excerpt": "Silent failure on file upload. No error, just disappears. Wasted 30 minutes thinking it was my internet.",
                        "url": "https://yourcompany.zendesk.com/tickets/10218",
                    },
                    {
                        "excerpt": "The upload spinner completes but nothing saves. It's a 75MB file. Is there a size limit I'm not seeing?",
                        "url": "https://yourcompany.zendesk.com/tickets/10234",
                    },
                ],
            },
            {
                "rank": 2,
                "category": "onboarding_friction",
                "title": "Trial users not discovering core feature during setup",
                "explanation": (
                    "Analysis of this week's support tickets from trial-period accounts shows "
                    "that 14 users contacted support asking how to use the automation feature — "
                    "the product's core differentiator. All 14 had been in the product for more "
                    "than 3 days without encountering it. The feature is accessible only from "
                    "a sub-menu that is not referenced in the onboarding flow."
                ),
                "suggested_action": (
                    "Add the automation feature to the onboarding checklist as step 2 or 3. "
                    "Create an empty state on the main dashboard that surfaces it with a "
                    "'Try automations' CTA. Trial conversion likely improves meaningfully if "
                    "users experience the core value in the first session."
                ),
                "confidence": 0.83,
                "affected_count": 14,
                "evidence": [
                    {
                        "excerpt": "I've been using the trial for 4 days and just found out about automations from a YouTube video. Why isn't this front and centre?",
                        "url": "https://yourcompany.zendesk.com/tickets/10255",
                    },
                    {
                        "excerpt": "Can you walk me through the automation feature? I can't figure out where to find it.",
                        "url": "https://yourcompany.zendesk.com/tickets/10263",
                    },
                ],
            },
        ],
    },
]


# --------------------------------------------------------------------------- #
# Seed                                                                         #
# --------------------------------------------------------------------------- #

def reset(org_id: uuid.UUID) -> None:
    """Delete all seeded briefs and pulse items for the org."""
    db = SessionLocal()
    try:
        # Cascade deletes insights + evidence refs via FK ON DELETE CASCADE
        result = db.execute(delete(Brief).where(Brief.org_id == org_id))
        briefs_deleted = result.rowcount
        pulse_result = db.execute(delete(InsightFeedItem).where(InsightFeedItem.org_id == org_id))
        pulse_deleted = pulse_result.rowcount
        db.commit()
        print(f"  reset  — deleted {briefs_deleted} brief(s), {pulse_deleted} pulse item(s)")
    finally:
        db.close()


def seed(org_id: uuid.UUID) -> None:
    db = SessionLocal()
    try:
        org = db.get(Organization, org_id)
        if org is None:
            print(f"  org {org_id} not found.")
            return

        print(f"Org: {org.name} ({org_id})")
        now = datetime.now(timezone.utc)

        # Briefs
        brief_count = db.execute(
            select(func.count(Brief.id)).where(Brief.org_id == org_id)
        ).scalar_one()

        if brief_count > 0:
            print(f"  briefs — already seeded ({brief_count} found), skipping")
        else:
            for brief_data in BRIEFS:
                period_end = now - timedelta(weeks=brief_data["weeks_ago"] - 1)
                period_start = period_end - timedelta(days=7)

                brief = Brief(
                    org_id=org_id,
                    period_start=period_start,
                    period_end=period_end,
                    status="ready",
                    generated_at=period_end - timedelta(hours=2),
                )
                db.add(brief)
                db.flush()

                for raw in brief_data["insights"]:
                    insight = Insight(
                        brief_id=brief.id,
                        org_id=org_id,
                        rank=raw["rank"],
                        category=raw["category"],
                        title=raw["title"],
                        explanation=raw["explanation"],
                        suggested_action=raw["suggested_action"],
                        confidence=raw["confidence"],
                        affected_count=raw["affected_count"],
                    )
                    db.add(insight)
                    db.flush()

                    for ev in raw.get("evidence", []):
                        db.add(EvidenceRef(
                            insight_id=insight.id,
                            raw_event_id=None,
                            excerpt=ev["excerpt"],
                            url=ev.get("url"),
                            relevance_score=1.0,
                        ))

                n = len(brief_data["insights"])
                print(f"  brief — {brief_data['weeks_ago']} week(s) ago, {n} insights")

            print(f"  briefs — seeded {len(BRIEFS)} briefs")

        # Pulse feed items
        pulse_count = db.execute(
            select(func.count(InsightFeedItem.id)).where(InsightFeedItem.org_id == org_id)
        ).scalar_one()

        if pulse_count > 0:
            print(f"  pulse  — already seeded ({pulse_count} found), skipping")
        else:
            for p in PULSE_ITEMS:
                detected = now - timedelta(hours=p["hours_ago"])
                db.add(InsightFeedItem(
                    org_id=org_id,
                    signal_type=p["signal_type"],
                    category=p["category"],
                    title=p["title"],
                    description=p["description"],
                    severity=p["severity"],
                    ticket_count=p["ticket_count"],
                    detected_at=detected,
                    expires_at=detected + timedelta(days=7),
                ))

            print(f"  pulse  — seeded {len(PULSE_ITEMS)} items")

        db.commit()
        print("Done.")
    finally:
        db.close()


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--reset"]
    do_reset = "--reset" in sys.argv

    db = SessionLocal()
    try:
        if args:
            org_id = uuid.UUID(args[0])
        else:
            row = db.execute(select(Organization)).scalars().first()
            if row is None:
                print("No orgs found. Create an org first via the app.")
                sys.exit(1)
            org_id = row.id
    finally:
        db.close()

    if do_reset:
        reset(org_id)

    seed(org_id)

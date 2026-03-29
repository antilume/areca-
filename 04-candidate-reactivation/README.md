# System 04: Candidate Reactivation System

## 1. Executive Summary
The Candidate Reactivation System (CRS) is designed to maximize the value of the agency's existing database (ATS). It automatically identifies and reaches out to past candidates whose profiles have become "stale" or who might be a fit for new roles, encouraging them to update their information and re-enter the pipeline.

## 2. Problem Statement & Business Context
Recruiters often have thousands of candidates in their ATS who haven't been contacted in months or years. These candidates are "warmer" than cold leads but are often forgotten. CRS solves this by turning a static database into a dynamic, recurring talent pool.

## 3. System Architecture Overview
CRS is an **Automated Outreach Engine** that monitors the job-to-candidate matching results (from System 03) and identifies "past favorites."
- **Staleness Monitor:** Flags profiles with no activity for 6+ months.
- **Outreach Manager:** Manages communication templates and sequences.
- **Profile Updater:** A self-service portal or AI-chat interface for candidates to refresh their skills and status.

## 4. Scraping Layer (Multi-Board) / Data Acquisition
Rather than external boards, CRS "scrapes" internal data:
- **Internal ATS:** Bullhorn, Greenhouse, or proprietary CSV/DB stores.
- **Historical Interaction Data:** Email threads, interview notes, and past "Reason for Rejection."

## 5. Deduplication & Quality Filter Engine
- **Profile Merging:** Ensures that if a candidate reapplies through a different board (System 02), their records are unified.
- **Intent Analysis:** Filters out candidates who previously requested "Do Not Contact" or have moved into unrelated career paths (e.g., from Software Engineer to Bakery Owner).

## 6. Decision-Maker Linking Engine
CRS links reactivated candidates to current hiring managers (from System 01) who have active roles (from System 02). It provides the "context of past success" (e.g., "This candidate made it to the final round at Google last year").

## 7. Data Models & Schema
- `ReactivationCampaign`: (id, job_id, segment_criteria, status, conversion_rate)
- `CandidateTouchpoint`: (id, candidate_id, channel, message_content, response_status, timestamp)
- `StaleProfileFlag`: (candidate_id, last_verified_date, primary_skill_stale_flag)

## 8. Workflow Diagrams (ASCII)
```text
[ Internal DB ] -> [ Staleness Monitor ] -> [ AI Personalizer ] -> [ CRM/Outreach ]
                                                    |
                                            (Candidate Update)
                                                    |
                                            v Golden Profile v
                                                    |
                                            [ Back to System 03 ]
```

## 9. Tech Stack & Tools
- **Engagement:** SendGrid (Email), Twilio (SMS), WhatsApp Business API.
- **Workflow:** Python (Temporal.io for long-running outreach sagas).
- **Profile Updates:** Next.js (for the candidate self-service portal).

## 10. Anti-Bot Evasion Strategy (Evasion & Resilience)
- **Email Deliverability:** Managing SPF, DKIM, and DMARC to ensure outreach doesn't land in spam.
- **Rate-Limited Outreach:** Throttling messages to avoid being flagged by email providers (Gmail/Outlook).
- **Human-Like Delay:** Spacing out SMS/Email sequences.

## 11. Legal & Compliance Considerations
- **GDPR (Right to Access):** Allowing candidates to easily see and edit the data the agency holds on them.
- **Opt-Out (Unsubscribe):** Mandatory, one-click unsubscribe in all reactivation communications.
- **Data Accuracy:** Ensuring the agency doesn't store outdated/incorrect PII for longer than necessary.

## 12. MVP vs. Production Scope
- **MVP:** Manual email templates and simple SQL-based segmenting.
- **Production:** AI-generated personalized outreach, automated SMS sequences, and a self-service profile update portal.

## 13. Error Handling & Resilience
- **Bounce Detection:** Automatically marking emails as "Invalid" if they bounce.
- **Out-of-Office (OOO) Handling:** Retrying the outreach after the OOO date has passed.

## 14. Performance & Scale Targets
- **Reactivation Rate:** > 15% of stale candidates responding or updating their profile.
- **Outreach Volume:** 5,000+ personalized messages per month.
- **Profile Accuracy:** 100% of reactivated profiles updated with current contact info.

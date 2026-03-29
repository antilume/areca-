# System 07: Interview Scheduling Agent

## 1. Executive Summary
The Interview Scheduling Agent (ISA) is a high-reliability orchestration layer that automates the logistics of candidate and client meetings. By syncing with calendars in real-time and providing automated "Magic Booking" links, the ISA eliminates the administrative "ping-pong" that often delays interviews. It ensures a seamless experience for both candidates and clients, accelerating the recruitment cycle and increasing the conversion rate from shortlist to interview.

## 2. Problem Statement & Business Context
Scheduling is cited by recruiters as the single most time-consuming "non-value-add" task. Delays in scheduling (often taking 24-48 hours of back-and-forth) lead to candidate drop-off and lost placements. The ISA solves this by providing a unified, real-time interface to multi-party availability, reducing scheduling time from days to minutes.

## 3. System Architecture Overview
The ISA is a **Multi-Calendar Orchestration Engine**.
- **Unified Calendar API:** A service layer that abstracts integrations with Google Workspace, O365, and iCloud via **Nylas** or **Cronofy**.
- **Conflict Resolution Engine:** A high-concurrency service that computes available slots by aggregating "Free/Busy" data and applying recruiter-defined rules (e.g., "minimum 30-min buffer between interviews").
- **Meeting Provisioner:** Automated creation of video meeting rooms (Zoom, Teams, Google Meet) and physical location instructions.

## 4. Scraping Layer (Multi-Board) / Data Acquisition
The ISA "scrapes" and syncs real-time availability:
- **Calendar Data:** Continuous polling or webhook-based updates of hiring manager and recruiter calendars.
- **Candidate Availability:** An interactive booking portal where candidates provide their availability, which is then stored in a temporary "Availability Buffer" (Redis).

## 5. Deduplication & Quality Filter Engine
- **Conflict Detection:** Real-time checking against the manager's latest calendar state before finalizing a booking (to prevent race conditions).
- **Timezone Normalization:** Every event and slot is stored in UTC with localized "Offset Metadata" to ensure zero timezone-related booking errors.

## 6. Decision-Maker Linking Engine
The ISA links the candidate (from System 05) and the hiring manager (from System 01) through a confirmed "Interview Event." It ensures that all parties have the necessary "Meeting Packs" (CV, JD, Interview Questions) automatically attached to their calendar invites.

## 7. Data Models & Schema
- `CalendarSyncToken`:
    - `id`: UUID
    - `user_id`: UUID (Recruiter or Hiring Manager)
    - `provider`: Enum (GOOGLE, OUTLOOK)
    - `access_token`: Encrypted String
    - `refresh_token`: Encrypted String
    - `last_sync_at`: DateTime
- `BookingEvent`:
    - `id`: UUID
    - `candidate_id`: UUID
    - `job_id`: UUID
    - `meeting_type`: Enum (SCREEN, TECHNICAL, FINAL)
    - `confirmed_start_at`: DateTime (UTC)
    - `meeting_link`: URL
    - `status`: Enum (PENDING, CONFIRMED, CANCELLED, RESCHEDULED)

## 8. Workflow Diagrams (ASCII)
```text
[ Feedback Approved ] --- (Trigger) ---> [ ISA Magic Link ]
                                              |
                                        v Nylas/Cronofy API v
                                              |
[ Multi-Calendar Sync ] <--- (Overlap Calc) --- [ Availability Engine ]
                                              |
[ Candidate UI ] <--- (Slot Selection) --- [ Booking Portal ]
                                              |
[ Confirm Booking ] --- (Provisioning) ---> [ Zoom / Teams API ]
      |
      +---> [ Update Both Calendars ]
      +---> [ Notify via System 06/08 ]
```

## 9. Tech Stack & Tools
- **API Wrapper:** Nylas / Cronofy (Standardizing O365/Google APIs).
- **Backend:** Node.js (for high-concurrency event handling).
- **Database:** Redis (Availability caching) + PostgreSQL (Booking history).
- **Infrastructure:** Serverless Functions (AWS Lambda) for event-driven provisioning.

## 10. Anti-Bot Evasion Strategy (Evasion & Resilience)
- **Token Security:** Hardware Security Module (HSM) for storing calendar credentials and tokens.
- **Rate-Limiting:** Adhering to provider-specific API quotas (Google/Microsoft) to ensure system stability during bulk scheduling.
- **Spam Defense:** Ensuring magic booking links are single-use or time-bound to prevent unauthorized calendar access.

## 11. Legal & Compliance Considerations
- **Data Privacy:** Only storing the minimum required calendar metadata (Free/Busy status) rather than full meeting content.
- **Explicit Consent:** Candidates must "Opt-In" to the scheduling workflow in compliance with GDPR.
- **Audit Logging:** Maintaining a history of all booking attempts and failures for troubleshooting and dispute resolution.

## 12. MVP vs. Production Scope
- **MVP:** Google Calendar only; single-person scheduling; simple Zoom integration.
- **Production:** Multi-provider (Google/Outlook/iCloud); multi-person panel scheduling; automated rescheduling; round-robin interviewer assignment.

## 13. Error Handling & Resilience
- **Auto-Reschedule Workflow:** If a client deletes a meeting from their calendar, the ISA detects the event via webhook and automatically emails the candidate to reschedule.
- **Sync Failure Alerts:** Notifying the recruiter immediately if a hiring manager's calendar token expires or is revoked.

## 14. Performance & Scale Targets
- **Availability Refresh:** < 1 minute between calendar change and ISA awareness.
- **Booking Latency:** < 3 seconds from "Slot Click" to "Meeting Confirmed."
- **Accuracy:** Zero double-bookings or timezone errors.

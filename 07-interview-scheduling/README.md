# System 07: Interview Scheduling Agent

## 1. Executive Summary
The Interview Scheduling Agent (ISA) is a friction-removing automation layer that coordinates the logistics of candidate and client meetings. It eliminates the back-and-forth "email ping-pong" by providing real-time calendar availability and automated booking links once a candidate is approved for an interview.

## 2. Problem Statement & Business Context
Scheduling is one of the most time-consuming administrative tasks in recruitment. Delays in scheduling lead to candidate drop-off and lost placements. ISA ensures that the momentum of a successful match (from System 06) is maintained through to the interview stage.

## 3. System Architecture Overview
ISA is a **Calendar Orchestration Engine**.
- **Calendar Sync:** Real-time integration with Google Calendar, Outlook, and iCloud.
- **Availability Engine:** Computes the overlap between the hiring manager's schedule and the candidate's preferred times.
- **Booking Service:** Generates meeting invites, creates Video Conference links (Zoom/Teams), and manages time-zone conversions.

## 4. Scraping Layer (Multi-Board) / Data Acquisition
ISA "scrapes" or ingests:
- **Calendar Free/Busy Data:** From integrated O365/GSuite accounts.
- **Interview Preferences:** Ingesting candidate availability from their response to the Scheduling Link.

## 5. Deduplication & Quality Filter Engine
- **Conflict Resolver:** Prevents double-booking by checking all integrated calendars (Personal + Work).
- **Buffer Management:** Automatically adds "prep time" or travel time between interviews based on recruiter preferences.

## 6. Decision-Maker Linking Engine
ISA links the specific candidate (from System 05) to the specific hiring manager (from System 01) and the recruiter in charge. It ensures all parties are notified and have the necessary calendar invites.

## 7. Data Models & Schema
- `InterviewSlot`: (id, manager_id, start_time, end_time, status, type)
- `BookingRecord`: (id, candidate_id, manager_id, job_id, confirmed_time, video_link, status)
- `CalendarIntegration`: (id, user_id, provider, access_token_encrypted, refresh_token_encrypted)

## 8. Workflow Diagrams (ASCII)
```text
[ Client Approved ] -> [ Send Magic Link ] -> [ Candidate Selects Time ]
                                                    |
                                            (Conflict Check)
                                                    |
                                            v Create Invite v
                                                    |
                                            [ Sync to Both Calendars ]
```

## 9. Tech Stack & Tools
- **API Wrapper:** Nylas or Cronofy (for unified calendar API).
- **Video:** Zoom / Microsoft Teams / Google Meet APIs.
- **Backend:** Node.js (for high-concurrency event handling).
- **Database:** Redis (for locking and temporary availability state).

## 10. Anti-Bot Evasion Strategy (Evasion & Resilience)
- **Token Security:** Rotating OAuth tokens and using hardware security modules (HSM) for storing calendar secrets.
- **Rate Limiting:** Ensuring the system doesn't hit Google/Microsoft API rate limits during bulk scheduling events.
- **Spam Protection:** Ensuring scheduling links are only accessible to the intended candidate and client.

## 11. Legal & Compliance Considerations
- **Privacy:** Only accessing "Free/Busy" data, not private event details, unless explicitly required.
- **Data Deletion:** Automatically removing calendar tokens if a user de-authorizes the app.
- **Audit:** Tracking all modifications to calendar events for conflict resolution.

## 12. MVP vs. Production Scope
- **MVP:** Integration with 1 calendar provider (Google) and simple booking links.
- **Production:** Multi-provider sync, automated rescheduling, and round-robin scheduling for panels.

## 13. Error Handling & Resilience
- **Auto-Reschedule:** If a client cancels, the system automatically sends a "Reschedule" link to the candidate.
- **Timezone Safety:** Forcing UTC-based logic throughout the backend to prevent timezone-related booking errors.

## 14. Performance & Scale Targets
- **Sync Latency:** < 1 minute from calendar update to system awareness.
- **Booking Speed:** < 5 seconds to generate an invite after slot selection.
- **Reliability:** 99.99% "No Double-Book" guarantee.

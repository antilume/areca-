# SYSTEM_MAP.md: ARECA OS Inter-System Connectivity

## High-Level Workflow Flow
ARECA OS operates as a continuous pipeline from market signal detection to successful placement.

### 1. The Funnel (Supply and Demand Acquisition)
- **Demand Side:** `01-Demand Intelligence` monitors job boards and news for hiring signals.
- **Supply Side:** `02-Job Board Scraper` crawls identified platforms to ingest live job descriptions.

### 2. Matching Engine (AI Core)
- `03-Candidate Sourcing & Matching` consumes scraped job data and queries internal/external databases.
- `04-Candidate Reactivation` specifically targets the existing database (ATS) to re-engage past candidates.

### 3. Qualification & Engagement
- `05-Resume Screening & Ranking` processes incoming applicants or sourced profiles through an LLM-based scoring engine.
- `06-Automated Client Communication` generates candidate "one-pagers" and handles client feedback loops.

### 4. Operations & Execution
- `07-Interview Scheduling Agent` manages calendar availability and logistics once a candidate is shortlisted.
- `08-Placement Tracking Dashboard` acts as the "Control Tower," consuming events from systems 01-07 for real-time reporting and human oversight.

## System Interdependency Diagram (ASCII)

```text
       [ 01-Demand Intelligence ]
                   |
                   v
       [ 02-Job Board Scraper   ] <---- (External Job Boards)
                   |
                   v
       [ 03-Sourcing & Matching ] <---- (LinkedIn, Indeed, Github)
                   |          ^
                   |          |
                   v          v
       [ 05-Resume Screening    ] <---- [ 04-Candidate Reactivation ]
                   |
                   v
       [ 06-Client Communication ]
                   |
                   v
       [ 07-Interview Scheduling ]
                   |
                   v
       [ 08-Placement Dashboard  ] <--- (CENTRAL CONTROL TOWER)
```

## Shared Data Backbone
- **Unified Profile Store:** Shared schema for candidates used by 03, 04, and 05.
- **Unified Lead Store:** Shared schema for job openings used by 01, 02, and 06.
- **Event Bus:** Shared message queue for all inter-system state transitions.

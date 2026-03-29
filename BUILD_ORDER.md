# BUILD_ORDER.md: ARECA OS Recommended Build Sequence

The following build order is optimized for minimizing dependencies and maximizing time-to-value (TTV).

## Phase 1: The Foundation (Core Services & Infrastructure)
1. **Infrastructure Setup:** VPC, PostgreSQL, Vector DB, and Message Broker.
2. **08-Placement Tracking Dashboard (MVP):** Essential for visualizing the pipeline even with manual data.
3. **Common Services:** Auth/Access Control, Centralized Logging.

## Phase 2: Demand & Data Acquisition
4. **01-Demand Intelligence:** Market signal detection to feed the pipeline.
5. **02-Job Board Scraper:** Core job data ingestion engine.

## Phase 3: Sourcing & Reactivation
6. **04-Candidate Reactivation:** High ROI on existing internal talent (low-hanging fruit).
7. **03-Candidate Sourcing & Matching:** Expanding to external talent discovery.

## Phase 4: Screening & Ranking
8. **05-Resume Screening & Ranking:** Automated qualification of incoming and sourced candidates.

## Phase 5: Communication & Scheduling
9. **06-Automated Client Communication:** Streamlining the "Selling" phase to hiring managers.
10. **07-Interview Scheduling Agent:** High-frequency task automation for operational efficiency.

## Phase 6: Production Hardening
11. **Scale & Evasion:** Anti-bot hardening for System 02.
12. **Analytics & BI:** Advanced reporting for System 08.
13. **Compliance Audit:** Final SOC2/GDPR review.

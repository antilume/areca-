# System 08: Placement Tracking Dashboard / Control Tower

## 1. Executive Summary
The Placement Tracking Dashboard (PTD) is the "Command Center" of ARECA OS. It provides real-time visibility into the entire recruitment funnel, from market signal to final placement. It aggregates data from all 7 other systems into a single, unified view for recruiters and managers.

## 2. Problem Statement & Business Context
Recruitment agencies often suffer from "data silos" across different tools (ATS, LinkedIn, Excel). PTD solves this by providing a "Single Source of Truth," allowing the agency to track KPIs (e.g., Time-to-Hire, Placement Revenue) and optimize their operations.

## 3. System Architecture Overview
PTD is a **Data Aggregator and Visualization Layer**.
- **Data Ingester:** Consumes events from the ARECA OS message bus.
- **Analytics Engine:** Computes real-time metrics (e.g., Funnel conversion rates).
- **Dashboard UI:** A high-performance web interface with real-time updates (WebSockets).

## 4. Scraping Layer (Multi-Board) / Data Acquisition
PTD "scrapes" or ingests:
- **ARECA OS Event Logs:** From Systems 01 through 07.
- **Financial Data:** Ingesting placement fees and revenue from accounting tools (Xero/QuickBooks).

## 5. Deduplication & Quality Filter Engine
- **Metric Verification:** Ensures that a single placement isn't counted twice if a candidate applies to multiple roles.
- **Outlier Detection:** Flags placements with unusually high/low fees for manual review.

## 6. Decision-Maker Linking Engine
PTD provides the "Top-Down" view of all links made in System 01-07. It shows which Hiring Managers (from System 01) are the most active and which candidates (from System 03) are the most "placeable."

## 7. Data Models & Schema
- `KPI_Report`: (id, type, value, timestamp, segment_id)
- `PlacementRecord`: (id, candidate_id, client_id, job_id, fee_amount, start_date, status)
- `AuditLog`: (id, system_id, event_type, payload_json, created_at)

## 8. Workflow Diagrams (ASCII)
```text
[ System 01-07 ] -> [ Event Bus ] -> [ Data Warehouse ]
                                            |
                                    (Metrics Engine)
                                            |
                                    v Real-Time UI v
                                            |
                                    [ Control Tower Dashboard ]
```

## 9. Tech Stack & Tools
- **UI:** React / Next.js / Chart.js / D3.js.
- **Analytics:** DuckDB or ClickHouse (for fast analytical queries).
- **Real-time:** Socket.io or AWS AppSync (GraphQL Subscriptions).
- **Orchestration:** Prefect or Airflow for batch processing of historical data.

## 10. Anti-Bot Evasion Strategy (Evasion & Resilience)
- **Rate-Limited Dashboards:** Ensuring complex analytical queries don't overwhelm the production database.
- **Data Security:** Using row-level security (RLS) to ensure recruiters only see data relevant to their specific desk/team.
- **Caching:** Using Redis to cache expensive KPI calculations.

## 11. Legal & Compliance Considerations
- **Retention:** Deleting PII from historical reports after the required retention period.
- **Anonymization:** Providing aggregate reports (e.g., "Average Fee by Location") without exposing individual candidate or client data.
- **Reporting:** Generating EEO-1 and other diversity reports automatically.

## 12. MVP vs. Production Scope
- **MVP:** Static dashboard with daily data updates and basic funnel metrics.
- **Production:** Real-time WebSockets, advanced predictive analytics (e.g., "Probability of Placement"), and full financial integration.

## 13. Error Handling & Resilience
- **Data Reconciliation:** Regularly comparing the dashboard's "truth" against the source systems (01-07) to detect discrepancies.
- **Stale Data Warning:** Visually flagging any metric that hasn't been updated in > 24 hours.

## 14. Performance & Scale Targets
- **UI Latency:** < 500ms for initial dashboard load.
- **Query Performance:** < 2 seconds for any historical report (1M+ rows).
- **Data Refresh:** Real-time (sub-second) for live pipeline events.

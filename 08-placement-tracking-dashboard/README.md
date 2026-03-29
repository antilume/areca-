# System 08: Placement Tracking Dashboard / Control Tower

## 1. Executive Summary
The Placement Tracking Dashboard (PTD) is the "Control Tower" of ARECA OS. It provides real-time visibility into the entire recruitment funnel, from market signal to final placement. By aggregating data from all 7 other systems into a single, unified view, the PTD enables recruiters to manage their pipeline more effectively and allows agency leadership to track high-level KPIs like Revenue, Conversion Rates, and Time-to-Hire.

## 2. Problem Statement & Business Context
Recruitment data is often siloed across multiple tools (ATS, LinkedIn, Email, Spreadsheets). These silos make it difficult to get a real-time view of the business, leading to missed opportunities and slow operational response. The PTD solves this by creating a "Single Source of Truth," providing actionable insights that drive better decision-making at every stage of the funnel.

## 3. System Architecture Overview
The PTD is a **Real-Time Data Aggregation and Analytics Layer**.
- **Event Bus Ingester:** A Go-based service that consumes state-change events (e.g., "Lead Created," "Candidate Shortlisted," "Interview Booked") from the ARECA OS message bus (RabbitMQ/Redis).
- **OLAP Data Store:** ClickHouse or DuckDB for high-speed analytical queries on millions of historical events.
- **WebSocket Gateway:** A real-time service (Socket.io) that pushes dashboard updates to connected recruiter UIs without requiring page refreshes.

## 4. Scraping Layer (Multi-Board) / Data Acquisition
The PTD "scrapes" internal system data:
- **System Event Logs:** Continuous ingestion of events from Systems 01-07.
- **Financial Data:** Syncing with external accounting tools (Xero, QuickBooks) to track placement fees, invoices, and accounts receivable.
- **Recruiter Productivity:** Tracking system interaction metrics (e.g., number of CVs reviewed, number of client submissions).

## 5. Deduplication & Quality Filter Engine
- **Funnel Consistency Check:** Ensuring that the funnel metrics are logically consistent (e.g., a candidate cannot have an "Interview Booked" without being "Shortlisted").
- **Financial Reconciliation:** Comparing the "Estimated Fee" in ARECA OS with the "Actual Invoiced Fee" in the accounting system to identify discrepancies.

## 6. Decision-Maker Linking Engine
The PTD provides a macro-view of the "Decision-Maker" graph. It identifies which hiring managers and companies have the highest conversion rates and which specific signals (from System 01) are the most predictive of a successful placement.

## 7. Data Models & Schema
- `PipelineEvent`:
    - `id`: UUID
    - `system_id`: Enum (01-07)
    - `event_type`: String (e.g., "SUBMISSION_FEEDBACK_RECEIVED")
    - `payload`: JSONB (Event metadata)
    - `created_at`: DateTime (ClickHouse Partition Key)
- `KPI_Report`:
    - `report_type`: Enum (TIME_TO_HIRE, CONVERSION_RATE, REVENUE_BY_DESK)
    - `segment_id`: UUID (Team or Recruiter ID)
    - `metric_value`: Float
    - `computed_at`: DateTime

## 8. Workflow Diagrams (ASCII)
```text
[ Systems 01-07 ] --- (State Change Event) ---> [ Event Bus (Redis) ]
                                                     |
                                               v Event Ingester v
                                                     |
[ ClickHouse OLAP ] <--- (Batch Insert) --- [ Pipeline Data Warehouse ]
                                                     |
[ Analytics Engine ] --- (Aggregation) ---> [ KPI Data Store (Redis) ]
                                                     |
[ Dashboard UI ] <--- (WebSocket/GraphQL) --- [ Real-Time Gateway ]
      |
      v
[ Recruiter Workspace ]
```

## 9. Tech Stack & Tools
- **UI:** Next.js / Tailwind CSS / D3.js (Visualizations).
- **Analytics:** ClickHouse (OLAP) / Redis (Real-time metrics).
- **Orchestration:** Prefect (Workflow management for historical re-computation).
- **Real-time:** Socket.io or GraphQL Subscriptions.

## 10. Anti-Bot Evasion Strategy (Evasion & Resilience)
- **Rate-Limited Analytical Queries:** Using a "Query Proxy" to ensure complex, heavy reports don't impact the performance of the production transactional database.
- **Row-Level Security (RLS):** Ensuring recruiters only see data and KPIs for the specific desks they are authorized to manage.
- **CDN Caching:** Caching common report structures (e.g., "Monthly Revenue") at the edge to reduce backend load.

## 11. Legal & Compliance Considerations
- **PII Anonymization:** In high-level reports, candidate and client data is anonymized to comply with data privacy regulations.
- **Audit Trails:** Maintaining a non-mutable log of all critical state changes (especially financial and placement events) for legal and financial auditing.
- **Retention Policies:** Automatically archiving event logs older than 7 years (per financial regulations).

## 12. MVP vs. Production Scope
- **MVP:** Daily static reports; simple funnel conversion; PostgreSQL-based analytics.
- **Production:** Real-time (WebSocket) updates; advanced predictive analytics (e.g., "Lead Probability Score"); ClickHouse-based OLAP for sub-second reporting on large datasets; full financial tool integration.

## 13. Error Handling & Resilience
- **Event Replay:** The ability to "Replay" events from the message bus into the data warehouse in case of an ingestion failure.
- **Data Freshness Monitor:** Alerting the engineering team if the dashboard's "Last Updated" timestamp lags behind the live system by more than 5 minutes.

## 14. Performance & Scale Targets
- **Initial Load:** < 500ms for the main dashboard.
- **Analytical Query Performance:** < 1 second for reports on 1M+ event records.
- **Data Latency:** < 5 seconds from system event to dashboard update.

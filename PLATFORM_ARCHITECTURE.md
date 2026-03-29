# PLATFORM_ARCHITECTURE.md: ARECA OS Core Platform Architecture

## Executive Summary
ARECA OS is built on a modular, event-driven architecture designed to support a high-throughput, AI-augmented recruitment lifecycle. This document outlines the foundational services, data orchestration, and security models that unify the 8 core systems.

## 1. Orchestration Model: Event-Driven Core
The system utilizes a **hub-and-spoke event model** to ensure decoupling and scalability.
- **Message Broker:** RabbitMQ or Redis Streams for asynchronous task distribution.
- **Workflow Orchestrator:** Temporal.io or AWS Step Functions to manage complex, multi-system state machines (e.g., from sourcing to interview scheduling).
- **Service Mesh:** Internal gRPC communication for low-latency synchronous requests between core services.

## 2. Shared Services & Storage
To avoid redundancy, ARECA OS maintains common infrastructure:
- **Centralized Data Store:** PostgreSQL (Primary transactional DB) + Pinecone/Milvus (Vector DB for candidate/job matching).
- **Blob Storage:** AWS S3 or MinIO for resumes and document storage.
- **Caching Layer:** Redis for session state and high-frequency scraping data.
- **Identity Provider (IdP):** Keycloak or Auth0 for unified authentication across all 8 modules.

## 3. Auth & Access Model
- **RBAC (Role-Based Access Control):** Granular permissions for Recruiters, Admins, and Clients.
- **Scoped API Keys:** Each of the 8 systems uses scoped service tokens for inter-system communication.
- **MFA (Multi-Factor Authentication):** Required for all human-in-the-loop interfaces.

## 4. Event Flow & Background Jobs
1. **Trigger:** `01-Demand Intelligence` identifies a new market lead.
2. **Event:** Emits `market_lead.created` event.
3. **Action:** `02-Job Board Scraper` consumes the event and begins crawling relevant platforms.
4. **Outcome:** Scraped jobs are normalized and indexed, triggering `03-Candidate Sourcing & Matching`.

## 5. Audit, Logging & Observability
- **Audit Logs:** Every state change (e.g., "Candidate Shortlisted") is recorded with a timestamp and actor ID.
- **Distributed Tracing:** Jaeger/OpenTelemetry to track requests across the 8 systems.
- **Log Aggregation:** ELK Stack (Elasticsearch, Logstash, Kibana) for centralized error and performance monitoring.

## 6. Human-in-the-Loop (HITL) & Oversight
ARECA OS is an *augmented* system. Oversight points are baked into the flow:
- **Approval Gates:** High-risk actions (e.g., sending an automated email to a premium client) require recruiter approval via the `08-Placement Tracking Dashboard`.
- **Quality Control:** Random sampling of AI-ranked resumes for manual review to prevent algorithmic bias.

## 7. Security Boundaries
- **Network Isolation:** Systems are deployed within private VPC subnets.
- **Data Encryption:** AES-256 at rest and TLS 1.3 in transit.
- **PII Masking:** Candidate PII is masked during the initial screening phase until a recruiter initiates a "reveal" action.

## 8. Notification Layer
A unified service for:
- **Internal Alerts:** Slack/Teams integrations for recruiters.
- **Candidate Comms:** Email (SendGrid/Postmark) and SMS (Twilio).
- **System Health:** PagerDuty integration for infra failures.

# System 01: Demand Intelligence System

## 1. Executive Summary
The Demand Intelligence System (DIS) is the "scout" of ARECA OS. It monitors the external hiring market to identify high-potential business development (BD) leads for the recruitment agency. By detecting early signals of hiring intent (funding, expansion, headcount growth) before they hit major job boards, the DIS allows recruiters to engage hiring managers before their competitors do.

## 2. Problem Statement & Business Context
Recruitment agencies often react to job postings after they are public, leading to high competition and low margins. The DIS shifts the agency from a reactive to a proactive BD model. It solves the "who is hiring?" problem by aggregating signals from non-traditional sources like news, funding rounds, and LinkedIn team growth, providing a first-mover advantage.

## 3. System Architecture Overview
DIS is an ingestion-heavy system based on a **Signal-to-Lead Pipeline**.
- **Signal Collectors:** Modular scrapers (Scrapy) and API connectors (Crunchbase, TechCrunch, LinkedIn).
- **Signal Scoring Engine:** A two-stage NLP pipeline. Stage 1 uses FastText for high-speed noise filtering; Stage 2 uses GPT-4o-mini to classify signals into hiring intent categories (e.g., "Aggressive Expansion," "Stable Hiring," "Replacement Need").
- **Lead Repository:** A PostgreSQL store with PostGIS for location-aware lead distribution.

## 4. Scraping Layer (Multi-Board)
The DIS scraping layer is optimized for signal detection rather than just job ingestion:
- **News/PR Aggregators:** Monitoring RSS feeds and site-specific scrapers for keywords like "series A," "new office," or "VP of Engineering."
- **Social Signal Scraper:** Monitoring company-level headcount changes and "hiring" badges on LinkedIn profiles.
- **Competitor Job Boards:** Monitoring the *volume* of postings on competitor sites as a proxy for company growth.
- **Company Career Portals:** Differential scraping (comparing snapshots) to detect "hidden" roles not yet pushed to aggregators.

## 5. Deduplication & Quality Filter Engine
- **Entity Resolution (ER):** Uses a BERT-based matching model to unify company names (e.g., "Acme Corp" vs "Acme Inc").
- **Signal Weighting:** Assigns weights to signals (e.g., a Series B funding round is weighted 3x higher than a single job repost).
- **Temporal Filtering:** Discards signals that are duplicates within a 30-day window to prevent "signal fatigue."

## 6. Decision-Maker Linking Engine
Once a high-intent lead is created, the system initiates a **Graph Matching** process:
1. **Identify Roles:** Queries the Company Graph for titles like "Director of Talent," "VP Engineering," or "Hiring Manager."
2. **Contact Discovery:** Asynchronous calls to Apollo.io or Hunter.io APIs to retrieve verified professional emails.
3. **Relationship Mapping:** Checks internal CRM data (System 04) to see if any recruiter has a "warm" historical relationship with the identified decision-maker.

## 7. Data Models & Schema
- `CompanySignal`:
    - `id`: UUID (Primary Key)
    - `company_name`: String (Normalized via ER)
    - `signal_type`: Enum (FUNDING, EXPANSION, HEADCOUNT_GROWTH, JOB_VOLUME)
    - `source_url`: URL
    - `raw_payload`: JSONB (Original signal data)
    - `intent_score`: Float (0.0 to 1.0)
- `HiringLead`:
    - `id`: UUID
    - `company_id`: UUID (Foreign Key)
    - `priority_level`: Enum (P0, P1, P2)
    - `status`: Enum (NEW, ASSIGNED, CONTACTED, CONVERTED, DISCARDED)
    - `decision_maker_ids`: UUID[] (Array of linked DM contacts)

## 8. Workflow Diagrams (ASCII)
```text
[ Signal Sources ]
      |
      v
[ Scraper/API Workers ] --- (Raw Data) ---> [ Signal Buffer (Redis) ]
                                                   |
                                            v NLP Scoring v
                                                   |
[ Entity Resolver ] <--- (Normalized Name) --- [ Lead Generator ]
                                                   |
                                            v Lead Store (PG) v
                                                   |
[ Enrichment Worker ] <--- (Link Decision Makers) --- [ DM Linker ]
      |
      v
[ Dashboard / CRM ]
```

## 9. Tech Stack & Tools
- **Framework:** Python / Scrapy / FastAPI.
- **NLP:** HuggingFace Transformers (BERT) / OpenAI API.
- **Database:** PostgreSQL + TimescaleDB (for signal history).
- **Task Queue:** Celery + RabbitMQ.
- **Data Enrichment:** Apollo.io / Clearbit APIs.

## 10. Anti-Bot Evasion Strategy
- **Proxy Mesh:** Utilizing a rotating pool of 50k+ residential IPs (Bright Data).
- **Header Fingerprinting:** Mimicking specific browser versions (Chrome/Firefox/Safari) on mobile and desktop.
- **Behavioral Jitter:** Adding randomized sleep intervals (Poisson distribution) between requests to mimic human browsing.

## 11. Legal & Compliance Considerations
- **GDPR Article 6:** Legitimate Interest processing for B2B contact data.
- **Robots.txt:** Strict adherence to crawling policies for non-public data.
- **Data Minimization:** Only storing the minimum PII required for business outreach (Name, Title, Company Email).

## 12. MVP vs. Production Scope
- **MVP:** Scraping 2 news sources + 1 job board; manual Decision-Maker linking; daily batch processing.
- **Production:** 50+ signal sources; automated DM linking with API enrichment; real-time signal-to-lead latency (< 15 mins).

## 13. Error Handling & Resilience
- **Dead Letter Queues (DLQ):** Capturing signals that fail NLP classification for manual review.
- **Stale Signal Monitor:** Automatically archiving leads that haven't had a new signal in 60 days.
- **Scraper Health Checks:** Monitoring "Blocked Rate" per source and auto-switching proxy providers.

## 14. Performance & Scale Targets
- **Throughput:** Processing 100,000 signals per day.
- **Latency:** < 10 seconds for NLP classification.
- **Lead Quality:** > 85% conversion from "System-Created Lead" to "Recruiter-Accepted Lead."

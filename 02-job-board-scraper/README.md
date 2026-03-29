# System 02: Intelligent Job Board Scraper

## 1. Executive Summary
The Intelligent Job Board Scraper (IJBS) is the primary engine for high-volume, cross-platform job data acquisition. It provides a clean, normalized, and schema-validated stream of job listings to ARECA OS. By utilizing distributed workers and advanced anti-bot evasion, the IJBS ensures a comprehensive view of the market while maintaining high data integrity.

## 2. Problem Statement & Business Context
Job market data is fragmented across hundreds of job boards, each with unique HTML structures, anti-bot mechanisms, and data schemas. Manually monitoring these is impossible at scale. The IJBS automates this, ensuring that ARECA OS has a real-time, deduplicated map of all relevant job openings, which directly feeds into the sourcing and matching engines.

## 3. System Architecture Overview
The IJBS is a **Distributed Crawler Grid** with a decoupled normalization layer.
- **Scraper Controller:** A Node.js service that manages the job queue (Redis) and assigns tasks to workers based on site-specific health metrics.
- **Worker Pool:** Containerized Playwright/Puppeteer instances that execute the scraping scripts. Each worker uses a unique session and proxy identity.
- **Normalization Engine:** A Python-based service that uses Pydantic models and LLM-assisted extraction for non-standard HTML structures.

## 4. Scraping Layer (Multi-Board)
The scraper uses a "Provider-Adapter" pattern for modularity:
- **Direct API Adapters:** For platforms with official APIs (e.g., Reed.co.uk, Adzuna).
- **DOM-Based Adapters:** Custom CSS/XPath-based scrapers for major sites (LinkedIn, Indeed).
- **LLM-Based Extraction:** For niche sites where DOM structures change frequently. The system sends a subset of the HTML to an LLM to extract fields like `salary`, `remote_status`, and `tech_stack`.

## 5. Deduplication & Quality Filter Engine
- **Content Hashing:** Uses SimHash on normalized job descriptions to identify duplicates across different boards.
- **Data Completeness Filter:** Discards listings that are missing critical fields like `title`, `company`, or `location`.
- **"Phantom" Job Detection:** Flags jobs that have been posted for > 90 days or have been repeatedly refreshed without changes to the description.

## 6. Decision-Maker Linking Engine
The IJBS extracts hiring manager names, department names, and recruiter contact info directly from the job description or metadata. This data is passed to System 01's linking engine for enrichment and CRM mapping.

## 7. Data Models & Schema
- `RawScrapeTask`:
    - `id`: UUID
    - `source_id`: String (e.g., "indeed_uk")
    - `target_url`: URL
    - `retry_count`: Integer
    - `status`: Enum (PENDING, ACTIVE, COMPLETED, FAILED)
- `NormalizedJob`:
    - `id`: UUID (Hash of source_id + external_id)
    - `external_id`: String (Original board ID)
    - `title`: String
    - `description`: Text
    - `salary_min/max`: Decimal
    - `is_remote`: Boolean
    - `tech_stack`: String[]
    - `posted_at`: DateTime

## 8. Workflow Diagrams (ASCII)
```text
[ Scraper Controller ]
      |
      v
[ BullMQ Queue (Redis) ]
      |
      v
[ Worker Node (Playwright) ] --- (Raw HTML) ---> [ S3 Bucket ]
      |
      v
[ Normalization Engine ] <--- (Pydantic Models) --- [ Field Mapping ]
      |
      v
[ Deduplication Engine ] --- (SimHash Compare) ---> [ Job Store (PG) ]
      |
      v
[ Event Bus ] ---> (Job Created Event)
```

## 9. Tech Stack & Tools
- **Runtime:** Node.js (Controller) / Python (Normalization).
- **Libraries:** Playwright, Pydantic, Beautiful Soup.
- **Infrastructure:** Docker / Kubernetes (Auto-scaling worker pool).
- **Proxy Management:** Zyte Smart Proxy Manager / Bright Data.

## 10. Anti-Bot Evasion Strategy
- **Fingerprint Randomization:** Randomized `Canvas`, `WebGL`, and `Audio` fingerprints via `playwright-extra`.
- **TLS Handshake Spoofing:** Mimicking specific browser TLS fingerprints to bypass JA3-based blocking.
- **Human-Like Navigation:** Randomized scrolling, mouse movement (Bezier curves), and variable click durations.
- **Proxy Tunneling:** Automatic rotation between Data Center, Residential, and Mobile IPs based on site resistance.

## 11. Legal & Compliance Considerations
- **hiQ vs. LinkedIn Precedent:** Scraping public-facing data only.
- **CFAD (Computer Fraud and Abuse Act):** Avoiding scraping behind logins without explicit permission.
- **Data Sovereignty:** Storing job data in the region where it was scraped to comply with local data laws.

## 12. MVP vs. Production Scope
- **MVP:** 5 major job boards; single-region proxy; basic Regex-based parsing.
- **Production:** 50+ job boards; multi-region global proxy mesh; LLM-assisted normalization; real-time phantom job detection.

## 13. Error Handling & Resilience
- **Exponential Backoff:** Retrying failed scrapes with increasing delays.
- **Circuit Breaker:** Automatically pausing all scrapers for a specific domain if the "Blocked Rate" exceeds 20%.
- **Schema Drift Detection:** Alerting when the percentage of "unmapped" fields in a specific board increases suddenly.

## 14. Performance & Scale Targets
- **Volume:** Scraping 500,000+ job URLs daily.
- **Deduplication Accuracy:** > 99% identification of cross-platform duplicates.
- **Normalization Latency:** < 500ms per job listing.

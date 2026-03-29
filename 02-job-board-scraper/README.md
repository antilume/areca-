# System 02: Intelligent Job Board Scraper

## 1. Executive Summary
The Intelligent Job Board Scraper (IJBS) is the primary engine for high-volume job data acquisition. It provides a clean, normalized stream of job listings to the rest of ARECA OS, acting as the foundation for candidate matching and market analysis.

## 2. Problem Statement & Business Context
Manually monitoring dozens of job boards is impossible at scale. IJBS automates this by providing a programmatic interface to otherwise unstructured web data. The business context is to ensure ARECA OS always has the most current and comprehensive "map" of the available job market.

## 3. System Architecture Overview
IJBS follows a **Distributed Worker Pattern**.
- **Scraper Controller:** Manages job queues and schedules.
- **Scraper Workers:** Individual nodes running headless browsers or API clients.
- **Normalization Engine:** Converts platform-specific HTML into a standard JSON schema.

## 4. Scraping Layer (Multi-Board)
The scraping layer is designed for modularity, with "adapters" for:
- **Major Boards:** LinkedIn, Indeed, ZipRecruiter, Monster.
- **Niche Boards:** Dice (Tech), Behance (Creative), Dribbble.
- **Aggregators:** Adzuna, Jooble.
- **ATS Career Portals:** Workday, Greenhouse, Lever.

## 5. Deduplication & Quality Filter Engine
- **Duplicate Detection:** MinHash or SimHash for identifying the same job posted across multiple boards.
- **Quality Scoring:** Flags listings with missing descriptions, suspicious salary ranges, or "phantom" roles.
- **Freshness Check:** Verifies if a listing is still active by performing a "head" request to the source URL.

## 6. Decision-Maker Linking Engine
While DIS (System 01) focuses on broad market signals, IJBS provides the specific job context (IDs, descriptions) that triggers the linking engine. It extracts hiring manager names directly from job descriptions when available.

## 7. Data Models & Schema
- `JobListing`: (id, board_source, source_url, company_name, title, location, description_raw, description_cleaned, salary_range, employment_type, date_posted, date_scraped)
- `PlatformConfig`: (id, board_name, base_url, scraper_type, retry_limit, status)

## 8. Workflow Diagrams (ASCII)
```text
[ Scraper Controller ] -> [ Worker Pool ] -> [ Multi-Platform Scraper ]
                                                    |
                                            (Raw HTML / JSON)
                                                    |
                                            v Normalization v
                                                    |
                                            [ Job Store / Bus ]
```

## 9. Tech Stack & Tools
- **Runtime:** Node.js / Playwright (for dynamic content).
- **Orchestration:** BullMQ or RabbitMQ.
- **Proxy Management:** Zyte or SmartProxy.
- **Parser:** Python (BeautifulSoup) or LLM-based extraction for complex sites.

## 10. Anti-Bot Evasion Strategy
- **Fingerprint Randomization:** Overriding navigator properties and WebGL fingerprints.
- **Behavioral Simulation:** Randomized mouse movements, scrolling, and click delays.
- **CAPTCHA Solving:** Integration with 2Captcha or similar services for unavoidable blocks.

## 11. Legal & Compliance Considerations
- **Public Domain Data:** Only scraping data that does not require an account.
- **Rate Limiting:** Ensuring scrapers do not overwhelm source sites (good citizen policy).
- **Data Sovereignty:** Compliance with local data scraping laws (e.g., hiQ vs. LinkedIn).

## 12. MVP vs. Production Scope
- **MVP:** 3-4 major job boards, single-node worker.
- **Production:** 20+ boards, globally distributed worker pool, advanced evasion, and CAPTCHA solving.

## 13. Error Handling & Resilience
- **Shadowing:** Comparing scraped data against known "truth" sets to detect silent failures.
- **Dead Letter Queues:** Isolating failed scrape tasks for manual inspection.
- **Self-Healing:** Automatically restarting workers that encounter persistent blocks.

## 14. Performance & Scale Targets
- **Throughput:** 50,000+ listings scraped and normalized per day.
- **Accuracy:** > 95% correctly parsed fields (salary, title, location).
- **Uptime:** 99.9% for the scraper controller.

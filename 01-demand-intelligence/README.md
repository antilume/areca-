# System 01: Demand Intelligence System

## 1. Executive Summary
The Demand Intelligence System (DIS) is the "scout" of ARECA OS. It monitors the external hiring market to identify high-potential business development (BD) leads for the recruitment agency. By detecting early signals of hiring intent, the DIS allows recruiters to engage hiring managers before their competitors do.

## 2. Problem Statement & Business Context
Recruitment agencies often react to job postings after they are public, leading to high competition. The business context for DIS is to shift from reactive to proactive BD. It solves the "who is hiring?" problem by aggregating signals from non-traditional sources (news, funding rounds, LinkedIn team growth) alongside traditional job boards.

## 3. System Architecture Overview
DIS is an ingestion-heavy system. It uses a series of **Signal Collectors** that feed into a **Signal Scoring Engine**.
- **Collectors:** Web scrapers and API integrations.
- **Scoring Engine:** An LLM-based classifier that determines the "Hiring Temperature" of a company.
- **Lead Repository:** A PostgreSQL store for tracking leads and company profiles.

## 4. Scraping Layer (Multi-Board)
The scraping layer targets:
- **Major Job Boards:** LinkedIn, Indeed, Glassdoor (monitoring volume changes).
- **Company Career Pages:** Identifying "ghost" jobs or unlisted roles.
- **News/PR:** TechCrunch, Crunchbase (funding, expansions).
- **Social Signals:** Employee headcount trends on LinkedIn.

## 5. Deduplication & Quality Filter Engine
- **Entity Resolution:** Maps "Acme Corp," "Acme Inc," and "Acme" to a single company entity.
- **Noise Reduction:** Filters out automated job reposts and expired listings using checksum comparisons.
- **Relevance Filter:** Discards leads that do not match the agency's niche (e.g., filtering out retail jobs for a tech agency).

## 6. Decision-Maker Linking Engine
Once a lead is identified, this engine uses:
- **LinkedIn API/Scraping:** Identifies the Head of Talent, CTO, or Hiring Manager.
- **Enrichment Services:** Integrations with Apollo.io or Hunter.io to find professional email addresses and phone numbers.
- **Graph Mapping:** Links identified decision-makers to the specific job lead.

## 7. Data Models & Schema
- `CompanySignal`: (id, company_name, signal_type, source_url, timestamp, raw_content)
- `HiringLead`: (id, company_id, job_title, estimated_budget, priority_score, status)
- `DecisionMaker`: (id, company_id, name, title, linkedin_url, email_status)

## 8. Workflow Diagrams (ASCII)
```text
[ Signal Source ] -> [ Scraper Layer ] -> [ LLM Classifier ] -> [ Lead Store ]
                                                |
                                        (If High Temp Lead)
                                                |
                                        v Link Decision Makers v
                                                |
                                        [ CRM / Dashboard ]
```

## 9. Tech Stack & Tools
- **Language:** Python (Scrapy, BeautifulSoup).
- **LLM:** OpenAI GPT-4o-mini (Classification).
- **Data Enrichment:** Apollo API.
- **Storage:** PostgreSQL.

## 10. Anti-Bot Evasion Strategy
- **Residential Proxies:** Rotating IP addresses (Bright Data).
- **User-Agent Rotation:** Mimicking various browsers and devices.
- **Headless Browser Stealth:** Using Playwright with stealth plugins to bypass Cloudflare.

## 11. Legal & Compliance Considerations
- **TOS Compliance:** Adherence to site-specific robots.txt.
- **PII:** Only scraping publicly available professional data.
- **Data Retention:** Policy-driven deletion of stale leads.

## 12. MVP vs. Production Scope
- **MVP:** Scraping top 2 job boards and manual lead scoring.
- **Production:** Full multi-signal ingestion (news + funding) and automated LLM scoring with API-based enrichment.

## 13. Error Handling & Resilience
- **Retry Logic:** Exponential backoff for scraper failures.
- **Circuit Breakers:** Pausing scrapers if a site's structure changes significantly.
- **Alerting:** PagerDuty for persistent data ingestion gaps.

## 14. Performance & Scale Targets
- **Ingestion:** 10,000+ signals per day.
- **Latency:** < 1 hour from signal detection to lead creation.
- **Accuracy:** > 90% relevance score for identified leads.

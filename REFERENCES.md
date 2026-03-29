# REFERENCES.md: ARECA OS Architecture References

## Architecture & Patterns
- **Clean Architecture (Uncle Bob):** Separation of concerns (Entities, Use Cases, Adapters).
- **Event-Driven Microservices:** Patterns for saga management and eventual consistency.
- **Vector Search (RAG):** Best practices for candidate-to-job matching using embeddings (OpenAI `text-embedding-3-small`, Pinecone/Milvus).

## Scraping & Data Acquisition
- **Anti-Bot Techniques:** Reference to Puppeteer-Stealth, Playwright, and Fingerprint rotation (Bright Data, Zyte).
- **DOM Parsing & LLM-based Extraction:** Using LangChain or Pydantic for structured data extraction from HTML.

## AI & ML Standards
- **Fairness & Bias Mitigation:** Responsible AI practices for screening (NIST AI RMF).
- **PII Protection:** GDPR and CCPA compliance for candidate data (Anonymization, Pseudonymization).

## Infrastructure & Ops
- **IaC (Infrastructure as Code):** Terraform or Pulumi for reproducible AWS/GCP deployments.
- **CI/CD:** GitHub Actions or GitLab CI for automated testing and container deployment (Docker/K8s).

## External Services & APIs
- **Job Boards:** LinkedIn, Indeed, Glassdoor (API and Scraping policies).
- **ATS Integrations:** Bullhorn, Greenhouse, Lever, Workday (common OIDC/OAuth2 patterns).
- **Communication:** Twilio (SMS), SendGrid (Email), Nylas (Calendar/Email API).

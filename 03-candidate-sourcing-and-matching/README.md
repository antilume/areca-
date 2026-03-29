# System 03: AI Candidate Sourcing & Matching

## 1. Executive Summary
The AI Candidate Sourcing & Matching (AICSM) system is the core intelligence hub for finding talent. It takes job descriptions (from System 02) and automatically identifies, evaluates, and ranks potential candidates from external sources and internal databases using semantic search and vector embeddings.

## 2. Problem Statement & Business Context
Recruiters spend hours searching LinkedIn and job boards using rigid Boolean strings. AICSM replaces this with "Semantic Intent Matching," allowing recruiters to describe a role in natural language and receive a ranked list of candidates who are a contextual fit, not just a keyword match.

## 3. System Architecture Overview
AICSM is built around a **Retrieval-Augmented Generation (RAG)** architecture.
- **Embedding Engine:** Converts job descriptions and resumes into high-dimensional vectors.
- **Vector Database:** Stores and indexes candidate profiles for fast similarity searches.
- **Re-Ranker:** A secondary, more expensive LLM pass that evaluates the top 50 matches for specific nuances (e.g., career progression, tech stack depth).

## 4. Scraping Layer (Multi-Board) / Data Acquisition
AICSM interfaces with:
- **Professional Networks:** LinkedIn, Xing, Viadeo.
- **Technical Portfolios:** GitHub (for code quality), Stack Overflow.
- **Niche Communities:** Kaggle (Data Science), Behance (Design).
- **Aggregated APIs:** People Data Labs, Clearbit (for profile enrichment).

## 5. Deduplication & Quality Filter Engine
- **Cross-Platform Merging:** Uses fuzzy matching and email hashing to merge a candidate's GitHub, LinkedIn, and internal ATS profiles into a "Golden Profile."
- **Bot/Spam Filtering:** Identifies and excludes low-quality or "bot-generated" profiles.
- **Work History Validation:** Checks for logical inconsistencies in employment dates.

## 6. Decision-Maker Linking Engine
While other systems link jobs to hiring managers, AICSM links candidates to specific open roles based on "fit scores." It identifies which hiring manager (from System 01) would be most interested in a specific high-value candidate ("Most Placeable Candidate" or MPC).

## 7. Data Models & Schema
- `CandidateVector`: (candidate_id, embedding_vector, last_updated)
- `MatchScore`: (job_id, candidate_id, score, match_reasoning_json)
- `GoldenProfile`: (id, full_name, current_title, skills_list, experience_years, locations, contact_info_encrypted)

## 8. Workflow Diagrams (ASCII)
```text
[ Job Desc ] -> [ Vectorize ] -> [ Vector Search (Top 100) ]
                                        |
                                [ LLM Re-Ranker (Top 20) ]
                                        |
                                [ Ranked Candidate List ] -> [ Dashboard ]
```

## 9. Tech Stack & Tools
- **Vector DB:** Pinecone or Milvus.
- **Embeddings:** OpenAI `text-embedding-3-large`.
- **Logic:** Python (LangChain, Pydantic).
- **Search:** Elasticsearch for hybrid (keyword + semantic) search.

## 10. Anti-Bot Evasion Strategy
- **Headless API Interaction:** Prioritizing official APIs (LinkedIn Talent Solutions) where possible.
- **Rate-Limited Crawling:** For secondary sources (GitHub), using personal access tokens and respecting rate limits.
- **Session Persistence:** Maintaining browser sessions to avoid frequent re-logins.

## 11. Legal & Compliance Considerations
- **Fairness & Bias:** Regular auditing of the ranking engine to ensure it doesn't discriminate based on gender, age, or ethnicity (using bias-detection libraries).
- **GDPR:** "Right to be Forgotten" implementation for candidates.
- **CCPA:** Transparency in how candidate data is sourced and used for ranking.

## 12. MVP vs. Production Scope
- **MVP:** Semantic search over internal database + 1 external source (GitHub).
- **Production:** Multi-source ingestion, real-time re-ranking, and automated "MPC" identification.

## 13. Error Handling & Resilience
- **Fallback to Keyword Search:** If the Vector DB or Embedding API is down, the system reverts to traditional Boolean search.
- **Stale Data Alerts:** Notifies recruiters if a high-ranking candidate's profile hasn't been updated in > 1 year.

## 14. Performance & Scale Targets
- **Search Latency:** < 2 seconds for semantic retrieval across 1M+ profiles.
- **Re-Ranking Time:** < 10 seconds for the top 50 profiles.
- **Match Precision:** > 80% (top 5 candidates are relevant to the job).

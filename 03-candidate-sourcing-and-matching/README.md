# System 03: AI Candidate Sourcing & Matching

## 1. Executive Summary
The AI Candidate Sourcing & Matching (AICSM) system is the intelligent core of ARECA OS. It automates the discovery and evaluation of candidates by mapping multi-source talent data against live job descriptions. Using a high-fidelity Vector RAG (Retrieval-Augmented Generation) pipeline, AICSM identifies the "Top 1% Fit" for any role, regardless of whether they are in the internal database or on external professional networks.

## 2. Problem Statement & Business Context
Recruiters currently spend 60-70% of their time manually searching LinkedIn using rigid Boolean strings that fail to capture semantic nuances (e.g., matching a "Node.js Expert" with a "Javascript Backend Lead"). AICSM solves this by shifting from "Keyword Matching" to "Intent-Based Matching," drastically reducing time-to-shortlist and surfacing overlooked high-potential candidates.

## 3. System Architecture Overview
The AICSM is a **Bi-Encoder + Cross-Encoder Semantic Search** pipeline.
- **Bi-Encoder Stage:** Uses OpenAI `text-embedding-3-large` to embed all candidates and jobs into a high-dimensional vector space. Initial retrieval is performed using Cosine Similarity in a vector database.
- **Cross-Encoder Stage (Re-Ranking):** The top 100 retrieved candidates are passed to a more expensive Cross-Encoder (GPT-4o) that performs a deep, contextual comparison between the full CV and the JD.
- **Vector DB:** Pinecone (Serverless) or Milvus for sub-second retrieval.

## 4. Scraping Layer (Multi-Board) / Data Acquisition
AICSM sources data from:
- **Professional Social Graphs:** LinkedIn (via Talent API or Scraper), GitHub (Code complexity/contributions), StackOverflow (Reputation).
- **Public Talent Registries:** Kaggle, Behance, Dribbble.
- **B2B Enrichment APIs:** People Data Labs (PDL), Clearbit, Apollo (to refresh work history).

## 5. Deduplication & Quality Filter Engine
- **Golden Profile Merging:** Uses a weighted Levenshtein distance and email/social-link hashing to unify profiles (e.g., merging a candidate's GitHub projects with their LinkedIn employment history).
- **Signal-to-Noise Filter:** Automatically discards "Bot Profiles," "Keyword Stuffers," and candidates with significant unverifiable gaps in employment.

## 6. Decision-Maker Linking Engine
AICSM links high-value candidates ("Most Placeable Candidates" or MPCs) to hiring managers identified in System 01. It uses predictive modeling to suggest which companies (even those without active roles) would be a high-probability fit for a specific candidate's unique profile.

## 7. Data Models & Schema
- `CandidateEmbedding`:
    - `candidate_id`: UUID
    - `vector`: Float[] (3072 dimensions)
    - `metadata`: JSONB (Title, Years of Exp, Location, Tech Stack)
    - `last_embedded_at`: DateTime
- `MatchResult`:
    - `id`: UUID
    - `job_id`: UUID
    - `candidate_id`: UUID
    - `semantic_score`: Float (0.0 - 1.0)
    - `reasoning_summary`: Text (AI-generated explanation of the fit)

## 8. Workflow Diagrams (ASCII)
```text
[ Raw Job Description ]
      |
      v
[ OpenAI Embedding ]
      |
      v
[ Pinecone Vector Search ] <--- (Initial Retrieve) --- [ Candidate Vector DB ]
      |
      v
[ GPT-4o Cross-Encoder ] <--- (Top 100 Candidates)
      |
      v
[ Ranked Shortlist ] --- (Reasoning) ---> [ System 06 Dashboard ]
```

## 9. Tech Stack & Tools
- **Embeddings:** OpenAI `text-embedding-3-large`.
- **Vector Database:** Pinecone or Milvus.
- **Orchestration:** LangChain / LlamaIndex.
- **Search:** Hybrid Search (Vector + BM25 keyword search via Elasticsearch).

## 10. Anti-Bot Evasion Strategy
- **Headless Browser Rotation:** Rotating between real user-agent strings and viewport sizes for LinkedIn/GitHub scraping.
- **Session Throttling:** Mimicking natural human "reading" patterns (pausing on profiles for 3-15 seconds).
- **Social Graph Mimicry:** For LinkedIn, interacting with the "People Also Viewed" section to stay within standard usage patterns.

## 11. Legal & Compliance Considerations
- **Algorithmic Fairness:** Auditing the embedding model to ensure it doesn't favor specific demographics (e.g., gender or age-based bias).
- **GDPR Article 17 (Right to Erasure):** Ensuring that when a candidate is deleted, their vector embedding is also purged from the index.
- **CCPA:** Providing transparency to candidates on how they were ranked or sourced.

## 12. MVP vs. Production Scope
- **MVP:** Semantic search on 10k internal profiles; simple cosine similarity; single external source (LinkedIn).
- **Production:** Hybrid search on 1M+ profiles; real-time Cross-Encoder re-ranking; multi-source ingestion (GitHub/Behance/PDL); automated MPC identification.

## 13. Error Handling & Resilience
- **Re-Embedding Queue:** Retrying embedding tasks if the OpenAI API is down or throttled.
- **Fallback to Keyword:** If the Vector DB is unavailable, the system automatically falls back to standard Elasticsearch Boolean search to ensure continuity.

## 14. Performance & Scale Targets
- **Search Latency:** < 1.5 seconds for the top 100 candidates.
- **Re-Ranking Latency:** < 5 seconds for the top 20 candidates.
- **Match Precision:** > 90% relevance in the top 10 results.

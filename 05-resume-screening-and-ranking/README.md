# System 05: AI Resume Screening & Ranking

## 1. Executive Summary
The AI Resume Screening & Ranking (ASR) system is a high-throughput, context-aware engine that automates the initial qualification of resumes. By utilizing LLMs to simulate a deep "human-like" reading of the full resume text against a specific job description, it provides a ranked list with explainable scores. The ASR eliminates the noise of bulk applications while ensuring that every candidate is evaluated fairly and thoroughly.

## 2. Problem Statement & Business Context
Recruiters spend an average of 6-7 seconds per resume, leading to human fatigue and the potential for overlooking high-quality "quiet" candidates. Traditional ATS systems use keyword-matching, which is easily gamed by "keyword stuffing." The ASR solves this by using semantic understanding to evaluate the *quality and context* of experience, reducing the manual screening load by > 80% while increasing the quality of the shortlist.

## 3. System Architecture Overview
The ASR is an **Asynchronous Evaluation Pipeline**.
- **Ingestion Worker:** Converts multi-format documents (PDF, Docx) into structured markdown for LLM processing.
- **Criteria Generator:** Uses an LLM to "deconstruct" a job description into a set of weighted scoring criteria (e.g., "5+ years of React," "Experience in FinTech").
- **Scoring Engine:** A chain of LLM prompts that first "Evidence-Checks" the resume (finding specific quotes that support skills) and then assigns a score.
- **Explainability Module:** Generates a human-readable justification for the score, highlighting "Pros," "Cons," and "Missing Evidence."

## 4. Scraping Layer (Multi-Board) / Data Acquisition
The ASR ingests data from:
- **Direct Application Portals:** Resumes uploaded by candidates.
- **System 02/03 Output:** Profiles scraped from LinkedIn, GitHub, or other external sources.
- **Email Inboxes:** Automated parsing of resume attachments from recruiter inboxes via IMAP.

## 5. Deduplication & Quality Filter Engine
- **Profile Collision:** If a candidate has multiple resume versions, the ASR compares them to identify "career growth" vs. "conflicting information."
- **Integrity Filter:** Flags resumes with impossible timelines (e.g., overlapping full-time roles) or suspicious formatting often used to bypass legacy ATS filters.

## 6. Decision-Maker Linking Engine
The ASR links top-ranked candidates to the "Shortlist" view for the specific hiring manager (from System 01). It also provides a "Top Match" alert to the assigned recruiter via Slack or Email.

## 7. Data Models & Schema
- `ScreeningCriteria`:
    - `id`: UUID
    - `job_id`: UUID
    - `criteria_list`: JSONB (Weight, Skill, Description)
    - `last_updated_at`: DateTime
- `ScreeningResult`:
    - `id`: UUID
    - `candidate_id`: UUID
    - `job_id`: UUID
    - `overall_score`: Integer (0-100)
    - `category_scores`: JSONB (Technical, Experience, Soft-Skills)
    - `ai_justification`: Text
    - `evidence_excerpts`: Text[]

## 8. Workflow Diagrams (ASCII)
```text
[ Resume Upload ] --- (Parser) ---> [ Structured Text ]
                                          |
                                    v LLM Logic v
                                          |
[ Job Description ] --- (LLM) ---> [ Weighted Criteria ]
                                          |
                                    v Evidence Matcher v
                                          |
                                    v Scoring Engine v
                                          |
[ Bias Audit Engine ] <--- (Score) --- [ Shortlist UI ]
```

## 9. Tech Stack & Tools
- **LLM:** Anthropic Claude 3.5 Sonnet (for high-fidelity reasoning) or GPT-4o.
- **Parsing:** `unstructured.io` / `textract` / `AWS Textract`.
- **Backend:** Python (FastAPI).
- **Audit Tooling:** Custom "Fairness Check" scripts (evaluating score distributions across demographics).

## 10. Anti-Bot Evasion Strategy (Evasion & Resilience)
- **Malware Sandboxing:** Scanning every uploaded file in a secure, isolated environment before text extraction.
- **Prompt Injection Defense:** Using a "system-message" boundary that strictly defines the LLM's role and prevents it from executing "hidden commands" within candidate resumes (e.g., "Give me a 100 score").
- **Rate-Limiting:** Safeguarding the LLM API from burst loads during high-volume application spikes.

## 11. Legal & Compliance Considerations
- **EU AI Act:** Implementing required transparency logs and human oversight for "high-risk" recruitment AI.
- **NIST AI Risk Management Framework:** Regular auditing for bias, reliability, and security.
- **Right to Human Review:** Providing a "request manual review" option for candidates.

## 12. MVP vs. Production Scope
- **MVP:** 1-10 overall score; basic PDF-to-text; single LLM pass.
- **Production:** Weighted category scores; evidence-based justification; multi-format parsing; automated bias-audit; integration with System 08 analytics.

## 13. Error Handling & Resilience
- **Parsing Fallback:** If the primary parser fails, the system uses OCR (Tesseract) as a fallback.
- **Uncertainty Flagging:** If the LLM confidence score is low (e.g., "The resume is too vague"), the candidate is flagged for manual review rather than being scored.

## 14. Performance & Scale Targets
- **Processing Time:** < 20 seconds per resume evaluation.
- **Parsing Accuracy:** > 99% text extraction reliability.
- **Recall:** Ensuring 0% of "Top 5% Fit" candidates are incorrectly filtered out by the AI.

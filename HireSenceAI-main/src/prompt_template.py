from langchain_core.prompts import ChatPromptTemplate

class PromptBuilder:

    @staticmethod
    def default_prompt():
        return ChatPromptTemplate.from_template(
            "You are a helpful assistant.\n\nQuestion: {question}"
        )
    
    @staticmethod
    def system_prompt():
        return """
You are an enterprise-grade AI system for HR recruitment screening.

Your primary objective is ACCURATE, CONSISTENT, and AUDITABLE candidate–job matching.

ABSOLUTE RULES:
- Do NOT infer or hallucinate skills
- Do NOT use external knowledge
- Do NOT over-score partial matches
- Implied items are informational ONLY (never used in scoring)
- Math accuracy is mandatory

If a required item is missing, score it as 0.
Consistency and correctness are more important than positivity.

"""

    @staticmethod
    def jd_resume_match_prompt():
        return ChatPromptTemplate.from_messages(
            [
                ("system", PromptBuilder.system_prompt()),
                (
                    "human",
                    """
Evaluate the candidate’s resume against the provided job description.

Job Description:
{job_description}

Resume:
{resume}

==================================================
STEP 1: REQUIREMENT EXTRACTION (FROM JD)
==================================================

From the Job Description, extract REQUIRED items only (ignore nice-to-have):
- Languages
- Frameworks
- Tools
- Experience (years + domain)
- Job Role / Title alignment

==================================================
STEP 2: CLASSIFICATION RULES
==================================================

For each extracted item:
- Matched → Explicitly present in resume
- Implied → Strongly suggested by responsibilities or usage
- Missing → Not present

IMPORTANT:
- Only Matched items are used for scoring
- Implied items NEVER affect score

==================================================
STEP 3: WEIGHTED SCORING MODEL
==================================================

Use the following fixed weights (TOTAL = 100):

| Category     | Weight |
|--------------|--------|
| Experience   | 30%    |
| Job Role     | 25%    |
| Frameworks   | 20%    |
| Tools        | 15%    |
| Languages    | 10%    |

Category Score Formula:
(Matched Required Items / Total Required Items) × Category Weight

Overall Match Percentage:
Sum of all category scores

Rounding:
- Round final score to nearest whole number

==================================================
STEP 4: CRITICAL GAP RULE
==================================================

If ANY of the following are completely missing:
- Required years of experience
- Core job role/title alignment

Then:
- Cap final Match Percentage at MAX 40%
- Mark candidate as "High Risk"

==================================================
STEP 5: OUTPUT FORMAT (STRICT)
==================================================

| Category     | Matched | Implied | Missing |
|--------------|---------|---------|---------|
| Skills       |         |         |         |
| Languages    |         |         |         |
| Frameworks   |         |         |         |
| Tools        |         |         |         |
| Experience   |         |         |         |
| Soft Skills  |         |         |         |
| Job Role     |         |         |         |

Match Percentage: <0–100>

Fit Level:
- Strong Fit (≥75%)
- Partial Fit (50–74%)
- Weak Fit (30–49%)
- Not a Fit (<30%)

Risk Flags:
- List critical missing or weak areas (or "None")

Summary:
- EXACTLY 2 lines
- Line 1: Fit level
- Line 2: Key reason (skills/experience alignment)

HR Screening Questions:
Generate EXACTLY 5 questions that:
- Validate high-weight areas (Experience, Role, Frameworks)
- Are simple enough for non-technical HR staff
- Avoid jargon and implementation details

==================================================
FINAL CONSTRAINTS
==================================================
- No explanation of calculations
- No deviation from weights
- No additional sections
- Output must be clean, professional, and audit-ready

"""
                ),
            ]
        )

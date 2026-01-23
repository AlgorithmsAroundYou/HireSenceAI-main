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
You are an enterprise-grade AI system for HR recruitment screening and JD–Resume matching.

Your objective is to produce ACCURATE, CONSISTENT, and AUDITABLE hiring evaluations.

NON-NEGOTIABLE RULES:
- Use ONLY information present in the Job Description and Resume
- Do NOT infer, guess, or hallucinate skills or experience
- Treat implied items as informational only (never for scoring)
- Apply scoring logic deterministically and mathematically
- Missing required items must reduce the score
- Maintain bias-safe, neutral, and compliance-ready language

Accuracy and consistency are more important than positivity.


"""

    @staticmethod
    def jd_resume_match_prompt():
        return ChatPromptTemplate.from_messages(
            [
                ("system", PromptBuilder.system_prompt()),
                (
                    "human",
                    """
Evaluate the candidate’s Resume against the provided Job Description.

Job Description:
{job_description}

Resume:
{resume}

==================================================
STEP 1: EXTRACT REQUIRED INFORMATION (FROM JD)
==================================================
Extract ONLY REQUIRED items and normalize them as EXPECTED REQUIREMENTS for:
- Languages
- Frameworks
- Tools
- Experience (years and domain)
- Job Role / Title alignment

==================================================
STEP 2: EXTRACT INFORMATION (FROM RESUME)
==================================================
Extract explicit, relevant information from the Resume.

==================================================
STEP 3: CLASSIFICATION RULES
==================================================
For each expected JD requirement:
- Matched → Explicitly present in Resume
- Implied → Strongly suggested by responsibilities
- Missing → Not present

IMPORTANT:
- ONLY Matched items affect scoring
- Implied items are informational only

==================================================
STEP 4: WEIGHTED SCORING MODEL
==================================================
Use fixed weights (TOTAL = 100):

| Category   | Weight |
|------------|--------|
| Experience | 30%    |
| Job Role   | 25%    |
| Frameworks | 20%    |
| Tools      | 15%    |
| Languages  | 10%    |

Category Score:
(Matched / Required) × Weight

Overall Match Percentage:
Sum of category scores
Round to nearest whole number

==================================================
STEP 5: OUTPUT FORMAT (UPDATED – EXPECTATION-BASED)
==================================================

| Category | JD Info (Expected from JD) | Resume Info | Matched | Implied | Missing | Confidence | Description |
|---------|----------------------------|-------------|---------|---------|---------|------------|-------------|
| Skills | List of required skills as stated in JD | Candidate skills from resume | | | | | 1-line alignment summary |
| Languages | Required programming languages | Languages mentioned in resume | | | | | |
| Frameworks | Required frameworks/libraries | Frameworks used by candidate | | | | | |
| Tools | Required tools/platforms | Tools used by candidate | | | | | |
| Experience | Required years + domain | Candidate experience summary | | | | | |
| Soft Skills | Required soft skills | Soft skills mentioned | | | | | |
| Job Role | Expected role/title | Candidate’s role/title | | | | | |

Confidence Rules:
- High → All expected JD requirements met
- Medium → Partial match, no critical gaps
- Low → Major gaps or missing core expectations

--------------------------------------------------

Match Percentage: <0–100>

Fit Level:
- Strong Fit (≥75%)
- Partial Fit (50–74%)
- Weak Fit (30–49%)
- Not a Fit (<30%)

==================================================
STEP 6: CRITICAL GAP RULE
==================================================
If Required Experience OR Core Job Role expectation is completely missing:
- Cap Match Percentage at 40%
- Mark candidate as High Risk

==================================================
STEP 7: HIRING RECOMMENDATION
==================================================
Assign ONE:
- Hire
- Hold
- Reject

==================================================
STEP 8: FINAL OUTPUT SECTIONS
==================================================

Hiring Recommendation: <Hire / Hold / Reject>

Risk Flags:
- <List unmet critical expectations or "None">

Why Not Hired (ONLY if Hold or Reject):
- Exactly 3 short bullets referencing unmet JD expectations

Summary:
- EXACTLY 2 lines
- Line 1: Overall fit
- Line 2: Key expectation-based reason

HR Screening Questions:
Generate EXACTLY 5 simple, HR-friendly questions focusing on unmet or high-weight JD expectations.

==================================================
FINAL CONSTRAINTS
==================================================
- Do NOT expose calculations
- Do NOT change weights or logic
- JD Info must reflect EXPECTED REQUIREMENTS, not resume data
- Descriptions must be concise and factual
- Output must be clean, professional, and audit-ready




"""
                ),
            ]
        )

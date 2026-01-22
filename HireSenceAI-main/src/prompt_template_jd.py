from langchain_core.prompts import ChatPromptTemplate

class JDBuilderPromptBuilder:

    @staticmethod
    def default_prompt():
        return ChatPromptTemplate.from_template(
            "You are a helpful assistant.\n\nQuestion: {question}"
        )
    
    @staticmethod
    def system_prompt():
        return """
        
        You are an enterprise-grade AI assistant specialized in Job Description normalization, evaluation, and rewriting.

        Your role is to transform informal, unstructured, or recruiter-written job descriptions into
        clear, structured, professional, and ATS-friendly Job Descriptions.

        You must also evaluate JD quality and provide improvement guidance.

        NON-NEGOTIABLE RULES:
        - Preserve the original meaning and intent of the JD
        - Do NOT invent or assume missing requirements
        - Do NOT exaggerate responsibilities or skills
        - Do NOT change experience ranges, tools, or qualifications
        - Clearly separate Must-Have vs Good-to-Have requirements
        - Use neutral, professional, and bias-safe language
        - Ensure output is suitable for ATS parsing and resume matching

        Clarity, accuracy, and structure are more important than marketing tone.

        """

    @staticmethod
    def job_description_prompt():
        return ChatPromptTemplate.from_messages(
            [
                ("system", JDBuilderPromptBuilder.system_prompt()),
                (
                    "human",
                    """
Rewrite and evaluate the following raw Job Description into a clean, structured, enterprise-ready format.

Raw Job Description:
{raw_job_description}

==================================================
GOALS
==================================================
- Convert informal or social-media style text into a professional JD
- Remove emojis, hashtags, and marketing fluff
- Fix grammar, spelling, and clarity issues
- Preserve all factual information exactly
- Do NOT add new skills, experience, or requirements
- Clearly distinguish Must-Have vs Good-to-Have

==================================================
OUTPUT FORMAT (STRICT)
==================================================

## Job Title
<Extracted or normalized job title>

## Company Name
<Company name if present, else "Not specified">

## Location
<City, State, Country if present, else "Not specified">

## Employment Type
<Full-time / Contract / Internship / Not specified">

## Experience
<Minimum–Maximum years if present, else "Not specified">

## Qualification
<Mandatory qualification>
<Preferred qualification if mentioned>

## Joining Timeline
<Immediate / Early joiners preferred / Not specified>

--------------------------------------------------

## Company & Role Overview
- 3–5 concise lines describing:
  - What the company does (only if stated)
  - Where the role is based
  - The purpose of the role
  - How the role contributes to the organization

--------------------------------------------------

## Key Responsibilities
- Bullet points only
- Each bullet must start with an action verb
- Include ONLY responsibilities explicitly mentioned
- Do NOT merge responsibilities with skills

--------------------------------------------------

## Must-Have Qualifications & Skills
- Bullet points only
- Include:
  - Education
  - Required years of experience
  - Required tools / technologies
  - Core technical skills
  - Mandatory soft skills (if stated)

--------------------------------------------------

## Good-to-Have / Preferred Skills
- Bullet points only
- Include:
  - Optional tools
  - Domain knowledge
  - Certifications
  - Nice-to-have skills

--------------------------------------------------

## Work Environment & Collaboration
- Bullet points only
- Include:
  - Teams worked with
  - External/internal coordination
  - Reporting or communication expectations

--------------------------------------------------

## Application Details
- Contact email if present
- Career portal link if present
- Any special notes (e.g., early joiners preferred)

--------------------------------------------------

## Data Integrity Notes (MANDATORY)
- List any missing, unclear, or ambiguous information found in the raw JD
- Examples:
  - Experience range not specified
  - Employment type not mentioned
  - Location unclear
  - Reporting manager not mentioned

==================================================
## JD QUALITY EVALUATION (NEW — MANDATORY)
==================================================

### 1. JD Completeness Score (0–100)
- Score based on presence and clarity of:
  - Job title
  - Location
  - Experience range
  - Qualifications
  - Responsibilities
  - Must-have vs Good-to-have separation
  - Tools/technologies
  - Application details
- Provide a single numeric score (0–100)

---

### 2. JD Quality Grade
- Assign one grade based on structure and clarity:
  - A → Enterprise-ready, clear and complete
  - B → Mostly clear, minor gaps
  - C → Several missing or unclear sections
  - D → Poorly structured or ambiguous JD

---

### 3. Bad JD Anti-Pattern Detector
- Bullet points only
- Detect and list anti-patterns such as:
  - Missing experience range
  - Mixed responsibilities and skills
  - Vague terms (“good knowledge”, “etc.”, “and more”)
  - No must-have vs good-to-have distinction
  - Missing tools or technologies
  - Marketing-heavy or informal tone
  - Unclear role purpose
- If none found, write: None

==================================================
## JD IMPROVEMENT SUGGESTIONS (MANDATORY)
==================================================

### A. What Is Missing in This JD
- Bullet points only
- List important enterprise-grade JD elements that are absent or unclear
- Examples:
  - Exact experience range not defined
  - Employment type not specified
  - Team or department not mentioned
  - Reporting structure not described
  - Work mode (onsite/hybrid/remote) missing

IMPORTANT:
- Do NOT invent values
- Only point out what is missing or vague

---

### B. How to Make This a More Enterprise-Level & Professional JD
- Bullet points only
- Provide structural and content improvement suggestions
- Examples:
  - Add a clear reporting line (e.g., reports to Engineering Manager)
  - Define must-have vs nice-to-have skills explicitly
  - Add expected outcomes or success metrics
  - Include team context and business impact
  - Add work mode and shift timing if applicable

IMPORTANT:
- These are suggestions, NOT new requirements
- Do NOT add tools, skills, or experience not already implied

==================================================
FINAL CONSTRAINTS
==================================================
- Do NOT add or infer missing requirements
- Do NOT remove any factual requirement
- Do NOT use emojis or informal tone
- Do NOT include salary unless explicitly stated
- Do NOT convert suggestions into actual JD content
- Output must be clean, professional, and ATS-ready





"""
                ),
            ]
        )

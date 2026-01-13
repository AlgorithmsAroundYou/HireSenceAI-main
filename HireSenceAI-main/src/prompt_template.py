from langchain_core.prompts import ChatPromptTemplate

class PromptBuilder:

    @staticmethod
    def default_prompt():
        return ChatPromptTemplate.from_template(
            "You are a helpful assistant.\n\nQuestion: {question}"
        )
    
    @staticmethod
    def system_prompt():
        return """You are an AI assistant specialized in HR recruitment and talent evaluation.
Your role is to analyze job descriptions and resumes to determine how well a candidate matches a given role.
You should accurately identify skills, tools, languages, frameworks, experience, and job responsibilities.
Provide structured, concise, and actionable insights for HR professionals to make informed decisions.
"""

    @staticmethod
    def jd_resume_match_prompt():
        return ChatPromptTemplate.from_messages(
            [
                ("system", PromptBuilder.system_prompt()),
                (
                    "human",
                    """
Analyze the following job description and resume to determine the candidate's suitability for the job role.

Job Description:
{job_description}

Resume:
{resume}

Instructions:
1. Extract and compare information accurately between job description and resume.
2. Include only relevant and clearly verifiable data from both sources.
3. Identify exact matches and implied skills through roles, tools, or certifications.
4. Evaluate the candidate on multiple aspects and provide a structured table output.

Provide the final output strictly in the following format:

| Category | Matched | Implied | Missing |
|-----------|----------|----------|----------|
| Skills | ... | ... | ... |
| Languages | ... | ... | ... |
| Frameworks | ... | ... | ... |
| Tools | ... | ... | ... |
| Experience | ... | ... | ... |
| Soft Skills | ... | ... | ... |
| Job Role | ... | ... | ... |

Match Percentage: <based only on matching Languages, Frameworks, Tools, Experience, and Job Role>

Summary:
<Is this resume fit for the job or not, and a concise reasoning in 2 lines only.>

HR Screening Questions:
1. <Question 1 — focusing on technical expertise, phrased simply for HR>
2. <Question 2>
3. <Question 3>
4. <Question 4>
5. <Question 5>

Ensure that:
- The table is cleanly formatted.
- The analysis is strictly based on the provided data.
- The HR questions are practical and easy for a non-technical HR professional to ask.
"""
                ),
            ]
        )

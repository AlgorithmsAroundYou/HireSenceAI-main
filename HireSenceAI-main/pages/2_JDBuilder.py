# Author: Sai Kumar Kodati

import streamlit as st
from src.jd_builder_sence import JDBuilderGenerateSence
from src.auth import require_auth

# -----------------------
# Route guard (SAFE)
# -----------------------
require_auth()

class JDBuilder:
    def __init__(self):
        self.page_title = "Agiliad HireSence"
        self.layout = "wide"
        self.jd_builder_sence = JDBuilderGenerateSence()

    def set_page_config(self):
        st.set_page_config(page_title=self.page_title, layout=self.layout)

    def display_header(self):
        st.markdown(
            "<h1 style='text-align: center;'>Agiliad HireSence Job Description Builder</h1>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<p style='text-align: center;'>Welcome to the Agiliad HireSence platform. "
            "Build your job descriptions effortlessly.</p>",
            unsafe_allow_html=True
        )
        st.markdown("---")

    def job_description_builder_input(self):
        st.subheader("Build Job Descriptions")
        job_description_input = st.text_area(
            "Paste raw or draft Job Description here",
            key="job_description_input",
            height=400
        )
        return job_description_input

    def job_description_builder_instructions(self):
        st.subheader("Job Description Guidelines")
        st.info("""
Create a Job Description using the following mandatory sections and rules.

SECTION 1: Job Header
- Job Title
- Company Name
- Location (City, State, Country)
- Employment Type (Full-time / Contract / Internship)
- Experience Range (e.g., 1–3 Years)
- Qualification (Minimum + Preferred)
- Joining Timeline (e.g., Immediate / Early Joiners Preferred)

SECTION 2: Company & Role Overview
- 3–5 lines describing:
  - What the company does
  - Where the role is based
  - The purpose of the role
  - How the role contributes to the organization

SECTION 3: Key Responsibilities
- Bullet points only
- Each bullet must start with an action verb
- Include only job-relevant responsibilities

SECTION 4: Must-Have Qualifications & Skills
- Educational qualification
- Required years of experience
- Required tools / software
- Core technical skills
- Mandatory soft skills (if any)

SECTION 5: Good-to-Have / Preferred Skills
- Optional tools
- Domain knowledge
- Certifications
- Nice-to-have skills

SECTION 6: Work Environment & Collaboration
- Teams worked with
- Internal/external coordination
- Cross-functional exposure
- Reporting expectations

SECTION 7: Application Details
- Contact email or career portal link
- Application instructions
- Special notes (if any)
""")

    def display_output(self, submitted, job_description_output):
        st.markdown("---")
        st.subheader("Output")
        if submitted:
            st.write(job_description_output)
            st.markdown("---")

    def run(self):
        self.set_page_config()
        self.display_header()

        job_description_input = self.job_description_builder_input()
        submitted = st.button("Generate Job Description")

        self.job_description_builder_instructions()

        if submitted:
            if not job_description_input.strip():
                st.warning("Please paste a job description first.")
                return

            with st.spinner("Analyzing and generating hiring insights..."):
                job_description_output = self.jd_builder_sence.generate_hire_sence(
                    raw_job_description=job_description_input
                )

            st.success("✅ Job Description generated successfully!")
            self.display_output(submitted, job_description_output)


# -----------------------
# Page entrypoint
# -----------------------
jd_builder = JDBuilder()
jd_builder.run()

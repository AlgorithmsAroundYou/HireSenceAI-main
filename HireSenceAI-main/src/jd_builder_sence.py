
from src.prompt_template_jd import JDBuilderPromptBuilder
from src.gemini_lang_chain_wrapper import GeminiLangChainWrapper
from src.openai_lang_chain_wrapper import OpenAILangChainWrapper

class JDBuilderGenerateSence:

    def __init__(self):
        print("🧠 Generating Job Description...")
        self.prompt = JDBuilderPromptBuilder.job_description_prompt()
        # self.gemini = GeminiLangChainWrapper(self.prompt)
        self.openai = OpenAILangChainWrapper(self.prompt)     

    def generate_hire_sence(self, raw_job_description):
        """Generate a hiring scene based on job description and resume."""
        inputs = {}
        inputs["raw_job_description"] = raw_job_description
        # Generate the hiring scene
        result = self.openai.run(inputs)
        print(result)
        return result
        #print("🧠 Hiring scene generated successfully!")

import os
from turtle import st
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

class GeminiLangChainWrapper:

    def __init__(self, prompt_template):
        load_dotenv()
        # os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_GEMINI_API_KEY")

        api_key = st.secrets.get("GOOGLE_GEMINI_API_KEY") or os.getenv("GOOGLE_GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GOOGLE_GEMINI_API_KEY is not set")

        os.environ["GOOGLE_GEMINI_API_KEY"] = api_key

        self.model="models/gemini-2.5-flash"
        
        self.llm = ChatGoogleGenerativeAI(
            model=self.model,
            temperature=0.7,
            convert_system_message_to_human=True
        )
        self.chain = prompt_template | self.llm

    def run(self, inputs: dict) -> str:
        try:
            response = self.chain.invoke(inputs)
            return response.content
        except Exception as e:
            return f"Error: {e}"

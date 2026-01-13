
import os
import logging
from turtle import st
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import streamlit as st

class OpenAILangChainWrapper:

    def __init__(self, prompt_template):
        load_dotenv()

        api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set")

        os.environ["OPENAI_API_KEY"] = api_key

        #os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
        self.model="gpt-3.5-turbo-16k"  # or any other model you prefer
        
        self.llm = ChatOpenAI(
            model=self.model,
            temperature=0.7,
            api_key=api_key
        )
        self.chain = prompt_template | self.llm

    def run(self, inputs: dict) -> str:
        try:
            response = self.chain.invoke(inputs)
            return response.content
        except Exception as e:
            logging.error(f"Error in OpenAILangChainWrapper.run: {e}")
            return ""

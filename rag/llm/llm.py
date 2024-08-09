import os
import json
from openai import OpenAI
from zhipuai import ZhipuAI
from groq import Groq
from rag.utils import logger
from dotenv import load_dotenv

class LLMGenerator:
    def __init__(self) -> None:
        self.llm_name = os.getenv('LLM_NAME')
        if self.llm_name == 'OpenAI':
            api_key = os.getenv('API_KEY')
            self.client = OpenAI(api_key=api_key)
            self.model_name = os.getenv('MODEL_NAME')
        elif self.llm_name == 'Groq':
            api_key = os.getenv('API_KEY')
            self.client = Groq(api_key=api_key)
            self.model_name = os.getenv('MODEL_NAME')
        elif self.llm_name == 'ZhipuAI':
            api_key = os.getenv('API_KEY')
            self.client = ZhipuAI(api_key=api_key)
            self.model_name = os.getenv('MODEL_NAME')
        elif self.llm_name == 'Ollama':
            ollama_base_url = os.getenv('OLLAMA_BASE_URL')
            self.client = OpenAI(
                base_url = f"{ollama_base_url}/v1",
                api_key='ollama', # required, but unused
            )
            self.model_name = os.getenv('MODEL_NAME')
        elif self.llm_name == 'DeepSeek':
            api_key = os.getenv('API_KEY')
            self.client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com/v1")
            self.model_name = os.getenv('MODEL_NAME')
        else:
            raise ValueError(f"Unsupported LLM_NAME: '{self.llm_name}'. Must be in['OpenAI', 'ZhipuAI', 'Ollama', 'DeepSeek', 'Groq]")

    def generate(self, query: str, is_streaming: bool = False, is_json: bool = False):
        PROMPT = os.getenv("TEMPLATE")
        query = PROMPT.format(query)
        if is_streaming:
            if self.llm_name in ['OpenAI', 'Ollama', 'DeepSeek', 'Groq']:
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": query}],
                    temperature=0,
                    top_p=0.7,
                    stream=True
                )
            elif self.llm_name == 'ZhipuAI':
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": query}],
                    temperature=0.1,
                    top_p=0.7,
                    stream=True
                )
            return response
        else:
            if self.llm_name in ['OpenAI', 'Ollama', 'DeepSeek', 'Groq']:
                if is_json:
                    response = self.client.chat.completions.create(
                        model=self.model_name,
                        response_format={"type": "json_object"},
                        messages=[{"role": "user", "content": query}],
                        temperature=0,
                        top_p=0.7,
                        stream=False
                    )
                else:
                    response = self.client.chat.completions.create(
                        model=self.model_name,
                        messages=[{"role": "user", "content": query}],
                        temperature=0,
                        top_p=0.7,
                        stream=False
                    )
            elif self.llm_name == 'ZhipuAI':
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": query}],
                    temperature=0.1,
                    top_p=0.7,
                    stream=False
                )
            return response


llm_generator = LLMGenerator()

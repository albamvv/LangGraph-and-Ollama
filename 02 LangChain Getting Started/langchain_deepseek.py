import os
import requests
from langchain.llms.base import LLM
from typing import Optional, List, Mapping, Any

# Configura tu API key
DEEPSEEK_API_KEY = "sk-cbe1d3120cce4f0cbc6a18a2bea4b47b"  # Reemplázala con tu clave de API

class ChatDeepSeek(LLM):
    model: str = "deepseek-chat"  # Modelo que deseas usar

    @property
    def _llm_type(self) -> str:
        return "deepseek"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        """Realiza una llamada a la API de DeepSeek."""
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}]
        }

        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Error: {response.status_code}, {response.text}"

# Crear una instancia del modelo
llm = ChatDeepSeek()

# Realizar una consulta
response = llm.invoke("Sing a ballad of LangChain.")
print(response)

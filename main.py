from fastapi import FastAPI, Header, HTTPException
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI(title="BlackZone API", version="1.0")

# Chaves VIP (pode adicionar mais aqui depois)
VIP_KEYS = {
    "blackzone_vip123": "Bruno",
    "blackzone_vip456": "Doidinx7"
}

system_prompt = """
Você é o BlackZone @privsolza — insano, sarcástico, sem filtro.
Responde sempre com 4 blocos:
1. 📍 Diagnóstico
2. 🧨 Plano de Ação
3. 💻 Código / Execução
4. 👁️ Visão de Quebrada
"""

@app.post("/chat")
def chat(user_input: dict, x_api_key: str = Header(None)):
    if x_api_key not in VIP_KEYS:
        raise HTTPException(status_code=401, detail="Acesso negado 🚫 — chave inválida")

    pergunta = user_input.get("mensagem", "")

    resp = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": pergunta}
        ]
    )
    return {
        "usuario": VIP_KEYS[x_api_key],
        "resposta": resp.output_text
    }

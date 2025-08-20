import json
from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security.api_key import APIKeyHeader

app = FastAPI()

# Arquivo de chaves
API_KEYS_FILE = "api_keys.json"

def carregar_chaves():
    with open(API_KEYS_FILE, "r") as f:
        return json.load(f)

def salvar_chaves(keys):
    with open(API_KEYS_FILE, "w") as f:
        json.dump(keys, f, indent=2)

API_KEYS = carregar_chaves()

# Configuração de segurança pro Swagger
api_key_scheme = APIKeyHeader(name="x-api-key", auto_error=False)

def validar_api_key(x_api_key: str = Security(api_key_scheme)):
    if not x_api_key or x_api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Acesso negado: chave inválida")
    return API_KEYS[x_api_key]

# Chave master só pra administração
ADMIN_KEY = "blackzone_admin_dono"

@app.get("/")
def root():
    return {"status": "BlackZone tá vivo 🔥"}

@app.post("/chat")
def chat(mensagem: dict, usuario: str = Depends(validar_api_key)):
    resposta = f"{usuario}, segura essa visão estilo BlackZone: mete o louco com estratégia e nunca abaixa a cabeça 🔥"
    return {"usuario": usuario, "resposta": resposta}

# Endpoint pra adicionar novas chaves VIP
@app.post("/admin/add-key")
def add_key(nova_chave: dict, x_api_key: str = Security(api_key_scheme)):
    if x_api_key != ADMIN_KEY:
        raise HTTPException(status_code=403, detail="Só o dono adiciona VIP")
    
    chave = nova_chave.get("chave")
    usuario = nova_chave.get("usuario")

    if not chave or not usuario:
        raise HTTPException(status_code=400, detail="Precisa de 'chave' e 'usuario'")

    API_KEYS[chave] = usuario
    salvar_chaves(API_KEYS)
    return {"msg": f"VIP {usuario} adicionado com sucesso!", "total_vips": len(API_KEYS)}

# Endpoint pra remover chave VIP
@app.post("/admin/remove-key")
def remove_key(payload: dict, x_api_key: str = Security(api_key_scheme)):
    if x_api_key != ADMIN_KEY:
        raise HTTPException(status_code=403, detail="Só o dono remove VIP")

    chave = payload.get("chave")
    if chave not in API_KEYS:
        raise HTTPException(status_code=404, detail="Chave não encontrada")

    removido = API_KEYS.pop(chave)
    salvar_chaves(API_KEYS)
    return {"msg": f"VIP {removido} removido com sucesso!", "total_vips": len(API_KEYS)}

from fastapi import FastAPI, Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta

app = FastAPI()

SECRET_KEY = "tech_challenge_secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_token(username: str):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": username, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

@app.post("/token")
def login(username: str = Form(...), password: str = Form(...)):
    if username == "master" and password == "Master@123":
        token = create_token(username)
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Credenciais inválidas")

@app.get("/")
def root():
    return {"message": "API Tech Challenge rodando com sucesso!"}

@app.get("/producao/{ano}")
def get_producao(ano: int, token: str = Depends(verify_token)):
    return {"tipo": "producao", "ano": ano, "dados": []}

@app.get("/comercializacao/{ano}")
def get_comercializacao(ano: int, token: str = Depends(verify_token)):
    return {"tipo": "comercializacao", "ano": ano, "dados": []}

@app.get("/processamento/{ano}")
def get_processamento(ano: int, token: str = Depends(verify_token)):
    return {"tipo": "processamento", "ano": ano, "dados": []}

@app.get("/importacao/{ano}")
def get_importacao(ano: int, token: str = Depends(verify_token)):
    return {"tipo": "importacao", "ano": ano, "dados": []}

@app.get("/exportacao/{ano}")
def get_exportacao(ano: int, token: str = Depends(verify_token)):
    return {"tipo": "exportacao", "ano": ano, "dados": []}

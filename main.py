from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from datetime import datetime, timedelta

app = FastAPI()

SECRET_KEY = "tech_challenge_secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def criar_token(usuario: str):
    expiracao = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dados = {"sub": usuario, "exp": expiracao}
    return jwt.encode(dados, SECRET_KEY, algorithm=ALGORITHM)


def validar_token(token: str = Depends(oauth2_scheme)):
    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")


@app.post("/token")
def login(dados: OAuth2PasswordRequestForm = Depends()):
    if dados.username == "master" and dados.password == "Master@123":
        token = criar_token(dados.username)
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Credenciais incorretas")


@app.get("/producao/{ano}")
def producao(ano: int, _: str = Depends(validar_token)):
    return {"tipo": "producao", "ano": ano, "dados": []}


@app.get("/comercializacao/{ano}")
def comercializacao(ano: int, _: str = Depends(validar_token)):
    return {"tipo": "comercializacao", "ano": ano, "dados": []}


@app.get("/processamento/{ano}")
def processamento(ano: int, _: str = Depends(validar_token)):
    return {"tipo": "processamento", "ano": ano, "dados": []}


@app.get("/importacao/{ano}")
def importacao(ano: int, _: str = Depends(validar_token)):
    return {"tipo": "importacao", "ano": ano, "dados": []}


@app.get("/exportacao/{ano}")
def exportacao(ano: int, _: str = Depends(validar_token)):
    return {"tipo": "exportacao", "ano": ano, "dados": []}

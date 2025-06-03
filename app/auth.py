from datetime import datetime, timedelta
import jwt
from fastapi import HTTPException

SECRET_KEY = "segredo_super_secreto"
ALGORITHM = "HS256"

def criar_token(usuario: str):
    expira = datetime.utcnow() + timedelta(hours=2)
    dados = {"sub": usuario, "exp": expira}
    return {"access_token": jwt.encode(dados, SECRET_KEY, algorithm=ALGORITHM), "token_type": "bearer"}

def verificar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(401, detail="Token inválido")
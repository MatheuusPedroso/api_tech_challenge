# API Embrapa Vitivinicultura

## Autenticação
1. Faça POST para `/token` com:
   - `usuario`: user
   - `senha`: pass

2. Use o token retornado no header:
   `Authorization: Bearer <token>`

## Endpoints

### GET /dados/{tipo}?ano=YYYY
Tipos disponíveis:
- producao
- comercializacao
- processamento
- importacao
- exportacao

Exemplo:
curl -X GET \
  "http://api.example.com/dados/producao?ano=2020" \
  -H "Authorization: Bearer seu_token"
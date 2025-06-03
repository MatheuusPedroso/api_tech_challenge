import requests
from bs4 import BeautifulSoup
from datetime import datetime

def pegar_dados_embrapa(tipo: str, ano: int):
    map_urls = {
        'producao': 'opt_02',
        'comercializacao': 'opt_03',
        'processamento': 'opt_04',
        'importacao': 'opt_05',
        'exportacao': 'opt_06'
    }

    if tipo not in map_urls:
        raise ValueError("Tipo de dado não suportado")

    url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao={map_urls[tipo]}"

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        tabela = soup.find('table', {'id': 'tbDados'})

        if not tabela:
            return {"erro": "Dados não encontrados"}

        dados = []
        for linha in tabela.find_all('tr')[1:]:
            cols = linha.find_all('td')
            if len(cols) >= 2:
                item = {
                    'produto': cols[0].text.strip(),
                    'quantidade': cols[1].text.strip()
                }
                if len(cols) > 2:
                    item['unidade'] = cols[2].text.strip()
                dados.append(item)

        return {
            'tipo': tipo,
            'ano': ano,
            'dados': dados,
            'fonte': 'Embrapa',
            'atualizado_em': datetime.now().isoformat()
        }

    except requests.exceptions.RequestException as e:
        raise Exception(f"Erro ao acessar Embrapa: {str(e)}")
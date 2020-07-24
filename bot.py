from random import choice
from time import sleep

import lxml.html as parser
import requests
from igninterage import Igninterage

"""
    ### Ign ign Bot demo by Psychodynae - 21/07/2020 ###
    
    Demo de um Bot que responde a tópicos no fórum ign.
    
    O dicionario abaixo e uma demo simples, o ideal seria carregar a arvore de palavras de um arquivo
    json ou ainda um db sqlite:
    
"""
# import json
# with open('palavras.json', encoding='utf-8') as json_file:
#    estrutura = json.load(json_file)

estrutura_demo = {
    "palavras_chave": [
        {
            "modo": "todas",
            "excluir": [],
            "chave": ["qual", "lvl"],
            "resposta": ["full equip lvl 20 no max", "gostosa", "lvl 100"]
        },
        {
            "modo": "qualquer",
            "excluir": ['455552966'],
            "chave": ["ze sims", "zelão", "jose sims", "jose"],
            "resposta": ["abre o boção", "potchi leva modera"]
        },
        {
            "modo": "todas",
            "excluir": [],
            "chave": ["duro", "golpe"],
            "resposta": ["nada mais pode ser feito", "RIP"]
        },
        {
            "modo": "todas",
            "excluir": [],
            "chave": ["avaliem"],
            "resposta": ["penta", "mono", "avaliando com estrelas"]
        }
    ]
}


ign = Igninterage('cache.session', 'https://www.ignboards.com/')
session = requests.Session()

ign.ign_login()


def bot(dicionario):
    req = session.get('https://www.ignboards.com/forums/vale-tudo.80331/')
    html = req.text
    tree = parser.fromstring(html)
    threads = tree.find_class('structItem-title')

    for thread in threads:
        palavras = thread.values()[1][9:-11].split('-')
        thread_id = thread.values()[1][-10:-1]

        for cada in dicionario['palavras_chave']:
            modo = cada['modo']
            cada_chave = cada['chave']
            nao_responder = cada['excluir']

            if thread_id in nao_responder:
                continue

            if modo == 'todas':
                check = all(item in palavras for item in cada_chave)
            elif modo == 'qualquer':
                check = any(item in palavras for item in cada_chave)
            else:
                continue

            if check:
                print(choice(cada['resposta']), thread_id)
                try:
                    ign.comentar(choice(cada['resposta']), thread_id)
                except Exception as e:
                    print(e)
                    print('tentar novamente ?')


if __name__ == '__main__':
    while True:
        print('rodando...')
        bot(estrutura_demo)
        sleep(60)

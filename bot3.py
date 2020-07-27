import pickle
import sqlite3
from random import choice
import time

import lxml.html as parser
from igninterage import Igninterage
from igninterage import exceptions as ex

"""
   ### Ign Bot3 Demo by Psychodynae - 27/07/2020 ###

   Bot que responde a perguntas ao ser mencionado em qulquer post ex:

   @Bot que horas sao
"""

# BONUS! testado com sucesso no forum adrenaline.

estrutura_demo = {
    "palavras_chave": [
        {
            "modo": "action",
            "chave": ["horas", "horas?", "que horas são?", "que horas são", "diga as horas"],
            "resposta": ["horas"]
        },
        {
            "modo": "random",
            "chave": ["oi", "ola", "olá", "dae", "beleza"],
            "resposta": ["sim", "oi amigo", "dae meu consagrado", "dae meu relacionado"]
        },
        {
            "modo": "random",
            "chave": ["piada", "conte uma piada"],
            "resposta": ["piu", "piada 1", "piada 2"]
        },
        {
            "modo": "random",
            "chave": ["foto"],
            "resposta": ["[IMG]https://picsum.photos/200/300[/IMG]"]
        },
        {
            "modo": "random",
            "chave": ["aqui-eduardo", "aquieduardo", "aqui eduardo"],
            "resposta": ["cada dia mais c@gado, curto demais. -aqui-eduardo332323416",
                         "Amorecos No verão, com o calor, as fezes tendem a suar e a feder muito amorecos certamente irei vomitar e peidar demais chorei. -aqui-eduardo332323416",
                         "Nada melhor que chegar em casa amores e achar 3 kilos de fezes alta a loira em cima da cama de calcinha querendo fazer amor. -aqui-eduardo332323416",
                         "Quero ficar bombadão pois quero que as fezes, em banheiros públicos, saiam das privadas e peçam meu telefone amorecos. -aqui-eduardo332323416",
                         "amorecos fiz uma fezes nesse momento é novinha. -aqui-eduardo332323416",
                         "aveia podre e vencida com fungos nas bordas com aveia com cheiro de ovo podre amorecos depois perco alguma tripa na privada. -aqui-eduardo332323416",
                         "Chorando demais amores. -aqui-eduardo332323416",
                         "fezes, curto amorecos. -aqui-eduardo332323416"]
        }
    ]

}


def get_horas():
    from datetime import datetime
    hora = datetime.now()
    return hora.strftime('Agora são: %H:%M')


def actions(acoes):
    for acao in acoes:
        if acao == 'horas':
            return get_horas()


def save_cache_file(content, f_name):
    pickle.dump(content, open(f_name, 'wb'))


def load_cache_file(f_name):
    return pickle.load(open(f_name, 'rb'))


class Bot3:
    # _url = 'https://adrenaline.com.br/forum/' # BONUS! testado com sucesso no forum adrenaline.
    _url = 'https://www.ignboards.com/' 

    def __init__(self, cache_session_file, cache_file, tempo_de_loop=60):
        self.ign = Igninterage(cache_session_file, self._url)
        # self.ign.xenforo2_login('miuser', 'mypass') # BONUS! testado com sucesso no forum adrenaline.
        self.ign.ign_login()
        self.cache_file = cache_file
        while True:
            print('rodando...')
            self.responde()
            time.sleep(tempo_de_loop)

    def get_mention(self):
        html = self.ign.interact_session.get(self._url + 'account/alerts').content
        tree = parser.fromstring(html)
        alerts = tree.find_class('contentRow-main contentRow-main--close')
        mention_uris = []
        for alert in alerts:
            msg_text = alert.xpath('text()')[1]
            if 'men' in msg_text:
                mention_uris.append(alert.xpath('a/@href')[1])
        return mention_uris

    def ultimo_respondido_cache(self):
        try:
            return load_cache_file(self.cache_file)
        except FileNotFoundError:
            return 0

    def get_quem_te_mencionou(self):
        responder_list = []
        mention_list = self.get_mention()
        for item in reversed(mention_list):
            int_post_id = int(item.split('/')[-2])
            ultimo_respondido = self.ultimo_respondido_cache()
            if int_post_id > ultimo_respondido:
                save_cache_file(int_post_id, self.cache_file)
                responder_list.append(item)
        return responder_list

    def procura_posts(self):
        mentions = self.get_quem_te_mencionou()
        post_mentions = []
        for mention in mentions:
            mention = 'posts' + mention.split('posts')[1]
            html = self.ign.interact_session.get(self._url + mention).content
            tree = parser.fromstring(html)
            post_id = mention.split('/')[-2]
            xpath_user = f'//*[@id="js-post-{post_id}"]'
            xpath_text = f'{xpath_user}/div/div[2]/div/div[1]/div/article/div[1]'
            my_username = tree.find_class('p-navgroup-linkText')[0].text_content()
            thread = tree.find_class('block-container lbContainer')[0].attrib['data-lb-id'].split('-')[1]
            user = tree.xpath(xpath_user)[0].attrib['data-author']
            text = tree.xpath(xpath_text)[0].text_content().replace(f'@{my_username}', '').strip().lower()
            post_mentions.append([thread, post_id, user, text])
        return post_mentions

    def responde(self):
        perguntas = self.procura_posts()
        for pergunta_list in perguntas:
            thread, post, user, pergunta = pergunta_list
            for cada in estrutura_demo['palavras_chave']:
                modo = cada['modo']
                cada_chave = cada['chave']
                respostas = cada['resposta']
                if modo == 'random':
                    check = any(item in pergunta for item in cada_chave)
                    if check:
                        try:
                            full_resp = f'[QUOTE="{user}, post: {post}"]{pergunta}[/QUOTE]{choice(respostas)}'
                            self.ign.comentar(full_resp, thread)
                            time.sleep(20)
                        except (ConnectionError, ex.LoginError, ex.NotXenforoPage) as err:
                            print(err)
                            print('tentar novamente ?')

                if modo == 'action':
                    check = any(item in pergunta for item in cada_chave)
                    if check:
                        resp = actions(respostas)
                        if resp:
                            full_resp = f'[QUOTE="{user}, post: {post}"]{pergunta}[/QUOTE]{resp}'
                            try:
                                self.ign.comentar(full_resp, thread)
                                time.sleep(20)
                            except (ConnectionError, ex.LoginError, ex.NotXenforoPage) as err2:
                                print(err2)
                                print('tentar novamente ?')
                else:
                    continue


if __name__ == '__main__':
    cache_da_sessao = 'ign_cache.session'
    cache_mecao_respondida = 'ign_cache.mention'
    
    try:
        print('A ultima mecao respondida foi:', load_cache_file(cache_mecao_respondida))
    except FileNotFoundError:
        print(cache_mecao_respondida, 'ainda nao foi criado')

    # atualize esse numero com o ultima mecao respondida na pagina https://www.ignboards.com/account/alerts caso
    # necessario. use a funcao save_cache_file abaixo:
    # save_cache_file('123456789', cache_mecao_respondida')

    Bot3(cache_da_sessao, cache_mecao_respondida, tempo_de_loop=30)
    

import pickle
from time import sleep

import lxml.html as parser
from igninterage import Igninterage

"""
    ### Ign Bot2 Demo by Psychodynae - 24/07/2020 ###

    Bot que reage com um joinha ao ser mencionado

"""


def save_cache_file(content, f_name):
    pickle.dump(content, open(f_name, 'wb'))


def load_cache_file(f_name):
    return pickle.load(open(f_name, 'rb'))


class Bot2:
    def __init__(self, cachesession_file, cache_file, tempo_de_loop=60):
        self.ign = Igninterage(cachesession_file, 'https://www.ignboards.com/')
        self.ign.ign_login()
        self.cache_file = cache_file
        while True:
            print('rodando...')
            self.reage_no_post_de_quem_te_mencionou()
            sleep(tempo_de_loop)

    def procura_mention(self):
        html = self.ign.interact_session.get('https://www.ignboards.com/account/alerts').text
        tree = parser.fromstring(html)
        alerts = tree.find_class('contentRow-main contentRow-main--close')
        mention_uris = []
        for alert in alerts:
            msg_text = alert.xpath('text()')[1]
            if ('mentioned' or 'mencionou') in msg_text:
                mention_uris.append(alert.xpath('a/@href')[1])
        return mention_uris

    def ultimo_respondido_cache(self):
        try:
            return load_cache_file(self.cache_file)
        except FileNotFoundError:
            return 0

    def reage_no_post_de_quem_te_mencionou(self):
        mention_list = self.procura_mention()
        for item in reversed(mention_list):
            int_post_id = int(item.split('/')[2])
            ultimo_respondido = self.ultimo_respondido_cache()
            if int_post_id > ultimo_respondido:
                print(f'Reagi ao post!: {int_post_id}')
                self.ign.react('1', str(int_post_id))
                save_cache_file(int_post_id, self.cache_file)
                

if __name__ == '__main__':
    bot2 = Bot2('cache.session', 'cache.mention', tempo_de_loop=30)

from time import sleep
from igninterage import Igninterage
from lxml.html import fromstring

MENSAGEM = '[MEDIA=twitter]1363989931736072192[/MEDIA]'  # A mensagem da MP
TOPICO = 'Viih tube pagando peitinho'  # titulo do topico
TEMPO = 30
COD_REC_CONF = 'cod_rec.conf'
URL = 'https://www.ignboards.com/'

ign = Igninterage(URL, navegador='chrome')
ign.ign_login()


def load_conf(file):
    try:
        with open(file) as f:
            return f.read()
    except FileNotFoundError:
        return '0'


def save_conf(file, data):
    with open(file, 'w') as f:
        f.write(data)


def topico_data(id_post):
    html = ign.interact_session.get(f'{URL}/posts/{id_post}/').content
    tree = fromstring(html)
    xpath_user = f'//*[@id="js-post-{id_post}"]'
    xpath_text = f'{xpath_user}/div/div[2]/div/div[1]/div/article/div[1]'
    my_username = tree.find_class('p-navgroup-linkText')[0].text_content()
    user = tree.xpath(xpath_user)[0].attrib['data-author']
    text = tree.xpath(xpath_text)[0].text_content().replace(f'@{my_username}', '').strip().lower()
    return text, user, id_post


def codigo_request():
    html = ign.interact_session.get(URL + 'account/alerts').content
    tree = fromstring(html)
    alerts = tree.find_class('contentRow-main contentRow-main--close')
    post_ids = [alert.xpath('a/@href')[1].split('/')[-2] for
                alert in alerts if 'replied to the thread ' + TOPICO in alert.text_content()]

    pedidos = [topico_data(post_id) for post_id in reversed(post_ids) if
               int(post_id) > int(load_conf(COD_REC_CONF))]
    for pedido in pedidos:
        texto, nick, post_id = pedido
        save_conf(COD_REC_CONF, post_id)
        if texto == 'codigo request':
            ign.msg_privada('tá ná mão meu consagrado', MENSAGEM, nick, )
            sleep(TEMPO)
            return True


if __name__ == '__main__':
    while True:
        print('rodando...')
        if not codigo_request():
            sleep(TEMPO)

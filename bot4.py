import requests
from time import sleep
from igninterage import Igninterage

"""flood no tpc de imagens random"""

"""https://www.ignboards.com/threads/topico-das-imagens-randoms.455505695/"""

TOPICO = '455505695'
TEMPO = 200  # segundos


def gur():
    """ Retorna img random do imgur.
    """
    r = requests.get('https://imgur.com/random', timeout=7)
    uOut = f"{r.url.replace('gallery/', '')}.jpg"
    rs = requests.get(uOut)
    if len(rs.history) == 1:
        return uOut
    else:
        return gur()


def imgflood():
    ign = Igninterage('https://www.ignboards.com/')
    ign.ign_login()
    while True:
        try:
            g = gur()
            if g:
                ign.comentar(f'[img]{g}[/img]', TOPICO)
            else:
                print('erro ao recuperar imagem, continuando...')

        except Exception as err1:
            print(f'Erro, ih rapaz: {err1}. Tentando novamente...')

        sleep(TEMPO)


if __name__ == '__main__':
    #print(gur())
    imgflood()

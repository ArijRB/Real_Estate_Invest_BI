import requests
from lxml import html

# FONTION : Récupérer l'IP utilisé
def get_my_ip(session):
    ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'

    header = {
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control':'no-cache',
        'Connection':'keep-alive',
        'Host':'www.seloger.com',
        'Pragma':'no-cache',
        'Referer':'http://www.seloger.com/list.htm?tri=initial&idtypebien=2,1&idtt=2&ci=750101&naturebien=1,2,4',
        'X-Requested-With':'XMLHttpRequest',
        'User-agent': ua
    }

    ip_address = "Inconnu"

    try:
        ip = session.get('http://icanhazip.com', headers = header, timeout = 20)
        tree = html.fromstring(ip.content)
        ip_address = tree.xpath('/html/body/p/text()')[0]

        #html.open_in_browser(tree)
    except Exception as e:
        print("# ERREUR | Get my IP : ", e)

    #print('# INFO : Adresse IP utilisé : ', ip_address)

    return ip_address

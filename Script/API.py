from requests import get as GET
from colorama import init, Fore
from json import loads as LOAD
from bs4 import BeautifulSoup
import base64


def CrtSh_API(domain, proxy, C_Domain=[]):
    print(end=Fore.WHITE + "[ CrtSh  ] crt.sh API模块运行")
    for o in BeautifulSoup(GET(url=f"https://crt.sh/?q={domain}", proxies=proxy).content, 'html.parser').find_all('td'):
        C_Domain.append(o.string) if domain in str(o.string) and o.string not in C_Domain and f"Search: '{domain}'" not in o.string and '*' not in o.string and '@' not in o.string else 1
    print(Fore.GREEN + f'\r[ CrtSh  ]  获取域名 {len(C_Domain)} 个  <OKay>    ')
    return C_Domain


def SSLmate_Api(domain, proxy, S_Domain=[]):
    try:
        print(end=Fore.WHITE + "[ SSlmate] sslmate API模块运行")
        rest = GET(url='https://api.certspotter.com/v1/issuances', params={'domain': domain, 'include_subdomains': 'true', 'expand': 'dns_names'}, proxies=proxy).json()
        for i in rest:
            if len(i['dns_names']) == 1: S_Domain.append(i['dns_names'][0]) if '*' not in i['dns_names'][0] else 0
            else:
                for o in i['dns_names']: S_Domain.append(o) if '*' not in o else 0
    except: pass
    print(Fore.GREEN + f'\r[ SSlmate]  获取(子/同证书)域名 {len(S_Domain)} 个  <OKay>    ')
    return list(set(S_Domain))


def Hackert_Api(domain, proxy, H_Domain=[]):  # 需要挂代理
    try:
        print(end=Fore.WHITE + "[ HackerT] HackerTarget API模块运行")
        H_Domain = [i.split(',')[0] for i in GET(f"https://api.hackertarget.com/hostsearch/?q={domain}", proxies=proxy).content.decode().split('\n')]
    except: pass
    print(Fore.GREEN + f'\r[ HackerT]  获取域名 {len(H_Domain)} 个  <OKay>    ')
    return list(set(H_Domain))


def FOFA_Api(domain, proxy):
    try:
        print(end=Fore.WHITE + "[ FOFA   ] FOFA_API模块运行")
        with open('./config/fofa_key.ini', 'r', encoding='utf-8') as F: ini = LOAD(F.read())
        target = "{}/api/v1/search/all?email={}&key={}&qbase64={}&size={}&full=true".format(ini['api'], ini['email'], ini['key'], str(base64.b64encode(f"domain=\"{domain}\"".encode()), encoding='utf-8'), ini['size'])
        F_Domain = get_domain([i[0] for i in LOAD(GET(url=target, proxies=proxy).content)['results']])
        print(Fore.GREEN + f'\r[ FOFA   ]  获取域名 {len(F_Domain)} 个  <OKay>    ')
        return F_Domain
    except Exception as error:
        print(Fore.RED + f'\rERROR : {error}')
        return []


def get_domain(domain_list):
    domain_get = []
    for i in domain_list:
        try: domain_get.append(i.split('://')[1].split(':')[0])
        except: domain_get.append(i.split(':')[0])
    return list(set(domain_get))
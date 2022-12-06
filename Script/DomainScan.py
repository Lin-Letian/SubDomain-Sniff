from time import sleep as lsp
from colorama import Fore
from dns import resolver as dns


def domain_scan(domain, subdomains, wait='.', S_Domain=[]):  # 通过dns获取值方式进行爆破
    print(end=Fore.WHITE + "[ DNScan ] 爆破搜索模块运行")
    for i in subdomains:
        wait = '.' if len(wait) > 2 else wait
        try: dns.resolve(f"{i}.{domain}", 'A'), S_Domain.append(f"{i}.{domain}"), lsp(0)
        except: pass
        wait = wait + '.'
        print(end=Fore.YELLOW + f'\r[ DNScan ]  获取域名 {len(S_Domain)} 个{wait}  ')
    print(Fore.GREEN + f'\r[ DNScan ]  获取域名 {len(S_Domain)} 个  <OKay>    ')
    return S_Domain

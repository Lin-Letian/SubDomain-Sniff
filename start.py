import Script.API as api, Script.Domain as dom, Script.DomainScan as d_scan
from json import loads as LOAD
from time import sleep as lsp
from colorama import init, Fore

init()


# 2022.12.03
# 作者：林乐天
# https://birdy02.com
# https://www.birdy02.com/261558.htm
# 1. BaiDu(百度)搜索引擎进行子域名搜集
# 2. Bing(必应)搜索引擎进行子域名搜集
# 3. Google(谷歌)搜索引擎进行子域名搜集
# 4. crt.sh 进行子域名搜集
# 5. SSLmate_Api 进行子域名搜集
# 6. Hackertarget 进行子域名搜集
# 7. FOFA_Api 进行子域名搜集
# 8. dns子域名爆破

def run(domain, GetDomain=set()):
    with open('./config/proxy.ini') as F: proxy = LOAD(F.read())
    with open('./config/baidu_cookie.ini') as F: baidu_Cookie = F.read()
    with open('./config/google_cookie.ini') as F: google_Cookie = F.read()
    with open('./config/subdomain.dict') as F: subdomains = [i for i in F.read().split('\n')]
    for i in dom.Baidu_Search(domain, proxy, baidu_Cookie): GetDomain.add(i)
    for i in dom.Bing_Search(domain, proxy): GetDomain.add(i)
    for i in dom.Google_Search(domain, proxy, google_Cookie): GetDomain.add(i)
    for i in api.CrtSh_API(domain, proxy): GetDomain.add(i)
    for i in api.Hackert_Api(domain, proxy): GetDomain.add(i)
    for i in api.FOFA_Api(domain, proxy): GetDomain.add(i)
    if isdomain == 'y':
        for i in d_scan.domain_scan(domain, subdomains): GetDomain.add(i)
    for i in api.SSLmate_Api(domain, proxy): GetDomain.add(i)
    domains, Odomain = format_domain(GetDomain), []
    print(Fore.YELLOW + '\n[Sniff]数据整理'), lsp(2)
    for i in domains: print(Fore.WHITE + "[*] " + i) if i.endswith(domain) else Odomain.append(i)
    for i in Odomain: print(Fore.YELLOW + "[!] 同证书域名" + i)
    print(Fore.WHITE + f"[Sniff]本次运行获取域名{len(domains)}个\n")


def format_domain(domains, newlist=[]):
    for i in domains: newlist.append(i.split('://')[1]) if '://' in i else newlist.append(i)
    return list(set(newlist))


if __name__ == '__main__':
    print(Fore.BLUE + '''
    2022.12.03
    作者：林乐天
    https://birdy02.com
    https://www.birdy02.com/261558.htm
    1. BaiDu(百度)搜索引擎进行子域名搜集
    2. Bing(必应)搜索引擎进行子域名搜集
    3. Google(谷歌)搜索引擎进行子域名搜集
    4. crt.sh 进行子域名搜集
    5. SSLmate_Api 进行子域名搜集
    6. Hackertarget 进行子域名搜集
    7. FOFA_Api 进行子域名搜集
    8. dns子域名爆破
    '''), print(Fore.GREEN + '[ Start ]')
    domain = input(Fore.WHITE + '[-] 请输入要扫描的(一、二...)级域名 : ')
    isdomainscan = input(Fore.WHITE + '[-] 是否要爆破子域名(y/n)默认y:')
    isdomain = 'y' if isdomainscan in ['y', 'Y', 'yes', 'ok', ''] else 'n'
    run(domain)
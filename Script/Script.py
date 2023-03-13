import random, base64
from bs4 import BeautifulSoup
from requests import get
from time import sleep as lsp
from dns import resolver as dns
from json import loads as LOAD
from colorama import Fore
import threading


class dom:
    def __init__(self, domain=None, proxy=None):  # 初始化获取参数并赋值，避免每次调用函数都要传参
        self.domain = domain
        self.proxy = proxy
        if self.domain != None and self.proxy != None: print(Fore.GREEN + '[*] Domain模块初始化成功')

    def Baidu_Search(self, cookie, i=1, wait='.', B_Domain=[]):
        # 百度搜索
        print(Fore.YELLOW + "[-] 百度搜索模块运行")
        while 1:  # 通过wile循环来获取所有查询结果
            try:
                wait = '.' if len(wait) > 5 else wait  # 等待
                result = get(url=f"https://www.baidu.com/s?wd=site:{self.domain}&pn={i * 9}",
                             headers=self.get_Header('baidu', cookie), proxies=self.proxy, timeout=5)
                Responses = BeautifulSoup(result.content, 'html.parser')
                # 百度每页返回9条结果，通过9*页数来获取下一页数据
                if "百度安全验证" in str(Responses):
                    print(Fore.RED + "\r[-] 百度Cookie失效或需验证,请打开以下链接手动验证后,重新配置Cookie")
                    print(result.request.url)
                    break
                for o in Responses.find_all('h3'):
                    if o.a.get('href').startswith('http'):  # 通过startswitch来判断href内容是否为http开头(是否为链接)
                        url = get(url=o.a.get('href'),
                                  headers=self.get_Header('baidu'),
                                  allow_redirects=False,
                                  proxies=self.proxy).headers['Location']  # 通过headers['location']获取跳转后的域名
                        link = url.split("://")[0] + '://' + url.split("://")[1].split('/')[0]  # 重新组合域名，去掉目录
                        B_Domain.append(link) if link not in B_Domain else False  # 判断链接是否存在于列表中，不存在则不添加
                    print(end=Fore.YELLOW + f'\r[-] Baidu->获取域名 {len(B_Domain)} 个{wait}    ')
                if len(Responses.find_all('h3')) < 10: break  # 判断返回内容小于10条时，结束运行
                i, wait = i + 1, wait + '.'  # 每次运行i+1保证页数增加
                lsp(2)
            except Exception as err:
                print(Fore.RED + f"[*] Baidu->Error::{err}")
                break
        print(Fore.GREEN + f'\r[*] Baidu->获取域名 {len(B_Domain)} 个  <OKay>    ')
        return B_Domain  # 返回获取的列表

    def Google_Search(self, cookie, wait='.', i=0, G_Domain=[]):
        print(Fore.YELLOW + "[-] 谷歌搜索模块运行")
        while True:
            try:
                wait = '.' if len(wait) > 5 else wait
                result = get(url=f'https://www.google.com/search?q=site:{self.domain}&num=10&start={i * 10}',
                             headers=self.get_Header('google', cookie), timeout=10, proxies=self.proxy)
                Responses, tmp = BeautifulSoup(result.content, 'html.parser'), []
                if "This page checks to see if it's really you sending the requests" in str(Responses):  # 判断Cookie是否可用
                    print(Fore.RED + "\r[-] 谷歌Cookie失效或需要验证,请打开以下链接手动验证后,重新配置Cookie")
                    print(result.request.url)
                    break
                for n in Responses.find_all('a'):
                    try:
                        if f'{self.domain}/' in n.get('href').split('url=')[1]:
                            link_1 = n.get('href').split('url=')[1].split('://')[0] + '://'
                            link_2 = n.get('href').split('://')[1].split('/')[0]
                            link = link_1 + link_2
                            tmp.append(link)
                    except:
                        pass
                [G_Domain.append(u) for u in tmp if u not in G_Domain]
                print(end=Fore.YELLOW + f'\r[-]  Google->获取域名 {len(G_Domain)} 个{wait}    ')
                if len(tmp) < 10: break
                i, wait = i + 1, wait + '.'
                lsp(2)
            except Exception as err:
                print(Fore.RED + f"[*] Google->Error::{err}")
                break
        print(Fore.GREEN + f'\r[*] Google->获取域名 {len(G_Domain)} 个  <OKay>    ')
        return G_Domain

    def Bing_Search(self, i=1, wait='.', B_Result=[]):
        print(Fore.YELLOW + "[-] 必应搜索模块运行")
        while True:
            try:
                wait = '.' if len(wait) > 5 else wait
                result, tmp = get(url=f"https://cn.bing.com/search?q=site:{self.domain}&first={i}&FORM=PERE2",
                                  headers=self.get_Header('bing'), timeout=10, proxies=self.proxy), []
                Responses = BeautifulSoup(result.content, 'html.parser').find_all('h2')  # 获取所有的h2标签
                for o in Responses:
                    link = o.a.get('href').split("://")[0] + "://" + o.a.get('href').split("://")[1].split("/")[0]
                    tmp.append(link)  # 对链接不去重，直接添加
                [B_Result.append(u) for u in tmp if u not in B_Result]
                print(end=Fore.GREEN + f'\r[*] Bing->获取域名 {len(B_Result)} 个{wait}    ')
                if len(Responses) < 10: break
                i, wait = i + 10, wait + '.'
                lsp(1)
            except Exception as err:
                print(Fore.RED + f"[*] Bing->Error::{err}")
                break
        print(Fore.GREEN + f'\r[*] Bing->获取域名 {len(B_Result)} 个  <OKay>    ')
        return B_Result

    def get_Header(self, switch=None, cookie=''):
        UA = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"]
        if switch == 'baidu':
            return {'User-Agent': random.choice(UA),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'Cookie': cookie, 'Referer': 'https://www.baidu.com'}
        elif switch == 'bing':
            return {'user-agent': random.choice(UA),
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'Host': 'cn.bing.com', 'Referer': 'https://www.bing.com'}
        elif switch == 'google':
            return {'user-agent': random.choice(UA),
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                    'Host': 'www.google.com', 'Referer': 'https://www.google.com', 'cookie': cookie}
        else:
            return {'User-Agent': random.choice(UA),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}


class api:
    def __init__(self, domain=None, proxy=None):
        self.domain = domain
        self.proxy = proxy
        self.dom = dom()
        if self.domain != None and self.proxy != None: print(Fore.GREEN + '[*] API模块初始化成功')

    def CrtSh(self, C_Domain=[]):
        print(Fore.YELLOW + "[-] API_CrtSh模块运行")
        try:
            for o in BeautifulSoup(get(url=f"https://crt.sh/?q={self.domain}",
                                       proxies=self.proxy, timeout=10,
                                       headers=self.dom.get_Header()).content, 'html.parser').find_all('td'):
                if self.domain in str(o.string) and o.string not in C_Domain and f"Search: '{self.domain}'" \
                        not in o.string and '*' not in o.string and '@' not in o.string:  # 排除条件
                    C_Domain.append(o.string)
        except:
            print(Fore.RED + f'\r[-] CrtSh->Error::目标不可达')
        print(Fore.GREEN + f'\r[*] CrtSh->获取域名 {len(C_Domain)} 个  <OKay>')
        return C_Domain

    def Hackert(self, H_Domain=[]):  # 需要挂代理
        print(Fore.YELLOW + "[-] API_HackerTarget模块运行")
        try:
            H_Domain = [i.split(',')[0] for i in get(f"https://api.hackertarget.com/hostsearch/?q={self.domain}",
                                                     proxies=self.proxy, timeout=10,
                                                     headers=dom.get_Header()).content.decode().split('\n') if
                        i.split(',')[0] not in H_Domain]
        except:
            print(Fore.RED + f'\r[-] HackerTarget->Error::目标不可达')
        print(Fore.GREEN + f'\r[*] HackerTarget->获取域名 {len(H_Domain)} 个  <OKay>')
        return list(set(H_Domain))

    def FOFA(self, ini):
        print(Fore.YELLOW + "[-] API_FOFA模块运行")
        try:
            target = f'''{ini['api']}/api/v1/search/all?email={ini['email']}&key={ini['key']}&qbase64={str(base64.b64encode(f'domain="{self.domain}"'.encode()), encoding='utf-8')}&size={ini['size']}&full=true'''
            F_Domain = self.get_domain_f([i[0] for i in LOAD(get(url=target, proxies=self.proxy).content)['results']])
            print(Fore.GREEN + f'\r[*] FOFA->获取域名 {len(F_Domain)} 个  <OKay>')
            return F_Domain
        except:
            print(Fore.RED + f'\r[-] FOFA->Error::网络不可达')
            return []

    def get_domain_f(self, domain_list):
        domain_get = []
        for i in domain_list:
            try:
                domain_get.append(i.split('://')[1].split(':')[0])
            except:
                domain_get.append(i.split(':')[0])
        return list(set(domain_get))

    def SSLmate(self, S_Domain=[]):
        print(Fore.YELLOW + "[-] API_sslmate模块运行")
        try:
            rest = get(url='https://api.certspotter.com/v1/issuances',
                       params={'domain': self.domain, 'include_subdomains': 'true', 'expand': 'dns_names'},
                       proxies=self.proxy).json()
            for i in rest:
                if len(i['dns_names']) == 1:
                    S_Domain.append(i['dns_names'][0]) if '*' not in i['dns_names'][0] else 0
                else:
                    for o in i['dns_names']: S_Domain.append(o) if '*' not in o else 0
        except:
            print(Fore.RED + "[-] SSLmate->Error::网络错误")
        print(Fore.GREEN + f'\r[*] SSlmate->获取(子/同证书)域名 {len(S_Domain)} 个  <OKay>')
        return list(set(S_Domain))


class domscan:
    def __init__(self, domain):
        self.domain = domain
        self.S_Domain = []

    def scan(self, subdomains,xc=1):  # 通过dns获取值方式进行爆破
        print(Fore.YELLOW + "[-] DNS爆破模块运行")
        SURI = [[] for N in range(xc)]  # 根据线程数分组
        [SURI[i % xc].append(e) for i, e in enumerate(subdomains)]  # 将总url根据线程平均分配
        [threading.Thread(target=self.threadScan, args=(SURI[i],)) for i in range(xc)]
        print(Fore.GREEN + f'\r[*] DNSScan->获取域名 {len(self.S_Domain)} 个  <OKay>')
        return self.S_Domain
    def threadScan(self,ulist):
        for i in ulist:
            try:
                dns.resolve(f"{i}.{self.domain}", 'A'), self.S_Domain.append(f"{i}.{self.domain}"), lsp(0.2)
            except:
                pass
            print(end=Fore.YELLOW + f'\r[-] DNSScan->获取域名 {len(self.S_Domain)} 个')

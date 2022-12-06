import random
from bs4 import BeautifulSoup
from requests import get as get
from time import sleep as lsp
from colorama import init, Fore


def Baidu_Search(domain, proxy, cookie, i=1, wait='.', B_Domain=[]):  # 百度搜索
    print(end=Fore.WHITE + "[ BaiDu  ] 百度搜索模块运行")
    while (1):  # 通过wile循环来获取所有查询结果
        try:
            wait = '.' if len(wait) > 5 else wait
            Responses = BeautifulSoup(get(url=f"https://www.baidu.com/s?wd=site:{domain}&pn={i * 9}", headers=get_Header('baidu', cookie), proxies=proxy).content, 'html.parser')
            # 百度每页返回9条结果，通过9*页数来获取下一页数据
            if "百度安全验证" in str(Responses): print(Fore.RED + "\r[ BaiDu  ] 百度Cookie失效或需验证")
            for o in Responses.find_all('h3'):
                if o.a.get('href').startswith('http'):  # 通过startswitch来判断href内容是否为http开头(是否为链接)
                    url = get(url=o.a.get('href'), headers=get_Header('baidu'), allow_redirects=False, proxies=proxy).headers['Location']  # 通过headers['location']获取跳转后的域名
                    link = url.split("://")[0] + '://' + url.split("://")[1].split('/')[0]  # 重新组合域名，去掉目录
                    B_Domain.append(link) if link not in B_Domain else False  # 判断链接是否存在于列表中，不存在则不添加
                print(end=Fore.YELLOW + f'\r[ BaiDu  ]  获取域名 {len(B_Domain)} 个{wait}  ')
            if len(Responses.find_all('h3')) < 10: break  # 判断返回内容小于10条时，结束运行
            i, wait = i + 1, wait + '.'  # 每次运行i+1保证页数增加
            lsp(1)
        except:
            print(end=Fore.CYAN + f"\r[ BaiDu  ] Slow network, exit or wait 5s {wait}  "), lsp(5)
            continue
    print(Fore.GREEN + f'\r[ BaiDu  ]  获取域名 {len(B_Domain)} 个  <OKay>    ')
    return B_Domain  # 返回获取的列表


def Bing_Search(domain, proxy, i=1, wait='.', B_Result=[]):
    print(end=Fore.WHITE + "[ Bing   ] 必应搜索模块运行")
    while (2):
        try:
            wait = '.' if len(wait) > 5 else wait
            Responses = BeautifulSoup(get(url=f"https://cn.bing.com/search?q=site:{domain}&first={i}&FORM=PERE2", headers=get_Header('bing'), timeout=10, proxies=proxy).content, 'html.parser').find_all('h2')
            for o in Responses:
                link = o.a.get('href').split("://")[0] + "://" + o.a.get('href').split("://")[1].split("/")[0]
                if link not in B_Result: B_Result.append(link)
                print(end=Fore.YELLOW + f'\r[ Bing   ]  获取域名 {len(B_Result)} 个{wait}  ')
            if len(Responses) < 10: break
            i, wait = i + 1, wait + '.'
            lsp(1)
        except:
            print(end=Fore.CYAN + f"\r[ Bing   ] site:{domain} , wait 5s ..."), lsp(5)
            continue
    print(Fore.GREEN + f'\r[ Bing   ]  获取域名 {len(B_Result)} 个  <OKay>    ')
    return B_Result


def Google_Search(domain, proxy, cookie, wait='.', i=0, G_Result=set()):
    print(end=Fore.WHITE + "[ Google ] 谷歌搜索模块运行")
    while (3):
        try:
            wait = '.' if len(wait) > 5 else wait
            Responses, tmp = BeautifulSoup(
                get(url=f'https://www.google.com/search?q=site:{domain}&num=10&start={i * 10}', headers=get_Header('google', cookie), timeout=10, proxies=proxy).content, 'html.parser'), []
            if "This page checks to see if it's really you sending the requests" in str(Responses): print(Fore.RED + "\r[ Google ] Google Cookie失效或需要其他验证")
            for n in Responses.find_all('a'):
                try: tmp.append(n.get('href').split('url=')[1]) if f'{domain}/' in n.get('href').split('url=')[1] else False
                except: pass
            for u in tmp: G_Result.add(u.split('://')[0] + '://' + u.split('://')[1].split('/')[0])
            print(end=Fore.YELLOW + f'\r[ Google ]  获取域名 {len(G_Result)} 个{wait}  ')
            if len(tmp) < 10: break
            i, wait = i + 1, wait + '.'
            lsp(2)
        except:
            print(Fore.RED + '\r[ Google ] There are one or more errors')
            break
    print(Fore.GREEN + f'\r[ Google ]  获取域名 {len(G_Result)} 个  <OKay>    ')
    return list(G_Result)


def get_Header(switch, cookie=''):
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
    if switch == 'baidu': return {'User-Agent': random.choice(UA), 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Cookie': cookie}
    elif switch == 'bing': return {'user-agent': random.choice(UA), 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
    elif switch == 'google': return {'user-agent': random.choice(UA), 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'cookie': cookie}
    else: return {'User-Agent': random.choice(UA), 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
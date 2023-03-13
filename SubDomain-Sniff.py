import base64
from bs4 import BeautifulSoup
from Script.Script import dom as domain, api, domscan
from json import loads as LOAD
import threading, re, os, sys, datetime, csv, time
from requests import head, get, post
from bs4 import BeautifulSoup as bs
from colorama import Fore, init

init()  # colorama.init()

banner = '''
------------------------------------------

    一键子域名收集工具
    2022.12.03
    作者：林乐天
    https://www.birdy02.com/261558.htm
    
    1. BaiDu(百度)搜索引擎进行子域名搜集
    2. Bing(必应)搜索引擎进行子域名搜集
    3. Google(谷歌)搜索引擎进行子域名搜集
    4. crt.sh 进行子域名搜集
    5. SSLmate_Api 进行子域名搜集
    6. Hackertarget 进行子域名搜集 # 需要挂VPN
    7. FOFA_Api 进行子域名搜集
    8. dns子域名爆破
    
------------------------------------------

'''


class initConf:  # 获取配置文件
    def __init__(self):
        print(Fore.YELLOW + "[*] 获取配置文件")
        self.proxy = self.getproxy()  # 获取proxy
        self.fofa_key = self.getfofakey()  # 获取FOFA key
        tmp_cookie = self.getcookie()
        self.baiduCookie = tmp_cookie[0]  # 获取baidu Cookie
        self.googleCookie = tmp_cookie[-1]  # 获取google Cookie

    def getproxy(self):  # 获取代理并检测代理是否可以使用
        print(Fore.YELLOW + "[*] 读取代理配置信息")
        with open('./config/proxy.ini') as F:
            try:
                proxy = LOAD(F.read())
            except:
                TmpP = F.read().split(':\\\\')
                proxy = {TmpP[0]: TmpP[-1]} if ':\\' in F.read() else {}
        if len(proxy) > 0:  # 判断是否获取到代理信息
            print(Fore.YELLOW + "[-] 获取到{}, 进行可以用性检测.".format(proxy))
            try:
                get(url='https://www.google.com', proxies=proxy)  # 通过访问谷歌检测是否可出网
                print(Fore.GREEN + f"[*] 成功访问到外网,测试网址 https://www.google.com")
            except:
                print(Fore.YELLOW + "[-] 代理/网络 不可用, 本次运行将不使用代理")
                proxy = {}
        else:
            print(Fore.YELLOW + "[*] 检测到未(或正确)配置代理, 本次运行将不使用代理")
        return proxy

    def getfofakey(self):  # 获取FOFA配置并检测是否可用
        print(Fore.YELLOW + "[*] 读取FOFA配置文件")
        try:
            with open('./config/fofa_key.ini') as F:
                fofa_key = LOAD(F.read())  # 将配置格式化为json
                print(Fore.YELLOW + "[-] 获取到{}, 进行可用性测试".format(fofa_key))
                target = f'''{fofa_key['api']}/api/v1/search/all?email={fofa_key['email']}&key={fofa_key['key']}&qbase64={str(base64.b64encode(f'domain="www.birdy02.com"'.encode()), encoding='utf-8')}&size={fofa_key['size']}&full=true'''
                try:
                    result = LOAD(get(target, proxies=self.proxy).text)  # 尝试请求并获取返回值
                    if not result['error']:  # 根据返回json中的error值判断是否存在配置信息的错误
                        print(Fore.GREEN + f'[*] 测试获取返回结果{len(result["results"])}条,可用性测试成功 √')
                    else:  # 当配置错误时将fofa_key赋值为空
                        print(Fore.RED + f'[×] {result["errmsg"]}' + Fore.WHITE)
                        fofa_key = {}
                except:
                    print(Fore.RED + '[×] 网络不可达')
                    fofa_key = {}  # 出现错误时，将fofa_key赋值为空
        except:
            fofa_key = {}
        if len(fofa_key) != 4: print(Fore.YELLOW + "[-] fofa配置错误或其他问题, 将不调用fofa模块")
        return fofa_key

    def getcookie(self):
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        }
        print(Fore.WHITE + '[*] 获取Cookie信息')
        print(end=Fore.YELLOW + "[*] 读取Baidu Cookie配置")
        try:
            with open('./config/baidu_cookie.ini') as F:  # 获取Baidu Cookie
                baidu_Cookie = F.read()
                if len(baidu_Cookie.split(';')) > 1:
                    print(Fore.GREEN + '\r[*] Baidu Cookie 获取成功, 对Cookie可用性进行尝试')
                    head = header
                    head.update({'Host': 'www.baidu.com', 'Cookie': baidu_Cookie})
                    response = get(url=f"https://www.baidu.com/s?wd=site:www.birdy02.com&pn=0",
                                   proxies=self.proxy, headers=head, timeout=5)
                    if "百度安全验证" in str(BeautifulSoup(response.content, 'html.parser')):  # 判断是否存在验证
                        print(Fore.RED + "\r[-] 百度Cookie失效或需验证,请打开以下链接手动验证后,重新配置Cookie")
                        print(Fore.BLUE + response.request.url)
                        baidu_Cookie = []
                    else:
                        print(Fore.GREEN + '[*] Baidu Cookie可用')
        except Exception as e:
            print(Fore.RED + f'\r[×] 百度Cookie Error: {e}')
        print(end=Fore.YELLOW + "[*] 读取Google Cookie配置")
        try:
            with open('./config/google_cookie.ini') as F:  # 获取Google Cookie
                google_Cookie = F.read()
                if len(google_Cookie.split(';')) > 1:
                    print(Fore.GREEN + '\r[*] Google Cookie 获取成功, 对Cookie可用性进行尝试')
                    head = header
                    head.update({'Host': 'www.google.com', 'Cookie': google_Cookie})
                    result = get(url='https://www.google.com/search?q=site:birdy02.com&num=10&start=0',
                                 proxies=self.proxy, headers=head, timeout=10)
                    Responses = BeautifulSoup(result.content, 'html.parser')
                    if "This page checks to see if it's really you sending the requests" in str(Responses):
                        print(Fore.RED + "\r[-] 谷歌Cookie失效或需要其他验证,请打开以下链接手动验证后,重新配置Cookie")
                        print(Fore.BLUE + result.request.url)
                        google_Cookie = ''
                    else:
                        print(Fore.GREEN + '[*] Google Cookie可用')
        except Exception as e:
            print(Fore.RED + f'\r[×] 谷歌Cookie Error: {e}')
        return [baidu_Cookie, google_Cookie]

    def result(self):  # result方法获取返回值
        return {'proxy': self.proxy, 'fofa_key': self.fofa_key,
                'baidu_cookie': self.baiduCookie, 'google_cookie': self.googleCookie}


class URIstatus:
    def __init__(self, urls, xc, proxy):
        self.Ok = [['状态', '请求方法', 'URL', '标题']]  # 可访问、访问失败
        self.Err = [['状态', '请求方法', 'URL', '标题']]
        self.proxy = proxy
        print(Fore.GREEN + "\n\n[*] 运行URIstatus模块")
        print(Fore.YELLOW + f'[+] 线程数: {xc}')
        self.dirName = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        Threadlist = self.getUriList(urls, xc)  # 获取url列表并根据线程数进行分配列表
        print('[*] 初始化完成，多线程启动\n')
        print(Fore.WHITE + '|  Code | Method |\tTitle\t\t  |\tURL')
        print(Fore.WHITE + '—————————————————————————————————————')
        for i in Threadlist: i.start()
        for i in Threadlist: i.join()
        print(Fore.WHITE + '—————————————————————————————————————\n')
        self.write_csv()

    def getUriList(self, ulist, xc):  # 对URI的处理
        print(Fore.GREEN + f'[*] 开始url读取::获取{len(ulist)}条URI(第一次去重)')
        protocol = ['https://', 'http://', 'https:/', 'http:/', 'htps://', 'htp://', 'htps:/',  # 协议库
                    'htp:/', 'https:', 'http:', 'htps:', 'htp:', 'https//', 'https/', 'http//',  # 不可改变列表顺序
                    'http/', 'htps//', 'htps/', 'htp//', 'htp/', 'https', 'http', 'htps', 'htp']
        newUlist, nuri = [], None  # 去协议之后的新列表
        print(Fore.GREEN + "[*] 开始url处理::去除(不规则)协议,去重")
        for url in ulist:  # 获取单个url
            for prot in protocol:  # 循环获取协议
                nuri = re.sub(prot, '', url, re.I)  # 正则匹配掉协议
                if url != nuri: break  # 当匹配到协议后停止循环
            newUlist.append(nuri)
        newUlist = list(set(newUlist))  # 通过set()二次去重
        print(Fore.GREEN + "[*] 开始分配线程::根据线程分配url组")
        SURI = [[] for N in range(xc)]  # 根据线程数分组
        [SURI[i % xc].append(e) for i, e in enumerate(newUlist)]  # 将总url根据线程平均分配
        return [threading.Thread(target=self.judge_status, args=(SURI[i],)) for i in range(xc)]  # 线程列表

    def judge_status(self, Ulist):
        for url in Ulist:
            new_url = f'https://{url}'
            res = self.get_statuecode(new_url)
            if str(res[0]) != "000":
                print(Fore.WHITE + f"|  {res[0]}  |  {res[1]}  |  {res[-1][:10]}  |\t{new_url}")
                self.Ok.append(res)
            else:
                new_url = f'http://{url}'
                res = self.get_statuecode(new_url)
                if str(res[0]) != "000":
                    print(Fore.WHITE + f"|  {res[0]}  |  {res[1]}  |  {res[-1][:10]}  |\t{new_url}")
                    self.Ok.append(res)
                else:
                    print(Fore.RED + f"[ERR] 目标不可达:: {url}")
                    self.Err.append(url)

    def get_statuecode(self, url):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.39',
            'Referer': url, 'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"'
        }
        try:
            response = get(url=url, timeout=10, headers=self.headers, proxies=self.proxy)
            return [response.status_code, "GET ", url,
                    bs(response.content, 'html.parser').find('title').text.replace('\n', '').replace('\r', '')]
        except:
            try:
                response = post(url=url, timeout=10, headers=self.headers, proxies=self.proxy)
                return [response.status_code, "POST", url,
                        bs(response.content, 'html.parser').find('title').text.replace('\n', '').replace('\r', '')]
            except:
                try:
                    response = head(url=url, timeout=10, headers=self.headers, proxies=self.proxy)
                    return [response.status_code, "HEAD", url, '']
                except:
                    return ["000", None, '']

    def write_csv(self):
        print(Fore.GREEN + "[*] 正在保存结果")
        dir_path = f"output\\{self.dirName}"
        if os.path.exists(dir_path):  # 判断目录是否已经存在
            input(f"检测到 {dir_path} 目录已经存在,将删除该目录并重新创建，请确认：")
            try:  # 避免人工删除目录导致的报错
                os.rmdir(dir_path)  # 当目录存在时候
            except:
                pass
        if not os.path.exists(dir_path): os.mkdir(dir_path)  # 判断目录不存在时候进行创建
        if len(self.Ok) > 1:
            with open(f'{dir_path}\\Result_Ok.csv', 'w', newline="") as csvfile:
                spamwriter = csv.writer(csvfile, dialect='excel')
                for ok in self.Ok: spamwriter.writerow(ok)
        if len(self.Err) > 1:
            with open(f'{dir_path}\\Fail.csv', 'w', newline="") as csvfile:
                spamwriter = csv.writer(csvfile, dialect='excel')
                for fail in self.Err: spamwriter.writerow(fail)

        print(Fore.YELLOW + f"[-] 访问成功 {len(self.Ok) - 1} 个")
        print(Fore.YELLOW + f"[-] 访问失败 {len(self.Err) - 1} 个")
        print(Fore.YELLOW + f'[-] 输出文件保存至目录:: {os.getcwd()}\\{dir_path}')


class SubDm:  # 主程序
    def __init__(self):
        init = initConf()  # 配置初始化
        config = init.result()  # 获取配置返回值
        arg = self.getinput()  # 获取输入值
        dicts = 'config\\subdomain.dict'
        if arg['domainscan'] == 'y':
            try:
                with open(dicts) as F:
                    dicts = [f for f in F.read().split('\n') if f != '' and f not in dicts]
            except:
                sys.exit(Fore.RED + f"[-] Error::{dicts}文件丢失(子域名字典)")
        result = {}  # 定义字典获取返回结果
        dom = domain(domain=arg['domain'], proxy=config['proxy'])  # 初始化domain模块，并传入域名和代理
        if config['baidu_cookie'] != '':
            result.update({"Baidu": dom.Baidu_Search(cookie=config['baidu_cookie'])})  # Baidu_Search
        if config['google_cookie'] != '':
            result.update({"Google": dom.Google_Search(cookie=config['google_cookie'])})  # Google_Search
        result.update({"Bing": dom.Bing_Search()})  # Bing_Search
        Api = api(domain=arg['domain'], proxy=config['proxy'])  # 初始化api模块，并传入域名和代理
        result.update({"CrtSh": Api.CrtSh()})  # crt.sh
        result.update({"Hackert": Api.Hackert()})
        result.update({"FOFA": Api.FOFA(ini=config['fofa_key'])})
        result.update({"SSLmate": Api.SSLmate()})
        if arg['domainscan'] == 'y':  # 判断是否运行DNSScan模块
            domScan = domscan(domain=arg['domain'])
            result.update({"DNSScan": domScan.scan(subdomains=dicts, xc=arg['xc'])})
        if not os.path.exists('output'): os.mkdir('output')  # 确保输出路径不存在无异常
        links = []  # 创建列来合并所有模块所查询到的数据
        for i in result: [links.append(u) for u in result[i] if u not in links]
        if arg['isURIstatus'] == 'y':  # 判断是否执行URIstatus
            URIstatus(urls=links, xc=arg['xc'], proxy=config['proxy'])
        else:
            fname = f'output\\{time.time()}.txt'
            with open(fname, 'w') as F:
                [F.write(l + '\n') for l in links]
            print(Fore.WHITE + f'[*] 结果输出->{fname}')

    def getinput(self, ):
        while True:
            domain = input(Fore.WHITE + '\n[-] 请输入要扫描的(一、二...)级域名 : ')
            if len(domain.split('.')) > 1: break  # 当输入域名不合规时重新输入
        isdomainscan = input(Fore.WHITE + '\n[-] 是否要爆破子域名(y/n):')
        isdomain = 'y' if isdomainscan in ['y', 'Y', 'yes', 'ok', ''] else 'n'
        isURIstatus = input(Fore.WHITE + '\n[-] 是否要对所有子域名的可用性进行检测，使用URIstatus模块(y/n):')
        URIstatus = 'y' if isURIstatus in ['y', 'Y', 'yes', 'ok', ''] else 'n'
        xc = 1  # 声明默认线程变量
        if URIstatus == 'y':
            xc = input(Fore.WHITE + '\n[-] 请输入线程,线程越高,数据准确度会降低,建议[4-10],最大20,默认4线程:')
            try:
                xc = int(xc)  # 将输入线程转换为int类型，失败则默认4线程
                xc = xc if xc <= 20 else 20
            except:
                xc = 4
        return {'domain': domain, 'domainscan': isdomain, 'isURIstatus': isURIstatus, 'xc': xc}

    def __del__(self):
        print()
        while True:
            inp = input('输入exit退出:')
            if inp == 'exit': break


if __name__ == '__main__':
    print(Fore.WHITE + banner), print(Fore.GREEN + '[*] 初始化')
    SubDm()

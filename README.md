# SubDomain-Sniff
SubDomain Sniff-综合子域名嗅探工具，集成3个搜索引擎+4个API(包括SSL证书)+爆破子域名或关联域名

###########环境依赖

python版本：3.9.5

site-packages -> pip install -r requirements.txt

####无语子，格式出错，所以跨行写


作者：林乐天

https://birdy02.com

https://www.birdy02.com/261558.htm

BaiDu(百度)搜索引擎进行子域名搜集

Bing(必应)搜索引擎进行子域名搜集

Google(谷歌)搜索引擎进行子域名搜集

crt.sh 进行子域名搜集

SSLmate_Api 进行子域名搜集

Hackertarget 进行子域名搜集

FOFA_Api 进行子域名搜集

DNS子域名爆破


###########目录结构描述

├── Readme.md                   // help

├── start.exe                   // 应用=>exe

├── start.py                    // 应用=>py

├── config                      // 配置

│   ├── baidu_cookie.ini        // 百度Cookie

│   ├── fofa_key.ini            // FOFA_API_Key 

│   ├── google_cookie.ini       // 谷歌 Cookie

│   ├── proxy.ini               // 代理配置

│   ├── subdomain.dict          // 域名爆破字典

├── requirements.txt            // pip安装库

├── Script                      // 脚本

│   └── API.py                  // API

│   └── Domain.py.py            // 搜索引擎

│   └── DomainScan.py           // 域名爆破
![image](https://user-images.githubusercontent.com/81403750/205918698-68141ea0-033d-4672-a549-f734d0e73c27.png)

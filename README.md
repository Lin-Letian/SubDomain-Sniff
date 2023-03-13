# SubDomain-Sniff
SubDomain Sniff-综合子域名嗅探工具，集成3个搜索引擎+4个API(包括SSL证书)+爆破子域名或关联域名

###环境依赖

python版本：3.8.10

site-packages -> pip install -r requirements.txt


版本：2023.03.01

作者：林乐天

发布：https://www.birdy02.com/261558.htm

这是一个子域名收集的工具，开发目的为将资产收集阶段自动化

    1. BaiDu(百度)搜索引擎进行子域名搜集
    2. Bing(必应)搜索引擎进行子域名搜集
    3. Google(谷歌)搜索引擎进行子域名搜集
    4. crt.sh 进行子域名搜集
    5. SSLmate_Api 进行子域名搜集
    6. Hackertarget 进行子域名搜集
    7. FOFA_Api 进行子域名搜集
    8. dns子域名爆破


配置：
初始化只能对代理和FOFA key进行检测，cookie获取到即可，不会对可用性进行检测
1. config/proxy.ini

    代理的配置有两种设置方式，如：
    
        https://127.0.0.1:4780
        
        {"https":"127.0.0.1:4780"}
        
    都可以设置成功，其他形式暂未作适配

2. config/fofa_key.ini

    FOFA配置信息支支持json格式，格式如下：
    
        {
        
            "api" : "", # fofaApi地址 -> url带协议
            
            "email" : "", # FOFA绑定的邮箱
            
            "key" : "", # FOFA的key
            
            "size" : 1000 # 每次获取最大返回值的数量
            
        }
3. config/baidu_cookie.ini

    Baidu Cookie可以从浏览器的请求头中直接复制Cookie值即可，如:
    
        BAIDUID=xxxxx; xxxxx=xxxxx; xxx=xxxx;

4. config/google_cookie.ini

    Google Cookie可以直接从浏览器的请求头中复制Cookie值即可，如:
    
        HSID=xxxxx; xxxxx=xxxxx; xxx=xxxx;


###目录结构描述

├── Readme.md                   // help

├── SubDomain-Sniff.exe         // 应用=>exe

├── SubDomain-Sniff.py          // 应用=>py

├── config                      // 配置

│   ├── baidu_cookie.ini        // 百度Cookie

│   ├── fofa_key.ini            // FOFA_API_Key 

│   ├── google_cookie.ini       // 谷歌 Cookie

│   ├── proxy.ini               // 代理配置

│   ├── subdomain.dict          // 域名爆破字典

├── requirements.txt            // pip安装库

├── Script                      // 脚本

│   └── Script.py               // 脚本文件

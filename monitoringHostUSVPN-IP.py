#此程序功能：每30s访问google一次，若访问失败则会企业微信机器人报警，报警频率为20s一次，恢复访问则报警消失。
from urllib.request import urlopen
import urllib
import re
import json
import requests
import time

#代理地址
proxy = {
    'http':"http://127.0.0.1:1080"
}

# 定义函数，调用可发送消息到企业微信机器人
def qiye(errorStr):
    url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=dc7258e5-ddb4-4afd-a32e-277940fa5fea"
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    data_text = {
        "msgtype": "text",
        "text": {
            "content": errorStr  # 文本内容，最长不超过2048个字节，必须是utf8编码
        }
    }
    r = requests.post(url, data=json.dumps(data_text), headers=headers)
    return r.text

#无限循环监控
while 1:
    # 输出国内出口IP
    myURL1 = urlopen("http://ip111.cn")
    htmlContent1 = myURL1.read().decode()
    localip1 = re.search(r'(([01]{0,1}\d{0,1}\d|2[0-4]\d|25[0-5])\.){3}([01]{0,1}\d{0,1}\d|2[0-4]\d|25[0-5])', htmlContent1)
    print(time.ctime(time.time()), "上网正常，国内出口IP", localip1.group())


    # 输出国外测试IP，失败则调用企业微信提醒
    try:
        myURL2 = requests.get("http://sspanel.net/ip.php", proxies=proxy, headers={'Cache-Control': 'no-cache'},timeout=3)
        htmlContent2 = myURL2.content.decode()
        localip2 = re.search(r'(([01]{0,1}\d{0,1}\d|2[0-4]\d|25[0-5])\.){3}([01]{0,1}\d{0,1}\d|2[0-4]\d|25[0-5])', htmlContent2)
        x = 1
    except:
        x = 0
    finally:
        if(x == 1):
            print(time.ctime(time.time()), "谷歌正常，国外测试IP", localip2.group())
            time.sleep(3)
        elif(x == 0):
            print(time.ctime(time.time()), "谷歌测试IP访问失败")
            qiye(time.ctime(time.time()) + " ，海外VPN出故障啦")
            time.sleep(3)

        # 清除urlopen缓存
        urllib.request.urlcleanup()
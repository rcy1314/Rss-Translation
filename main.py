# coding:utf-8 
import configparser
from pygtrans import Translate
from bs4 import BeautifulSoup
import sys
import os
from urllib import request
import urllib
# pip install pygtrans -i https://pypi.org/simple
# ref:https://zhuanlan.zhihu.com/p/390801784
# ref:https://beautifulsoup.readthedocs.io/zh_CN/latest/
# ref:https://pygtrans.readthedocs.io/zh_CN/latest/langs.html
# client = Translate()
# text = client.translate('Google Translate')
# print(text.translatedText)  # 谷歌翻译
import hashlib
def get_md5_value(src):
    _m = hashlib.md5()
    _m.update(src.encode('utf-8'))
    return _m.hexdigest()
    
config = configparser.ConfigParser()
config.read('test.ini',encoding='utf-8')
secs=config.sections()



def get_cfg(sec,name):
    return config.get(sec,name).strip('"')

def set_cfg(sec,name,value):
    config[sec][name]='"%s"'%value

def get_cfg_tra(sec):
    cc=config.get(sec,"action").strip('"')
    target=""
    source=""
    if cc == "auto":
        source  = 'auto'
        target  = 'zh-CN'
        
         
    else:
        source  = cc.split('->')[0]
        target  = cc.split('->')[1]
    return source,target


# config['url']={'url':'www.baidu.com'} #类似于字典操作
 
# with open('example.ini','w') as configfile:
#     config.write(configfile)

BASE=get_cfg("cfg",'base')
try:
    os.makedirs(BASE)
except:
    pass
links=[]
def tran(sec):
    out_dir= BASE + get_cfg(sec,'name')
    url=get_cfg(sec,'url')
    max_item=int(get_cfg(sec,'max'))
    old_md5=get_cfg(sec,'md5')
    source,target=get_cfg_tra(sec)
    global links

    links+=[" - %s [%s](%s) -> [%s](%s)\n"%(sec,url,url,get_cfg(sec,'name'),out_dir)]


    GT = Translate()
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36 LBBROWSER'
        }
    req = urllib.request.Request(url, headers=headers)

 
    html_doc=request.urlopen(req).read().decode('utf8')
    new_md5= get_md5_value(html_doc)

    if old_md5 == new_md5:
        return
    else:
        set_cfg(sec,'md5',new_md5)
    # move style
    html_doc=html_doc.replace('<?', '</s')
    html_doc=html_doc.replace('?>', '/>')
    
    soup = BeautifulSoup(html_doc, 'html.parser')
    items=soup.find_all('item')
    for idx,e in enumerate(items):
        if idx >max_item:
                e.decompose()
    
    content= str(soup)
    
    content=content.replace('title>', 'stitle>')
    content=content.replace( '<pubdate>','<pubDate><span translate="no">')
    content=content.replace( '</pubdate>','</span></pubdate>')
    # print(content)
    
    
    _text = GT.translate(content,target=target,source=source)
    
    
    with open(out_dir,'w',encoding='utf-8') as f:
        c=_text.translatedText
        
        c=c.replace('stitle>', 'title>')
        c=c.replace('<span translate="no">', '')
        c=c.replace('</span></pubdate>', '</pubDate>') # 对于ttrss需要为pubDate才会识别正确
        c=c.replace('&gt','>') # &gt 会影响识别
        
        f.write(c)
        #print(c)
        #f.write(content)
    print("GT: "+ url +" > "+ out_dir)

for x in secs[1:]:
    tran(x)
    print(config.items(x))

with open('test.ini','w') as configfile:
    config.write(configfile)



YML="README.md"

f = open(YML, "r+", encoding="UTF-8")
list1 = f.readlines()           
list1= list1[:13] + links

f = open(YML, "w+", encoding="UTF-8")
f.writelines(list1)
f.close()
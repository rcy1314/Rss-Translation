import configparser
import os
import sys
from urllib import parse
import hashlib
import datetime
import time
from rss import RSS, Item
from bs4 import BeautifulSoup
from mtranslate import translate

def get_md5_value(src):
    _m = hashlib.md5()
    _m.update(src.encode('utf-8'))
    return _m.hexdigest()

def getTime(e):
    try:
        struct_time = e['published_parsed']
    except:
        struct_time = time.localtime()
    return datetime.datetime(*struct_time[:6])

def getSubtitle(e):
    try:
        sub = e.get('subtitle', '')
    except:
        sub = ""
    return sub

class BingTran:
    def __init__(self, url, source='auto', target='zh-CN'):
        self.url = url
        self.source = source
        self.target = target

        self.rss = RSS(url)

    def tr(self, content):
        return translate(content, to_language=self.target, from_language=self.source)

    def get_newcontent(self, max_item=2):
        item_list = []
        if len(self.rss.items) < max_item:
            max_item = len(self.rss.items)
        for item in self.rss.items[:max_item]:
            title = self.tr(item.title)
            link = item.link
            soup = BeautifulSoup(item.description, 'html.parser')
            content = self.tr(soup.get_text().strip())
            guid = item.guid
            pubDate = getTime(item)
            one = Item(title=title, link=link, content=content, guid=guid, pubDate=pubDate)
            item_list += [one]
        newrss = RSS(title=self.tr(self.rss.title), link=self.rss.link, description=self.tr(getSubtitle(self.rss.__dict__)), pubDate=self.rss.pubDate, items=item_list)
        return newrss.to_xml()

with open('test.ini', mode='r') as f:
    ini_data = parse.unquote(f.read())
config = configparser.ConfigParser()
config.read_string(ini_data)
secs = config.sections()

def get_cfg(sec, name):
    return config.get(sec, name).strip('"')

def set_cfg(sec, name, value):
    config[sec][name] = '"%s"' % value

def get_cfg_tra(sec):
    cc = config.get(sec, "action").strip('"')
    target = ""
    source = ""
    if cc == "auto":
        source = 'auto'
        target = 'zh-CN'
    else:
        source = cc.split('->')[0]
        target = cc.split('->')[1]
    return source, target

BASE = get_cfg("cfg", 'base')
try:
    os.makedirs(BASE)
except:
    pass
links = []

def tran(sec):
    out_dir = BASE + get_cfg(sec, 'name')
    url = get_cfg(sec, 'url')
    max_item = int(get_cfg(sec, 'max'))
    old_md5 = get_cfg(sec, 'md5')
    source, target = get_cfg_tra(sec)
    global links

    links += [" - %s [%s](%s) -> [%s](%s)\n" % (sec, url, (url), get_cfg(sec, 'name'), parse.quote(out_dir))]

    new_md5 = get_md5_value(url)

    if old_md5 == new_md5:
        return
    else:
        set_cfg(sec, 'md5', new_md5)

    c = BingTran(url, target=target, source=source).get_newcontent(max_item=max_item)

    with open(out_dir, 'w', encoding='utf-8') as f:
        f.write(c)

    print("BT: " + url + " > " + out_dir)

for x in secs[1:]:
    tran(x)
    print(config.items(x))

with open('test.ini', 'w') as configfile:
    config.write(configfile)

YML = "README.md"

f = open(YML, "r+", encoding="UTF-8")
list1 = f.readlines()
list1 = list1[:13] + links

f = open(YML, "w+", encoding="UTF-8")
f.writelines(list1)
f.close()

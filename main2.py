import configparser
from pygtrans import Translate
from bs4 import BeautifulSoup
import sys
import os
import hashlib
import datetime
import time
from rfeed import *
import feedparser
from urllib import request, parse


def get_md5_value(src):
    _m = hashlib.md5()
    _m.update(src.encode('utf-8'))
    return _m.hexdigest()


def getTime(e):
    try:
        struct_time = e.published_parsed
    except:
        struct_time = time.localtime()
    return datetime.datetime(*struct_time[:6])


def getSubtitle(e):
    try:
        sub = e.subtitle
    except:
        sub = ""
    return sub


class GoogleTran:
    def __init__(self, url, source='auto', target='zh-cn', item=None, **kwargs):
        self.url = url
        self.source = source
        self.target = target

        self.d = feedparser.parse(url)
        self.GT = Translate()

    def tr(self, content):
        tt = self.GT.translate(content, target=self.target, source=self.source)
        try:
            return tt.translatedText
        except:
            return ""

    def get_newcontent(self, max_item=2):
        item_list = []
        entries_len = len(self.d.entries)
        if entries_len < max_item:
            max_item = entries_len
        for entry in self.d.entries[:max_item]:
            summary = getattr(entry, 'summary', '')
            one = Item(title=self.tr(entry.title),
                       link=entry.link,
                       description=self.tr(summary),
                       guid=Guid(entry.link),
                       pubDate=getTime(entry))
            item_list += [one]
        feed = self.d.feed
        newfeed = Feed(title=self.tr(feed.title),
                       link=feed.link,
                       description=self.tr(getSubtitle(feed)),
                       lastBuildDate=getTime(feed),
                       items=item_list)
        return newfeed.rss()


config = configparser.ConfigParser()
config.read('test.ini')
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
    out_dir= BASE + get_cfg(sec,'name')
    url=get_cfg(sec,'url')
    max_item=int(get_cfg(sec,'max'))
    old_md5=get_cfg(sec,'md5')
    source,target=get_cfg_tra(sec)
    global links



    # 调用
    tran_result = GoogleTran(url, target=target, source=source).get_newcontent(max=max_item)

    links.append(" - %s [%s](%s) -> [%s](%s)\n" % (sec, url, (url), get_cfg(sec, 'name'), parse.quote(out_dir)))

    new_md5 = get_md5_value(url)

    if old_md5 == new_md5:
        return
    else:
        set_cfg(sec, 'md5', new_md5)

    with open(out_dir, 'w', encoding='utf-8') as f:
        f.write(tran_result)

    print("GT: " + url + " > " + out_dir)


for x in secs[1:]:
    tran(x)
    print(list(config.items(x)))

with open('test.ini', 'w') as configfile:
    config.write(configfile)

YML = "README.md"

with open(YML, 'r+', encoding="UTF-8") as f:
    list1 = f.readlines()
    list1 = list1[:13] + links

with open(YML, 'w+', encoding="UTF-8") as f:
    f.writelines(list1)

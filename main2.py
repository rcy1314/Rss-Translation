import configparser
from pygtrans import Translate
from bs4 import BeautifulSoup
import sys
import os
import hashlib
import datetime
import time
import feedparser
from rfeed import *
import urllib.parse

def get_md5_value(src):
    _m = hashlib.md5()
    _m.update(src.encode('utf-8'))
    return _m.hexdigest()

def get_time(e):
    try:
        struct_time = e.published_parsed
    except:
        struct_time = time.localtime()
    return datetime.datetime(*struct_time[:6])

def get_subtitle(e):
    try:
        sub = e.subtitle
    except:
        sub = ""
    return sub

class GoogleTran:
    def __init__(self, url, source='auto', target='zh-CN'):
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

    def get_new_content(self, max_items=2):
        item_list = []
        if len(self.d.entries) < max_items:
            max_items = len(self.d.entries)
        for entry in self.d.entries[:max_items]:
            one = Item(
                title=self.tr(entry.title),
                link=entry.link,
                description=self.tr(entry.summary),
                guid=Guid(entry.link),
                pubDate=get_time(entry)
            )
            item_list.append(one)
        feed = self.d.feed
        new_feed = Feed(
            title=self.tr(feed.title),
            link=feed.link,
            description=self.tr(get_subtitle(feed)),
            lastBuildDate=get_time(feed),
            items=item_list
        )
        return new_feed.rss()

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

def translate(sec):
    out_dir = BASE + get_cfg(sec, 'name')
    url = get_cfg(sec, 'url')
    max_items = int(get_cfg(sec, 'max'))
    old_md5 = get_cfg(sec, 'md5')
    source, target = get_cfg_tra(sec)
    global links

    links.append(" - %s [%s](%s) -> [%s](%s)\n" % (sec, url, url, get_cfg(sec, 'name'), urllib.parse.quote(out_dir)))

    new_md5 = get_md5_value(url)

    if old_md5 == new_md5:
        return
    else:
        set_cfg(sec, 'md5', new_md5)

    c = GoogleTran(url, target=target, source=source).get_new_content(max_items=max_items)

    with open(out_dir, 'w', encoding='utf-8') as f: 

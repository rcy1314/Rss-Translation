import configparser
import os
import sys
from urllib import parse
import hashlib
import datetime
import time
import feedparser
from bs4 import BeautifulSoup
from mtranslate import translate

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

class BingTran:
    def __init__(self, url, source='auto', target='zh-CN'):
        self.url = url
        self.source = source
        self.target = target

        self.d = feedparser.parse(url)

    def tr(self, content):
        return translate(content, to_language=self.target, from_language=self.source)

    def get_newcontent(self, max_item=2):
        item_list = []
        if len(self.d.entries) < max_item:
            max_item = len(self.d.entries)
        for entry in self.d.entries[:max_item]:
            title = self.tr(entry.title)
            link = entry.link
            description = self.tr(entry.summary)
            guid = entry.link
            pubDate = getTime(entry)
            one = {"title": title, "link": link, "description": description, "guid": guid, "pubDate": pubDate}
            item_list += [one]
        feed = self.d.feed
        newfeed = {"title":self.tr(feed.title), "link":feed.link, "description":self.tr(getSubtitle(feed)), "lastBuildDate":getTime(feed), "items":item_list}
        return newfeed

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

    feed = BingTran(url, target=target, source=source).get_newcontent(max_item=max_item)

    rss_items = []
    for item in feed["items"]:
        title = item["title"]
        link = item["link"]
        description = item["description"]
        guid = item["guid"]
        pubDate = item["pubDate"]
        one = dict(title=title, link=link, description=description, guid=guid, pubDate=pubDate)
        rss_items += [one]

    rss_title = feed["title"]
    rss_link = feed["link"]
    rss_description = feed["description"]
    rss_last_build_date = feed["lastBuildDate"]
    rss = feedparser.FeedParserDict()
    rss.feed = feedparser.FeedParserDict({
        "title": rss_title,
        "link": rss_link,
        "description": rss_description,
        "lastBuildDate": rss_last_build_date,
        "items": rss_items
    })

    with open(out_dir, 'w', encoding='utf-8') as f:
        f.write(rss.to_string())

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

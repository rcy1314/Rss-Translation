import configparser
import os
import sys
from urllib.parse import unquote, quote
import hashlib
import datetime
import time
import feedparser
from mtranslate import translate
from bs4 import BeautifulSoup


def get_md5_value(src):
    """
    Calculate the MD5 hash value of the given string
    :param src: input string
    :return: MD5 hash value
    """
    _m = hashlib.md5()
    _m.update(src.encode('utf-8'))
    return _m.hexdigest()


def get_time(e):
    """
    Convert a time.struct_time object to a datetime.datetime object
    :param e: time.struct_time object
    :return: datetime.datetime object
    """
    try:
        struct_time = e.published_parsed
    except:
        struct_time = time.localtime()
    return datetime.datetime(*struct_time[:6])


class BingTran:
    def __init__(self, url, source='auto', target='zh-CN'):
        self.url = url
        self.source = source
        self.target = target
        self.d = feedparser.parse(url)

    def tr(self, content):
        """
        Translate a given content from source to target language
        :param content: input content
        :return: translated content
        """
        try:
            text = translate(content, to_language=self.target, from_language=self.source)
            return text
        except:
            return content

    def get_newcontent(self, max_item=2):
        """
        Get the translated content of the latest RSS feed
        :param max_item: the maximum number of items to be translated
        :return: dictionary containing the translated content of the latest RSS feed
        """
        item_list = []
        if len(self.d.entries) < max_item:
            max_item = len(self.d.entries)
        for entry in self.d.entries[:max_item]:
            try:
                title = self.tr(entry.title)
            except:
                title = ""
            link = entry.link
            description = ""
            try:
                description = self.tr(entry.summary)
            except:
                try:
                    description = self.tr(entry.content[0].value)
                except:
                    pass
            guid = entry.link
            pubDate = get_time(entry)
            one = {"title": title, "link": link, "description": description, "guid": guid, "pubDate": pubDate}
            item_list += [one]
        feed = self.d.feed
        try:
            rss_description = self.tr(feed.subtitle)
        except AttributeError:
            rss_description = ''
        newfeed = {"title": self.tr(feed.title), "link": feed.link, "description": rss_description,
                   "lastBuildDate": get_time(feed), "items": item_list}
        return newfeed


with open('test.ini', mode='r') as f:
    ini_data = unquote(f.read())
config = configparser.ConfigParser()
config.read_string(ini_data)
secs = config.sections()


def get_cfg(sec, name):
    """
    Get a value from the given section and name in the config file
    :param sec: section name
    :param name: name of value
    :return: value
    """
    return config.get(sec, name).strip('"')


def set_cfg(sec, name, value):
    """
    Set the value of the given name in the given section of the config file
    :param sec: section name
    :param name: name of value
    :param value: new value
    :return: None
    """
    config.set(sec, name, '"%s"' % value)


def get_cfg_tra(sec):
    """
    Get the source and target language of the given section in the config file
    :param sec: section name
    :return: source language, target language
    """
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
    """
    Translate and save the latest feed of the given section
    :param sec: section name
    :return: None
    """
    out_dir = BASE + get_cfg(sec, 'name')
    url = get_cfg(sec, 'url')
    max_item = int(get_cfg(sec, 'max'))
    old_md5 = get_cfg(sec, 'md5')
    source, target = get_cfg_tra(sec)
    global links

    links += [" - %s [%s](%s) -> [%s](%s)\n" % (sec, url, (url), get_cfg(sec, 'name'), quote(out_dir))]

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
    rss_description = ''
    rss_last_build_date = feed["lastBuildDate"]
    rss = """<rss version="2.0">
        <channel>
            <title>{}</title>
            <link>{}</link>
            <description>{}</description>
            <lastBuildDate>{}</lastBuildDate>
            {}
        </channel>
    </rss>""".format(rss_title, rss_link, rss_description, rss_last_build_date, "\n".join(
        ["<item>\n<title>{}</title>\n<link>{}</link>\n<description>{}</description>\n<guid>{}</guid>\n<pubDate>{}</pubDate>\n</item>".format(
            item["title"], item["link"], item["description"], item["guid"],
            item["pubDate"].strftime('%a, %d %b %Y %H:%M:%S GMT')) for item in rss_items]))

    with open(out_dir, 'w', encoding='utf-8') as f:
        f.write(rss)

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

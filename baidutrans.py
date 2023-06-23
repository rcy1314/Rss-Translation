# 请将"YOUR_BAIDU_API_KEY"和"YOUR_BAIDU_APP_ID"替换为您自己的百度翻译API密钥和应用ID再使用。
import configparser
import os
import sys
from urllib import parse
import hashlib
import datetime
import time
import feedparser
from bs4 import BeautifulSoup
from jinja2 import Template
import requests
import json

baidu_api_key = 'YOUR_BAIDU_API_KEY'
baidu_app_id = 'YOUR_BAIDU_APP_ID'

def get_md5_value(src):
    _m = hashlib.md5()
    _m.update(src.encode(encoding='utf-8'))
    return _m.hexdigest()

def getTime(e):
    try:
        struct_time = e.published_parsed
    except:
        struct_time = time.localtime()
    return datetime.datetime(*struct_time[:6])

class BaiduTran:
    def __init__(self, url, source='auto', target='zh'):
        self.url = url
        self.source = source
        self.target = target

        self.d = feedparser.parse(url)

    def tr(self, content):
        if not content:
            return ''

        # 使用百度翻译API进行翻译
        url = 'https://fanyi-api.baidu.com/api/trans/vip/translate'
        salt = str(int(time.time()))
        sign = hashlib.md5((baidu_app_id + content + salt + baidu_api_key).encode()).hexdigest()
        data = {
            'q': content,
            'from': self.source,
            'to': self.target,
            'appid': baidu_app_id,
            'salt': salt,
            'sign': sign
        }
        response = requests.get(url, params=data)
        result = json.loads(response.text)
        return result['trans_result'][0]['dst'] if 'trans_result' in result and len(result['trans_result']) > 0 else ''

    def get_newcontent(self, max_item=10):
        item_set = set()
        item_list = []
        for entry in self.d.entries:
            try:
                title = entry.title
                link = entry.link
                description = entry.summary
                guid = entry.link
                pubDate = getTime(entry)
                one = {"title": title, "link": link, "description": description, "guid": guid, "pubDate": pubDate}
                if guid not in item_set:
                    item_list.append(one)
                    item_set.add(guid)
            except:
                pass
        
        sorted_list = sorted(item_list, key=lambda x: x['pubDate'], reverse=True)
        
        if len(sorted_list) < max_item:
            max_item = len(sorted_list)
        item_list = sorted_list[:max_item]
        feed = self.d.feed
        try:
            rss_description = self.tr(feed.subtitle)
        except AttributeError:
            rss_description = ''
        newfeed = {"title": self.tr(feed.title), "link": feed.link, "description": rss_description, "lastBuildDate": getTime(feed), "items": item_list}
        return newfeed

with open('test.ini', mode='r') as f:
    ini_data = parse.unquote(f.read())
config = configparser.ConfigParser()
config.read_string(ini_data)
secs = config.sections()

def get_cfg(sec, name):
    return config.get(sec, name).strip('"')

def set_cfg(sec, name, value):
    config.set(sec, name, '"%s"' % value)

def get_cfg_tra(sec):
    cc = config.get(sec, "action").strip('"')
    target = ""
    source = ""
    if cc == "auto":
        source = 'auto'
        target = 'zh'
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

def update_readme():
    global links
    with open('README.md', "r+", encoding="UTF-8") as f:
        list1 = f.readlines()
    list1 = list1[:13] + links
    with open('README.md', "w+", encoding="UTF-8") as f:
        f.writelines(list1)

def tran(sec):
    out_dir = os.path.join(BASE, get_cfg(sec, 'name'))
    xml_file = os.path.join(BASE, f'{get_cfg(sec, "name")}.xml')
    url = get_cfg(sec, 'url')
    max_item = int(get_cfg(sec, 'max'))
    old_md5 = get_cfg(sec, 'md5')
    source, target = get_cfg_tra(sec)
    global links
    links += [" - %s [%s](%s) -> [%s](%s)\n" % (sec, url, (url), get_cfg(sec, 'name'), parse.quote(xml_file))]

    # 读取url链接对应的rss内容
    try:
        feed = BaiduTran(url, target=target, source=source).get_newcontent(max_item=max_item)
    except Exception as e:
        print("Error occurred when fetching RSS content for %s: %s" % (sec, str(e)))
        return

    # 判断rss内容是否有更新
    new_md5 = get_md5_value(url + str(feed))
    if old_md5 == new_md5:
        print("No update needed for %s" % sec)
        return
    else:
        print("Updating %s..." % sec)
        set_cfg(sec, 'md5', new_md5)

     # 处理 RSS 内容，生成新的 RSS 文件
    rss_items = []
    for item in feed["items"]:
        title = item["title"]
        link = item["link"]
        description = item["description"]
        guid = item["guid"]
        pubDate = item["pubDate"]
        # 处理翻译结果中的不正确的 XML 标记
        soup = BeautifulSoup(description, 'html.parser')
        description = soup.get_text()
        one = dict(title=title, link=link, description=description, guid=guid, pubDate=pubDate)
        rss_items.append(one)
        # 转义特殊字符
        description = description.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')
        one = dict(title=title, link=link, description=description, guid=guid, pubDate=pubDate)
        rss_items.append(one)


    rss_title = feed["title"]
    rss_link = feed["link"]
    rss_description = feed["description"]
    rss_last_build_date = feed["lastBuildDate"].strftime('%a, %d %b %Y %H:%M:%S GMT')

    template = Template("""<?xml version="1.0" encoding="UTF-8"?>
 <rss version="2.0">
 <channel>
    <title>{{ rss_title }}</title>
    <link>{{ rss_link }}</link>
    <description>{{ rss_description }}</description>
    <lastBuildDate>{{ rss_last_build_date }}</lastBuildDate>
    {% for item in rss_items -%}
    <item>
        <title>{{ item.title }}</title>
        <link>{{ item.link }}</link>
        <description>{{ item.description }}</description>
        <guid isPermaLink="false">{{ item.guid }}</guid>
        <pubDate>{{ item.pubDate.strftime('%a, %d %b %Y %H:%M:%S GMT') }}</pubDate>
    </item>
    {% endfor -%}
 </channel>
 </rss>""")

    rss = template.render(rss_title=rss_title, rss_link=rss_link, rss_description=rss_description, rss_last_build_date=rss_last_build_date, rss_items=rss_items)

    try:
        os.makedirs(BASE, exist_ok=True)
    except Exception as e:
        print("Error occurred when creating directory %s: %s" % (BASE, str(e)))
        return

    if os.path.isfile(xml_file):
        try:
            with open(xml_file, 'r', encoding='utf-8') as f:
                old_rss = f.read()
        except Exception as e:
            print("Error occurred when reading RSS file %s for %s: %s" % (xml_file, sec, str(e)))
            return
        rss = old_rss + rss

    try:
        with open(xml_file, 'w', encoding='utf-8') as f:
            f.write(rss)
    except Exception as e:
        print("Error occurred when writing RSS file %s for %s: %s" % (xml_file, sec, str(e)))
        return

    set_cfg(sec, 'md5', new_md5)
    with open('test.ini', "w") as configfile:
        config.write(configfile)

config = configparser.ConfigParser()
config.read('test.ini')
secs = config.sections()

for x in secs[1:]:
    tran(x)
update_readme()

with open('test.ini', "w") as configfile:
    config.write(configfile)

YML = "README.md"
f = open(YML, "r+", encoding="UTF-8")
list1 = f.readlines()
list1 = list1[:13] + links
f = open(YML, "w+", encoding="UTF-8")
f.writelines(list1)
f.close()

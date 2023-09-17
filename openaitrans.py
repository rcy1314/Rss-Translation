import configparser
import os
import sys
import hashlib
import datetime
import time
import feedparser
from urllib import parse
from bs4 import BeautifulSoup
from jinja2 import Template
import requests
import openai

# 设置OpenAI API密钥
openai.api_key = "YOUR_API_KEY"

def get_md5_value(src):
    m = hashlib.md5()
    m.update(src.encode(encoding='utf-8'))
    return m.hexdigest()

def get_time(e):
    try:
        struct_time = e.published_parsed
    except:
        struct_time = time.localtime()
    return datetime.datetime(*struct_time[:6])

class OpenAITran:
    def __init__(self, url, source='auto', target='zh-CN'):
        self.url = url
        self.source = source
        self.target = target
        self.d = feedparser.parse(url)
        self.translation_cache = {}

    def tr(self, content):
        if content in self.translation_cache:
            return self.translation_cache[content]

        response = openai.Completion.create(
            model="gpt-3.5-turbo",
            prompt=content,
            max_tokens=2000,
            temperature=0.7,
            n=1,
            stop=None
        )

        translation = response.choices[0].text.strip()
        self.translation_cache[content] = translation
        return translation

    def get_new_content(self, max_item=10):
        item_set = set()  # 使用集合来存储项目，用于过滤重复项
        item_list = []
        for entry in self.d.entries:
            try:
                title = self.tr(entry.title)
            except:
                title = ""
            parsed_link = urlparse(entry.link)
            if not all([parsed_link.scheme, parsed_link.netloc]):
                continue
            link = entry.link
            description = ""
            try:
                description = self.tr(entry.summary)
            except:
                try:
                    description = self.tr(entry.content[0].value)
                except:
                    pass
            guid = link
            pub_date = get_time(entry)
            one = {"title": title, "link": link, "description": description, "guid": guid, "pubDate": pub_date}
            if guid not in item_set:  # 判断是否重复
                item_set.add(guid)
                item_list.append(one)
            if len(item_list) >= max_item:  # 判断是否达到最大项目数
                break
        sorted_list = sorted(item_list, key=lambda x: x['pubDate'], reverse=True)
        feed = self.d.feed
        try:
            rss_description = self.tr(feed.subtitle)
        except AttributeError:
            rss_description = ''
        new_feed = {"title": self.tr(feed.title), "link": feed.link, "description": rss_description,
                    "lastBuildDate": get_time(feed), "items": sorted_list}
        return new_feed

def update_readme(links):
    with open('README.md', "r+", encoding="UTF-8") as f:
        list1 = f.readlines()
        list1 = list1[:13] + links
    with open('README.md', "w+", encoding="UTF-8") as f:
        f.writelines(list1)

def tran(sec, max_item):
    # 获取各种配置信息
    out_dir = os.path.join(BASE, get_cfg(sec, 'name'))
    xml_file = os.path.join(BASE, f'{get_cfg(sec, "name")}.xml')
    url = get_cfg(sec, 'url')
    old_md5 = get_cfg(sec, 'md5')
    # 读取旧的 MD5 散列值
    source, target = get_cfg_tra(sec, config)
    global links
    links += [" - %s %s -> %s\n" % (sec, url, get_cfg(sec, 'name'))]
    # 判断 RSS 内容是否有更新
    try:
        r = requests.get(url)
        new_md5 = get_md5_value(r.text)
    except Exception as e:
        print("Error occurred when fetching RSS content for %s: %s" % (sec, str(e)))
        return
    if old_md5 == new_md5:
        print("No update needed for %s" % sec)
        return
    else:
        print("Updating %s..." % sec)
        set_cfg(sec, 'md5', new_md5)

    # 调用 OpenAITran 类获取新的 RSS 内容
    try:
        feed = OpenAITran(url, target=target, source=source).get_new_content(max_item=max_item)
    except Exception as e:
        print("Error occurred when fetching RSS content for %s: %s" % (sec, str(e)))
        return

    # 处理 RSS 内容，生成新的 RSS 文件
    rss_items = []
    for item in feed["items"]:
        title = item["title"]
        link = item["link"]
        description = item["description"]
        guid = item["guid"]
        pub_date = item["pubDate"]
        # 处理翻译结果中的不正确的 XML 标记
        soup = BeautifulSoup(description, 'html.parser')
        description = soup.get_text()
        # 转义特殊字符
        description = description.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')
        one = dict(title=title, link=link, description=description, guid=guid, pubDate=pub_date)
        rss_items.append(one)

    rss_title = feed["title"]
    rss_link = feed["link"]
    rss_description = feed["description"]
    rss_last_build_date = feed["lastBuildDate"].strftime('%a, %d %b %Y %H:%M:%S GMT')

    template = Template("""<?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0"> <channel> <title>{{ rss_title }}</title> <link>{{ rss_link }}</link> <description>{{ rss_description }}</description> <lastBuildDate>{{ rss_last_build_date }}</lastBuildDate> {% for item in rss_items -%} <item> <title>{{ item.title }}</title> <link>{{ item.link }}</link> <description><![CDATA[{{ item.description }}]]></description> <guid>{{ item.guid }}</guid> <pubDate>{{ item.pubDate.strftime('%a, %d %b %Y %H:%M:%S GMT') }}</pubDate> </item> {% endfor -%} </channel> </rss>""")
    rss = template.render(rss_title=rss_title, rss_link=rss_link, rss_description=rss_description,
                          rss_last_build_date=rss_last_build_date, rss_items=rss_items)

    try:
        os.makedirs(BASE, exist_ok=True)
    except Exception as e:
        print("Error occurred when creating directory %s: %s" % (BASE, str(e)))
        return

    # 如果 RSS 文件存在，则删除原有内容
    if os.path.isfile(xml_file):
        try:
            with open(xml_file, 'r', encoding='utf-8') as f:
                old_rss = f.read()
            if rss == old_rss:
                print("No change in RSS content for %s" % sec)
                return
            else:
                os.remove(xml_file)
        except Exception as e:
            print("Error occurred when deleting RSS file %s for %s: %s" % (xml_file, sec, str(e)))
            return

    try:
        with open(xml_file, 'w', encoding='utf-8') as f:
            f.write(rss)
    except Exception as e:
        print("Error occurred when writing RSS file %s for %s: %s" % (xml_file, sec, str(e)))
        return

    # 更新配置信息并写入文件中
    set_cfg(sec, 'md5', new_md5)
    with open('test.ini', "w") as configfile:
        config.write(configfile)

def get_cfg(sec, name):
    return config.get(sec, name).strip('"')

def set_cfg(sec, name, value):
    config.set(sec, name, '"%s"' % value)

def get_cfg_tra(sec, config):
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

# 读取配置文件
config = configparser.ConfigParser()
config.read('test.ini')

# 获取基础路径
BASE = get_cfg("cfg", 'base')
try:
    os.makedirs(BASE)
except:
    pass
links = []

# 遍历所有的 RSS 配置，依次更新 RSS 文件
secs = config.sections()

links = []
for x in secs[1:]:
    max_item = int(get_cfg(x, 'max'))
    tran(x, max_item)
    time.sleep(3)  # 添加延迟，每次调用API之间间隔3秒

update_readme(links)

with open('test.ini', "w") as configfile:
    config.write(configfile)

YML = "README.md"
f = open(YML, "r+", encoding="UTF-8")
list1 = f.readlines()
list1 = list1[:13] + links
f = open(YML, "w+", encoding="UTF-8")
f.writelines(list1)
f.close()

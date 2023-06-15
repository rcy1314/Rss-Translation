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
from jinja2 import Template

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

class BingTran:
    def __init__(self, url, source='auto', target='zh-CN'):
        self.url = url
        self.source = source
        self.target = target

        self.d = feedparser.parse(url)

    def tr(self, content):
        return translate(content, to_language=self.target, from_language=self.source)

    def get_newcontent(self, max_item=50):
        item_list = []
        # 获取所有项目以过滤重复项
        for entry in self.d.entries:
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
            pubDate = getTime(entry)
            one = {"title": title, "link": link, "description": description, "guid": guid, "pubDate": pubDate}
            item_list += [one]
        # 按发布日期降序排序
        sorted_list = sorted(item_list, key=lambda x: x['pubDate'], reverse=True)
        # 过滤重复项目
        unique_list = []
        for item in sorted_list:
            if item not in unique_list:
                unique_list.append(item)
        # 截取前 max_item 个项目
        if len(unique_list) < max_item:
            max_item = len(unique_list)
        item_list = unique_list[:max_item]
        feed = self.d.feed
        try:
            rss_description = self.tr(feed.subtitle)
        except AttributeError:
            rss_description = ''
        newfeed = {"title":self.tr(feed.title), "link":feed.link, "description":rss_description, "lastBuildDate":getTime(feed), "items":item_list}
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

def update_readme():
    global links
    with open('README.md', "r+", encoding="UTF-8") as f:
        list1 = f.readlines()
    list1 = list1[:13] + links
    with open('README.md', "w+", encoding="UTF-8") as f:
        f.writelines(list1)

def tran(sec):
    # 获取各种配置信息
    out_dir = os.path.join(BASE, 'rss', get_cfg(sec, 'name'))
    xml_file = os.path.join(out_dir, f'{get_cfg(sec, "name")}.xml')
    url = get_cfg(sec, 'url')
    max_item = int(get_cfg(sec, 'max'))
    old_md5 = get_cfg(sec, 'md5') 
    # 读取旧的 MD5 散列值
    source, target = get_cfg_tra(sec)
    global links
    links += [" - %s [%s](%s) -> [%s](%s)\n" % (sec, url, (url), get_cfg(sec, 'name'), parse.quote(out_dir))]

    # 获取新的 RSS 内容，并计算新的 MD5 散列值
    new_content = BingTran(url, target=target, source=source).get_newcontent(max_item=max_item)
    new_md5 = get_md5_value(url + str(new_content))

    # 检查是否需要更新 RSS 内容
    if old_md5 == new_md5:
        print("No update needed for %s" % sec)
        return
    else:
        print("Updating %s..." % sec)
        set_cfg(sec, 'md5', new_md5) # 更新配置文件中的 MD5 散列值

    # 调用 BingTran 类获取新的 RSS 内容
    try:
        feed = BingTran(url, target=target, source=source).get_newcontent(max_item=max_item)
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
        pubDate = item["pubDate"]
        one = dict(title=title, link=link, description=description, guid=guid, pubDate=pubDate)
        rss_items += [one]

    rss_title = feed["title"]
    rss_link = feed["link"]
    rss_description = feed["description"]
    rss_last_build_date = feed["lastBuildDate"].strftime('%a, %d %b %Y %H:%M:%S GMT')

    template = Template("""<rss version="2.0">
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
        os.makedirs(out_dir, exist_ok=True)
    except Exception as e:
        print("Error occurred when creating directory %s: %s" % (out_dir, str(e)))
        return

    rss_file = os.path.join(out_dir, f'{get_cfg(sec, "name")}.xml')
    # 如果 RSS 文件存在，则将新内容追加到原有内容后面
    if os.path.isfile(rss_file):
        try:
            with open(rss_file, 'r', encoding='utf-8') as f:
                old_rss = f.read()
        except Exception as e:
            print("Error occurred when reading RSS file %s for %s: %s" % (rss_file, sec, str(e)))
            return
        rss = old_rss + rss

    try:
        with open(rss_file, 'w', encoding='utf-8') as f:
            f.write(rss)
    except Exception as e:
        print("Error occurred when writing RSS file %s for %s: %s" % (rss_file, sec, str(e)))
        return

    # 更新配置信息并写入文件中
    set_cfg(sec, 'md5', new_md5)
    with open('test.ini', "w") as configfile:
        config.write(configfile)

# 遍历所有的 RSS 配置，依次更新 RSS 文件
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

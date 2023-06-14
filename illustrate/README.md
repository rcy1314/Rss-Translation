# ⭐说明及添加⭐

已在原项目基础上更新Action环境依赖，默认翻译为main.py文件，已改为Bing翻译接口，可随时切换翻译接口

注意：免费的翻译API会有请求次数限制！如果定时运行时间过于频繁，可能会导致action更新抓取一些站点时被限制及封禁！

已改为定时每6小时运行一次（建议每12小时运行），增加[谷歌翻译接口](https://github.com/rcy1314/Rss-Translation/blob/main/mygoogletrans.py)、[Bing翻译接口](https://github.com/rcy1314/Rss-Translation/blob/main/Bingtrans.py)及[百度翻译接口](https://github.com/rcy1314/Rss-Translation/blob/main/baidutrans.py)

## Bing翻译接口文件调整：

• 修复了使用set_cfg()方法修改配置文件数据时的bug

• 使用了 jinja2 模板引擎来生成 RSS 格式的输出，并对 XML 数据进行了安全处理，添加了运行命令pip install lxml外一个解析库 html5lib：pip install html5lib

• 对Feed的生成做了一些修改，扩展RSS的一些属性，如通过strftime格式化时间输出。并且将Feed的构成改成了字符串拼接的方式，更加简洁易懂。

• 代码使用了try-except语句进行容错处理，确保代码不会因为单个翻译出错而出现错误。

## google翻译接口文件调整：

• 更换了翻译接口，使用googletrans模块代替pygtrans模块。

• 安全地将字符串输入到md5()函数中，使用encode()函数将字符串转换为UTF-8编码。

• 使用os.path.join()方法代替基本字符串拼接的方式来构建输出目录。

• 在处理HTML数据时，使用了更准确的BeautifulSoup的解析模式。

## 使用说明

1. 在运行代码前，确认已安装库文件，对应翻译接口文件中的模块，如pip install mtranslate

2. 在test.ini 文件中添加需要翻译的 RSS 订阅信息。例如：

```
[cfg]
base=./rss/

[BBC]
url=https://feeds.bbci.co.uk/news/rss.xml
name=BBC_zh.xml
max=5
action=en->zh-CN
md5=""
```
3.打开 GitHub 仓库的界面，进入“Settings” > “Secrets”，点击“New repository secret”按钮，创建名为 WORK_TOKEN 的 secret。

4.将生成的Personal Access Token及U_EMAIL、U_NAME复制黏贴到Action-操作机密和变量中，然后运行action即可

## 目前仍存在的Bug

由于国外一些站点时常封禁api及禁止RSS，如果使用类似的RSS源会导致覆写文件时某些元素错误，建议先查看已转换xml文件下raw格式链接

## 关于bug报错及修复：

• 用于解析RSS的库和在使用的python版本不兼容

• 添加的rss源字符串过多（如全文输出的rss源），api无法翻译，如果缺少subtitle属性，可以将rss_description设置为空字符串，如rss_description = ''

• 环境依赖无或版本过旧，可更新后替换

• Python翻译库不兼容，可以更换为其它（TextBlob、IBM Watson、Bing Translator、andex Translate API等）

## 本地

如要本地使用（请确保你有python环境及SSL证书）
并确保你有安装以下模块（检查文件确保包含文件内的导入模块）：
如：

- configparser
- pygtrans
- beautifulsoup4
- urllib

如果提示没有安装模块，你可以通过以下方式来安装：

```
pip install configparser
pip install pygtrans
pip install beautifulsoup4
pip install urllib
```

最后运行python文件即可。

[个人喜好RSS阅读页](https://rcy1314.github.io/news/)：无历史数据，可点击 [rss feed for you](https://morss.it/:proxy:items=%7C%7C*[class=card]%7C%7Col%7Cli/https://rcy1314.github.io/news/) 来订阅页面

<img src="https://camo.githubusercontent.com/82291b0fe831bfc6781e07fc5090cbd0a8b912bb8b8d4fec0696c881834f81ac/68747470733a2f2f70726f626f742e6d656469612f394575424971676170492e676966" width="800"  height="3">

## 已添加订阅源
•  [TG频道Artificial Intelligence](https://raw.githubusercontent.com/rcy1314/Rss-Translation/main/rss/Artificial_intelligence_in.xml)

•  [reddit-自动化](https://rcy1314.github.io/Rss-Translation/rss/reddit_automation.xml)

•  [huggingface博客页](https://rcy1314.github.io/Rss-Translation/rss/huggingface_blog.xml)

•  [reddit-人工智能](https://rcy1314.github.io/Rss-Translation/rss/reddit_ArtificialInteligence.xml)

•  [reddit_OpenAI](https://rcy1314.github.io/Rss-Translation/rss/reddit_OpenAI.xml)

•  [reddit_ChatGPT](https://rcy1314.github.io/Rss-Translation/rss/reddit_ChatGPT.xml)

•  [reddit_GPT3](https://rcy1314.github.io/Rss-Translation/rss/reddit_GPT3.xml)

•  [reddit_风光摄影](https://rcy1314.github.io/Rss-Translation/rss/reddit_LandscapePhotography.xml)

•  [reddit_街头摄影](https://rcy1314.github.io/Rss-Translation/rss/reddit_streetphotography.xml)

•  [reddit_免费频道](https://rcy1314.github.io/Rss-Translation/rss/reddit_FREE.xml)

•  [reddit_免费课程](https://rcy1314.github.io/Rss-Translation/rss/reddit_FREECoursesEveryday.xml)

•  [reddit_后期制作](https://rcy1314.github.io/Rss-Translation/rss/reddit_editors.xml)

•  [reddit_软件相关](https://rcy1314.github.io/Rss-Translation/rss/reddit_software.xml)

•  [reddit_电脑编程](https://rcy1314.github.io/Rss-Translation/rss/reddit_programming.xml)

•  [reddit_ 艺术自由区](https://rcy1314.github.io/Rss-Translation/rss/reddit_PixelArt.xml)

•  [reddit_复古游戏音乐](https://rcy1314.github.io/Rss-Translation/rss/reddit_chiptunes.xml)

•  [reddit_无版权音乐](https://rcy1314.github.io/Rss-Translation/rss/reddit_youtubeaudiolibrary.xml)

•  [reddit_web开发](https://rcy1314.github.io/Rss-Translation/rss/reddit_webdev.xml)

•  [reddit_开源社区](https://rcy1314.github.io/Rss-Translation/rss/reddit_opensource.xml)

•  [producthunt_每日产品](https://rcy1314.github.io/Rss-Translation/rss/producthunt_today.xml)

•  [Hacker News自动摘要TG频道](https://rcy1314.github.io/Rss-Translation/rss/hn_summary.xml)

•  [顶级开源项目网站更新](https://rcy1314.github.io/Rss-Translation/rss/opensourceagenda.xml)

•  [独立黑客社区更新](https://rcy1314.github.io/Rss-Translation/rss/indiehackers-world.xml)

•  [独立黑客_生产力频道](https://rcy1314.github.io/Rss-Translation/rss/indiehackers-productivity.xml)

•  [独立黑客_自动化频道](https://rcy1314.github.io/Rss-Translation/rss/indiehackers-Automation.xml)

•  [独立黑客_ChatGpt频道](https://rcy1314.github.io/Rss-Translation/rss/indiehackers-ChatGPT.xml)

•  [独立黑客_无代码频道](https://rcy1314.github.io/Rss-Translation/rss/indiehackers-No-Code.xml)

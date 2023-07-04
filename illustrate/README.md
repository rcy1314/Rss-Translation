# ⭐说明及添加⭐

已重构翻译文件配置、更新Action环境依赖，已测试运行翻译文件，可随时切换翻译接口【切换翻译需在工作流yml文件中更改ls_show步骤下运行的python文件】

为防止运行加载过慢出现错误，代码中添加了避免重复翻译及使用集合来去除重复项

**默认规则：如果 RSS 文件已存在，将去除原有xml重复内容更新最新内容**

注意：免费的翻译API会有请求次数限制！如果定时运行时间过于频繁，可能会导致action更新抓取一些站点时被限制及封禁！免费的翻译包括bing翻译和谷歌翻译

已改为定时每3小时运行一次（建议每6-12小时运行），增加[谷歌翻译接口](https://github.com/rcy1314/Rss-Translation/blob/main/mygoogletrans.py)、[Bing翻译接口](https://github.com/rcy1314/Rss-Translation/blob/main/Bingtrans.py)及[百度翻译接口](https://github.com/rcy1314/Rss-Translation/blob/main/baidutrans.py)、[Open ai翻译接口](https://github.com/rcy1314/Rss-Translation/blob/main/openaitrans.py)

## Bing翻译接口文件调整：

- 修复了使用set_cfg()方法修改配置文件数据时的bug

- 使用了 jinja2 模板引擎来生成 RSS 格式的输出，并对 XML 数据进行了安全处理，添加了运行命令pip install lxml外一个解析库 html5lib：pip install html5lib

- 对Feed的生成做了一些修改，扩展RSS的一些属性，如通过strftime格式化时间输出。并且将Feed的构成改成了字符串拼接的方式，更加简洁易懂。

- 代码使用了try-except语句进行容错处理，确保代码不会因为单个翻译出错而出现错误。

## google翻译接口文件调整：

- 更换了翻译接口，使用pygtrans模块代替googletrans模块

- 将字符串输入到md5()函数中，使用encode()函数将字符串转换为UTF-8编码。

- 使用os.path.join()方法代替基本字符串拼接的方式来构建输出目录。

-  在处理HTML数据时，使用了更准确的BeautifulSoup的解析模式。

## 百度翻译接口文件调整：

- 集成了百度翻译API密钥和应用ID，修改为自己的即可使用
- 优势：收费的api翻译更多更准确和不限制api次数
- 设置源语言和目标语言为百度翻译API支持的语言代码
- 修改tran方法中的BaiduTran实例化部分，传入源语言和目标语言参数

## OPEN AI翻译接口文件调整：

- 集成了open ai翻译API密钥修改为自己的即可使用
- 修改调用模型为gpt-3.5-turbo
- 优化传入源语言和目标语言参数


## 工作流文件调整：

**添加翻译文件依赖库**

```
          pip install mtranslate

​          pip install lxml

​          pip install html5lib

​          pip install jinja2

​          pip install googletrans

​          pip install googletrans==4.0.0-rc1

​          pip install beautifulsoup4 pygtrans feedparser rfeed

​          pip install --upgrade feedparser

​          pip install requests
```

- 其中googletrans为谷歌翻译库，requests为百度翻译库，mtranslate`和`jinja2为bing翻译必须库

- 使用 git status --porcelain 指令来检查代码库中是否存在新的更改需要提交，如果有，则执行 git add，git commit 和 git push 命令。否则，输出 “No changes, skip push.” 的消息。

- 为可随时切换不同翻译api，添加多个翻译文件所需模块


# 【使用说明】

1. 在运行代码前，先删除本项目原有的rss文件目录下的xml文件（并确认已安装库文件）可查看工作流文件中Install dependencies步骤下配置【一般不需要改动】

2. 在test.ini 文件中添加需要翻译的 RSS 订阅信息。例如：

```
[cfg]
base = "rss/"

[BBC]
url= "https://feeds.bbci.co.uk/news/rss.xml"
name= "BBC_zh"
max= "5"
action = "auto"
md5= ""
```
**其中name为英文名不要添加后缀！！！！，本项目生成的文件为固定的.xml格式文件**，不需要name有后缀，此外name也不要字符过长避免识别有误

<img src="https://cdn.staticaly.com/gh/rcy1314/tuchuang@main/20230704/wrer.47jpkdp3pfu0.jpg" style="zoom:40%;" />

base参数为生成的文件存放目录，max参数为rss最大条目数（请不要设置超过20，使用免费翻译的api时RSS条目超过一定数量会出现不完整翻译），md5请设置为空！

3.打开 GitHub 仓库的界面，进入“Settings” > “Secrets”，点击“New repository secret”按钮，创建名为 WORK_TOKEN 的 secret。【设置-开发者设置-生成个人经典令牌】

![](https://cdn.staticaly.com/gh/rcy1314/tuchuang@main/20230704/wauh.13r6vfv3ipz4.jpg)

4.将生成的 Token及U_EMAIL（你的github邮箱）、U_NAME（你的github用户名）复制黏贴到Action-操作机密和变量中，然后运行action即可

<img src="https://cdn.staticaly.com/gh/rcy1314/tuchuang@main/20230704/wqw.50kt20k20lk0.jpg" style="zoom:25%;" />

注：我把jekyll-gh-pages.yml生成页面工作流关闭了自动运行，如果你是直接fork的，如果更新[页面](https://rcy1314.github.io/Rss-Translation/)需要手动运行Deploy

另外这个项目是支持全文翻译的！但就像上面提到的全文过多字符的源用免费的翻译api（谷歌或必应）是无法全部翻译！![](https://cdn.staticaly.com/gh/rcy1314/tuchuang@main/20230704/ererere.2rl39yjugcq0.jpg)

全文翻译查看示例：

<img src="https://cdn.staticaly.com/gh/rcy1314/tuchuang@main/20230704/quanwen.3vboa74fem40.jpg" style="zoom:50%;" />

## *关于max_item数值的说明*

`max_item`是用来控制获取的RSS项的数量的参数。它决定了从RSS源中获取的最大项目数目。默认值是10，但你可以根据你的需求进行调整。

在`get_newcontent`函数中，使用`max_item`来限制循环获取的项数。当获取的项目数达到`max_item`时，循环就会终止，不再获取更多的项目。

因此，根据你的需求，你可以将`max_item`设置为任何你想要的整数值。如果你想要获取所有的项目，你可以将`max_item`设置为一个很大的数，比如100，那么每次更新将返回最多100个rss条目，但过大的数值会让免费翻译的api无法完整翻译为中文，如果你只想获取最新的几个项目，你可以将`max_item`设置为一个较小的数，比如5。

需要注意的是，如果RSS源中的项目数少于`max_item`，那么将获取所有的项目，不会进行截断

## 关于如果出现bug报错原因及修复：

- 用于解析RSS的库和在使用的python版本不兼容

- 添加的rss源字符串过多（如全文输出的rss源），api无法翻译，如果缺少subtitle属性，可以将rss_description设置为空字符串，如rss_description = ''

- 环境依赖无或版本过旧，可更新后替换

- Python翻译库不兼容，可以更换为其它（TextBlob、IBM Watson、Bing Translator、andex Translate API等）

- 如果直接出现http服务器链接失败大概率是因为github本身问题或action运行被限制，等待一段时间后再运行。


## 本地使用

如要本地使用（请确保你有python环境及网络SSL证书）
并确保你有安装翻译接口所需的模块，例如以下模块（检查文件确保包含文件内的导入模块）：
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
•  [TG频道Artificial Intelligence](https://rcy1314.github.io/Rss-Translation/rss/Artificial_intelligence_in.xml)

•  [reddit-自动化](https://rcy1314.github.io/Rss-Translation/rss/reddit_automation.xml)

•  [huggingface博客页](https://rcy1314.github.io/Rss-Translation/rss/huggingface_blog.xml)

•  [reddit-人工智能](https://rcy1314.github.io/Rss-Translation/rss/reddit_ArtificialInteligence.xml)

•  [TG频道AI工作](https://rcy1314.github.io/Rss-Translation/rss/AiIndiaJobs.xml)

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

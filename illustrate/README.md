# ⭐说明及添加⭐

已在原项目基础上更新Action环境依赖，由于此前每3小时运行过于频繁，目前已导致action更新抓取一些站点时被限制及封禁！！！

改为定时每6小时运行一次（建议每12小时运行）或更久时间，增加及完善[谷歌翻译接口](https://github.com/rcy1314/Rss-Translation/blob/main/googletrans.py)及[百度翻译接口](https://github.com/rcy1314/Rss-Translation/blob/main/baidutrans.py)

一些调整：

• 更换了翻译接口，使用googletrans模块代替pygtrans模块。

• 修改了导入的模块

• 安全地将字符串输入到md5()函数中，使用encode()函数将字符串转换为UTF-8编码。

• 使用os.path.join()方法代替基本字符串拼接的方式来构建输出目录。

• 在处理HTML数据时，使用了更准确的BeautifulSoup的解析模式。

rss注意：有的RSS源过多字符会造成不完整翻译及报错，不要添加过多字符的源如全文输出的rss源

本地使用（请确保你有python环境及SSL证书）
并确保你有安装以下模块：

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

[个人喜好RSS阅读页](https://rcy1314.github.io/news/)：无历史数据，可点击 rss for you 来订阅页面

<img src="https://camo.githubusercontent.com/82291b0fe831bfc6781e07fc5090cbd0a8b912bb8b8d4fec0696c881834f81ac/68747470733a2f2f70726f626f742e6d656469612f394575424971676170492e676966" width="800"  height="3">

## 已添加订阅源
 1. [TG频道Artificial Intelligence](https://rcy1314.github.io/Rss-Translation/rss/Artificial_intelligence_in.xml)
 2. [reddit-自动化](https://rcy1314.github.io/Rss-Translation/rss/reddit_automation.xml)
 3. [reddit-生产力](https://rcy1314.github.io/Rss-Translation/rss/reddit_productivity.xml)
 4. [huggingface博客页](https://rcy1314.github.io/Rss-Translation/rss/huggingface_blog.xml)
 5. [reddit-人工智能](https://rcy1314.github.io/Rss-Translation/rss/reddit_ArtificialInteligence.xml)
 6. [reddit_OpenAI](https://rcy1314.github.io/Rss-Translation/rss/reddit_OpenAI.xml)
 7. [reddit_ChatGPT](https://rcy1314.github.io/Rss-Translation/rss/reddit_ChatGPT.xml)
 8. [reddit_GPT3](https://rcy1314.github.io/Rss-Translation/rss/reddit_GPT3.xml)
 9. [reddit_风光摄影](https://rcy1314.github.io/Rss-Translation/rss/reddit_LandscapePhotography.xml)
 10. [reddit_街头摄影](https://rcy1314.github.io/Rss-Translation/rss/reddit_streetphotography.xml)
 11. [reddit_免费频道](https://rcy1314.github.io/Rss-Translation/rss/reddit_FREE.xml)
 12. [reddit_免费课程](https://rcy1314.github.io/Rss-Translation/rss/reddit_FREECoursesEveryday.xml)
 13. [reddit_后期制作](https://rcy1314.github.io/Rss-Translation/rss/reddit_editors.xml)
 14. [reddit_软件相关](https://rcy1314.github.io/Rss-Translation/rss/reddit_software.xml)
 15. [reddit_电脑编程](https://rcy1314.github.io/Rss-Translation/rss/reddit_programming.xml)
 16. [reddit_ 艺术自由区](https://rcy1314.github.io/Rss-Translation/rss/reddit_PixelArt.xml)
 17. [reddit_复古游戏音乐](https://rcy1314.github.io/Rss-Translation/rss/reddit_chiptunes.xml)
 18. [reddit_无版权音乐](https://rcy1314.github.io/Rss-Translation/rss/reddit_youtubeaudiolibrary.xml)
 19. [reddit_web开发](https://rcy1314.github.io/Rss-Translation/rss/reddit_webdev.xml)
 20. [reddit_开源社区](https://rcy1314.github.io/Rss-Translation/rss/reddit_opensource.xml)
 21. [producthunt_每日产品](https://rcy1314.github.io/Rss-Translation/rss/producthunt_today.xml)
 22. [Hacker News自动摘要TG频道](https://rcy1314.github.io/Rss-Translation/rss/hn_summary.xml)
 23. [顶级开源项目网站更新](https://rcy1314.github.io/Rss-Translation/rss/opensourceagenda.xml)
 24. [独立黑客社区更新](https://rcy1314.github.io/Rss-Translation/rss/indiehackers-world.xml)
 25. [独立黑客_生产力频道](https://rcy1314.github.io/Rss-Translation/rss/indiehackers-productivity.xml)
 26. [独立黑客_自动化频道](https://rcy1314.github.io/Rss-Translation/rss/indiehackers-Automation.xml)
 27. [独立黑客_ChatGpt频道](https://rcy1314.github.io/Rss-Translation/rss/indiehackers-ChatGPT.xml)
 28. [独立黑客_无代码频道](https://rcy1314.github.io/Rss-Translation/rss/indiehackers-No-Code.xml)

#  Rss-Translation

## 这是一个外文RSS翻译转换订阅页面 

[![circle_translate](https://github.com/rcy1314/Rss-Translation/actions/workflows/circle_translate.yml/badge.svg)](https://github.com/rcy1314/Rss-Translation/actions/workflows/circle_translate.yml) [![Deploy](https://github.com/rcy1314/Rss-Translation/actions/workflows/jekyll-gh-pages.yml/badge.svg)](https://github.com/rcy1314/Rss-Translation/actions/workflows/jekyll-gh-pages.yml)

 💡重构翻译文件配置、更新Action环境依赖，添加不同翻译机制,已修复特殊字符转译

 📢查看 [项目修改完善、已添加源及使用说明](https://github.com/rcy1314/Rss-Translation/tree/main/illustrate)

 📢查看[ 本页 ](https://rcy1314.github.io/Rss-Translation) 参考自[ rss-translate ](https://github.com/talengu/rss-translate)

## 已转换翻译源
 - source001 [https://rsshub.app/telegram/channel/Artificial_intelligence_in](https://rsshub.app/telegram/channel/Artificial_intelligence_in) -> [Artificial_intelligence_in](rss/Artificial_intelligence_in.xml)
 - source002 [https://www.reddit.com/r/automation.rss](https://www.reddit.com/r/automation.rss) -> [reddit_automation](rss/reddit_automation.xml)
 - source003 [https://huggingface.co/blog/feed.xml](https://huggingface.co/blog/feed.xml) -> [huggingface_blog](rss/huggingface_blog.xml)
 - source004 [https://www.reddit.com/r/ArtificialInteligence.rss](https://www.reddit.com/r/ArtificialInteligence.rss) -> [reddit_ArtificialInteligence](rss/reddit_ArtificialInteligence.xml)
 - source005 [https://rsshub.app/telegram/channel/AiIndiaJobs](https://rsshub.app/telegram/channel/AiIndiaJobs) -> [AiIndiaJobs](rss/AiIndiaJobs.xml)
 - source006 [https://www.reddit.com/r/ChatGPT/new.rss](https://www.reddit.com/r/ChatGPT/new.rss) -> [reddit_ChatGPT](rss/reddit_ChatGPT.xml)
 - source007 [https://www.reddit.com/r/GPT3/new.rss](https://www.reddit.com/r/GPT3/new.rss) -> [reddit_GPT3](rss/reddit_GPT3.xml)
 - source008 [https://www.reddit.com/r/LandscapePhotography.rss](https://www.reddit.com/r/LandscapePhotography.rss) -> [reddit_LandscapePhotography](rss/reddit_LandscapePhotography.xml)
 - source009 [https://www.reddit.com/r/streetphotography.rss](https://www.reddit.com/r/streetphotography.rss) -> [reddit_streetphotography](rss/reddit_streetphotography.xml)
 - source010 [https://www.reddit.com/r/FREE/new.rss](https://www.reddit.com/r/FREE/new.rss) -> [reddit_FREE](rss/reddit_FREE.xml)
 - source011 [https://www.reddit.com/r/FREECoursesEveryday/new.rss](https://www.reddit.com/r/FREECoursesEveryday/new.rss) -> [reddit_FREECoursesEveryday](rss/reddit_FREECoursesEveryday.xml)
 - source012 [https://www.reddit.com/r/editors/new.rss](https://www.reddit.com/r/editors/new.rss) -> [reddit_editors](rss/reddit_editors.xml)
 - source013 [https://www.reddit.com/r/software/new.rss](https://www.reddit.com/r/software/new.rss) -> [reddit_software](rss/reddit_software.xml)
 - source014 [https://www.reddit.com/r/programming/new.rss](https://www.reddit.com/r/programming/new.rss) -> [reddit_programming](rss/reddit_programming.xml)
 - source015 [https://www.reddit.com/r/PixelArt/new.rss](https://www.reddit.com/r/PixelArt/new.rss) -> [reddit_PixelArt](rss/reddit_PixelArt.xml)
 - source016 [https://www.reddit.com/r/chiptunes/new.rss](https://www.reddit.com/r/chiptunes/new.rss) -> [reddit_chiptunes](rss/reddit_chiptunes.xml)
 - source017 [https://www.reddit.com/r/youtubeaudiolibrary/new.rss](https://www.reddit.com/r/youtubeaudiolibrary/new.rss) -> [reddit_youtubeaudiolibrary](rss/reddit_youtubeaudiolibrary.xml)
 - source018 [https://www.reddit.com/r/webdev/new.rss](https://www.reddit.com/r/webdev/new.rss) -> [reddit_webdev](rss/reddit_webdev.xml)
 - source019 [https://www.reddit.com/r/opensource/new.rss](https://www.reddit.com/r/opensource/new.rss) -> [reddit_opensource](rss/reddit_opensource.xml)
 - source020 [https://www.producthunt.com/feed](https://www.producthunt.com/feed) -> [producthunt_today](rss/producthunt_today.xml)
 - source021 [https://tg.i-c-a.su/rss/hn_summary](https://tg.i-c-a.su/rss/hn_summary) -> [hn_summary](rss/hn_summary.xml)
 - source022 [https://www.opensourceagenda.com/feeds/projects](https://www.opensourceagenda.com/feeds/projects) -> [opensourceagenda](rss/opensourceagenda.xml)
 - source023 [https://feed.indiehackers.world/posts.rss](https://feed.indiehackers.world/posts.rss) -> [indiehackers-world](rss/indiehackers-world.xml)
 - source024 [https://feed.indiehackers.world/posts.rss?q=productivity](https://feed.indiehackers.world/posts.rss?q=productivity) -> [indiehackers-productivity](rss/indiehackers-productivity.xml)
 - source025 [https://feed.indiehackers.world/posts.rss?group=Automation](https://feed.indiehackers.world/posts.rss?group=Automation) -> [indiehackers-Automation](rss/indiehackers-Automation.xml)
 - source026 [https://feed.indiehackers.world/posts.rss?group=ChatGPT](https://feed.indiehackers.world/posts.rss?group=ChatGPT) -> [indiehackers-ChatGPT](rss/indiehackers-ChatGPT.xml)
 - source027 [https://feed.indiehackers.world/posts.rss?group=No-Code](https://feed.indiehackers.world/posts.rss?group=No-Code) -> [indiehackers-No-Code](rss/indiehackers-No-Code.xml)
 - source028 [https://allainews.com/feed/](https://allainews.com/feed/) -> [allainews-posts](rss/allainews-posts.xml)

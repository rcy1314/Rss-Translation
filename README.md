<div align="center">

# 📡 Rss-Translation

*Multi-language RSS feeds — translated and ready to subscribe*

[![Circle CI](https://img.shields.io/github/actions/workflow/status/rcy1314/Rss-Translation/circle_translate.yml?label=Translation&logo=github)](https://github.com/rcy1314/Rss-Translation/actions)
[![Deploy](https://img.shields.io/github/actions/workflow/status/rcy1314/Rss-Translation/jekyll-gh-pages.yml?label=Deploy&logo=github)](https://github.com/rcy1314/Rss-Translation/actions)
[![License](https://img.shields.io/badge/License-CC--BY--SA--4.0-blue?logo=creativecommons)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

</div>

## 🎯 What is this?

A **RSS translation pipeline** that fetches feeds from around the web and outputs machine-translated XML — ready to drop into any RSS reader (Reeder, Feedly, NetNewsWire, etc.).

## ✨ Features

- 🌐 **Multi-language sources** — Telegram channels, Reddit, Hugging Face, Hacker News, Indie Hackers, Product Hunt, and more
- 🔄 **Auto-translation** — Powered by Google Translate API via GitHub Actions (runs daily)
- 📥 **Standard RSS output** — Compatible with any RSS reader
- ⚡ **No server required** — Pure GitHub Actions + Pages deployment

## 📡 Supported Sources

| # | Source | Category | Output |
|---|--------|----------|--------|
| 001 | Telegram: AI channels | Artificial Intelligence | `rss/Artificial_intelligence_in.xml` |
| 002 | Reddit: r/automation | Automation | `rss/reddit_automation.xml` |
| 003 | Hugging Face Blog | ML/AI | `rss/huggingface_blog.xml` |
| 004 | Reddit: r/GPT3 | LLMs | `rss/reddit_GPT3.xml` |
| 005 | Reddit: r/programming | Programming | `rss/reddit_programming.xml` |
| 006 | Reddit: r/opensource | Open Source | `rss/reddit_opensource.xml` |
| 007 | Reddit: r/webdev | Web Dev | `rss/reddit_webdev.xml` |
| 008 | Reddit: r/software | Software | `rss/reddit_software.xml` |
| 009 | Product Hunt | Products | `rss/producthunt_today.xml` |
| 010 | Hacker News (via TG) | Tech News | `rss/hn_summary.xml` |
| 011 | Indie Hackers | Startups | `rss/indiehackers-world.xml` |
| ... | [See full list →](rss/) | | |

## 🚀 Quick Start

### Subscribe to a translated feed

1. Pick a feed from the [`rss/`](rss/) directory
2. Copy the raw file URL
3. Paste into your RSS reader

### Add a new source

```bash
# Fork the repo and edit sources
# Add your RSS URL to the translation pipeline
```

See [`illustrate/`](illustrate/) for detailed setup instructions.

## 🔧 How It Works

```
RSS Source → RSSHub/Feed → Translation (GitHub Actions) → Translated RSS XML
                                                           ↓
                                                   GitHub Pages (auto-deploy)
```

1. **Fetch** — Raw RSS feeds via RSSHub or direct URLs
2. **Translate** — GitHub Actions triggers translation on schedule
3. **Publish** — Translated XML files deploy to GitHub Pages

## 📦 Live Demo

📖 **View the live page →** https://rcy1314.github.io/Rss-Translation

## 🛠 Tech Stack

| Layer | Tool |
|-------|------|
| Feed aggregation | RSSHub |
| Translation | Google Translate API |
| CI/CD | GitHub Actions |
| Hosting | GitHub Pages |

## 📄 License

CC BY-NC-SA 4.0 — see [LICENSE](LICENSE) for details.

---

README optimized with [Gingiris README Generator](https://gingiris.github.io/github-readme-generator/)

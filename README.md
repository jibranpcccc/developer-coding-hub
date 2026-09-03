# Developer & Coding Communities Hub

> Curated, verified index of 30+ premier developer communities across Python, JavaScript, DevOps, Web3, LeetCode, and AI/ML.

[![Daily Developer Directory Update](https://github.com/jibranpcccc/developer-coding-hub/actions/workflows/daily_update.yml/badge.svg)](https://github.com/jibranpcccc/developer-coding-hub/actions/workflows/daily_update.yml)

## 🌐 Live Deployments
- **GitHub Pages:** [https://jibranpcccc.github.io/developer-coding-hub/](https://jibranpcccc.github.io/developer-coding-hub/)
- **Vercel Production:** [https://developer-coding-hub.vercel.app](https://developer-coding-hub.vercel.app)
- **RSS 2.0 Feed:** [https://jibranpcccc.github.io/developer-coding-hub/feed.xml](https://jibranpcccc.github.io/developer-coding-hub/feed.xml)
- **Sitemap:** [https://jibranpcccc.github.io/developer-coding-hub/sitemap.xml](https://jibranpcccc.github.io/developer-coding-hub/sitemap.xml)

---

## ⚡ Features
- **Developer-First Aesthetic:** Sleek dark/light modes, monospaced tech chips, responsive grid layout.
- **Client-Side Real-Time Filter & Search:** Instant search across titles, technologies, and tags, with platform and category toggle pills.
- **AI Citability Box (`.geo-answer-block`):** Formatted for Google AI Overviews, ChatGPT Search, Perplexity, and LLM web crawlers.
- **Comprehensive Schema.org JSON-LD:**
  - `WebSite`
  - `Organization`
  - `BreadcrumbList`
  - `CollectionPage` (`ItemList` of all indexed communities)
  - `FAQPage` (5 comprehensive developer FAQs)
- **Automated CI/CD Cron Pipeline:**
  - Powered by Google Gemini 2.5 Flash API (`update_content.py`)
  - Scheduled to run every 6 hours (`0 */6 * * *`)
  - Pings Google PubSubHubbub on every release

---

## 🛠️ Stack
- **HTML5 & Tailwind CSS** (Responsive, Dark/Light Themes)
- **Vanilla JavaScript** (Zero dependencies, instant client-side filtering)
- **Python 3.11+** (`build_site.py`, `update_content.py`)
- **Google Gemini 2.5 Flash API** (Autonomous community curation)
- **GitHub Actions & GitHub Pages**
- **Vercel Edge Network**

# 🚀 ANIHUB Master Data Engine
**A High-Performance Anime Discovery API & Dashboard**

ANIHUB is a robust backend engine built with **Python (Flask)** and deployed on **Vercel**. It acts as a bridge between the AniList GraphQL API and TMDB, providing a unified, simplified JSON interface for anime metadata, schedules, and trending content.

## 🌐 Live Access
- **Dashboard:** [https://anihub-orcin.vercel.app/](https://anihub-orcin.vercel.app/)
- **API Base URL:** `https://anihub-orcin.vercel.app/api`

---

## 🛠️ Features
* **Full Metadata**: Deep-dive into anime details including Seiyuu (Voice Actors), Studios, and Rankings.
* **Smart Scheduling**: 7-day airing forecast using localized Unix timestamps.
* **TMDB Integration**: Cross-reference anime titles with TMDB for additional movie/TV metadata.
* **Vibe-Coding Optimized**: Lightweight JSON responses designed for React, Vue, and Vanilla JS frontends.

---

## 📡 API Endpoints

| Endpoint | Description |
| :--- | :--- |
| `GET /api/trending` | Top 25 currently trending anime. |
| `GET /api/this-season` | Most popular shows from the current season. |
| `GET /api/schedule` | Upcoming episodes for the next 7 days. |
| `GET /api/search?q=TITLE` | Search the entire database for a specific title. |
| `GET /api/details/ID` | Get exhaustive data (Characters, Staff, Recommendations) for an ID. |
| `GET /api/top-upcoming` | Most anticipated future releases. |

---

## 🔌 How to Use This API in Your Project

Integrating ANIHUB into your other apps is simple.

### 1. JavaScript (Frontend / Node.js)
```javascript
const fetchAnime = async () => {
    const response = await fetch('[https://anihub-orcin.vercel.app/api/trending](https://anihub-orcin.vercel.app/api/trending)');
    const data = await response.json();
    console.log(data.data.Page.media);
};

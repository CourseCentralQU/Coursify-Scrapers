# 📚 CoursifyQU – Scrapers

A scraping pipeline for Coursify, a course insights platform built for Queen's University students. This repository powers the data collection layer for a system that:

- Displays **historic grade distribution data** for courses.
- Hosts a **RAG-powered chatbot** trained on real student feedback from Reddit and RateMyProfessors.

The chatbot enables Queen’s students to get honest, up-to-date insights on courses and instructors — beyond just what's in the calendar.

---

## 📦 Related Repositories

This project is split across multiple repositories:

| Repository | Purpose |
|-----------|---------|
| [Coursify-Scrapers](https://github.com/CoursifyQU/Coursify-Scrapers) | Handles scraping data from Queen’s calendar, Reddit, and RateMyProf |
| **Coursify-RAG** (🚧 under construction) | Fine-tunes embeddings and manages vector DB for retrieval |
| [Coursify-Web](https://github.com/CoursifyQU/Coursify-WebApp) | Frontend built in Next.js for the public-facing site |

---

## ⚙️ How It Works

Coursify's scraper system is designed to be modular, scalable, and reliable. Here’s a breakdown of how the data collection pipeline functions:

### 1. **GitHub Actions Scheduled Runs**
- **Reddit Scraper:** Runs **weekly** to keep up with fast-paced Reddit discussions.
- **RateMyProfessors Scraper:** Runs **monthly** due to slower data changes.
- **Course Catalog Scraper:** Runs **monthly** to refresh course metadata.

Each scraper is a self-contained Python module, triggered automatically using GitHub Actions. Secrets for Supabase and Reddit credentials are securely stored using GitHub Secrets.

---

### 2. **Scraper Breakdown**

#### 📘 `course-scraper.py`
- Pulls official course listings from [Queen’s Academic Calendar](https://www.queensu.ca/academic-calendar/).
- Extracts course codes, descriptions, requirements, hours, and learning outcomes.
- Uses `upsert` logic to preserve manually entered data like GPA and enrollment size.

#### 🐿️ `reddit-scraper.py`
- Uses PRAW (Python Reddit API Wrapper) to fetch comments from relevant Queen’s subreddits.
- Filters and deduplicates posts before storing them in the `rag_chunks` table.
- Runs every week to keep data fresh and relevant.

#### 🧑‍🏫 `rmp-scraper.py`
- Uses Selenium + BeautifulSoup to scrape professor reviews from RateMyProfessors.
- Handles comment deduplication using the `latest_comment_date` field.
- Maps scraped course mentions to valid Queen’s courses using a custom two-pass cleaning algorithm.

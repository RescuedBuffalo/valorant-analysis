# Valorant Player Performance Modeling & Tracker Tool

## 🔍 Project Overview
This project is a performance analysis and tracking tool for Valorant players, combining scraped match data with user-submitted metrics to:
- Measure player impact (Wins Above Replacement / WAR-style models)
- Identify improvement areas using Aim Lab and in-game metrics
- Build supervised and deep learning models for performance prediction
- Explore potential for smurf detection modeling
- Eventually provide a lightweight web interface for sharing and feedback

We will collect structured player data from:
- Tracker.gg (public player stats, match histories, rivalries, event logs, and map positions)
- Daily warmup performance (Aim Lab tasks)
- Contextual variables (sleep, caffeine, stimulant use, exercise, comms, etc.)
- Manual feedback logs (game feel, mental sharpness, utility usage)

---

## 🎯 Motivation
This project builds off prior experience applying machine learning to sports analytics (e.g. NHL expected goals models and danger zone clustering). Valorant offers rich, structured, publicly accessible data, but no open-source model pipeline exists to quantify:
- A player’s relative in-match value
- How non-skill factors affect performance (e.g., sleep or stimulants)
- True duel win rates and positional effectiveness

---

## 🧠 Modeling Plan

### Primary Goal
**Build a deep learning model to estimate player WAR (Wins Above Replacement) per match.**

#### Inputs:
- Player-level match stats (ACS, KDA, ADR, HS%, opening duels, etc.)
- Duel history and killfeed logs (from event log)
- Aim Lab daily task results (pivoted by task)
- Confounding variables (time of day, stimulant use, stress score, sleep score)

#### Targets:
- Match outcome (team win/loss)
- Round-level outcome (for future modeling)
- Impact rating (scaled contribution)

---

### Baseline Competitor Models
- XGBoost classifier
- Logistic regression
- Linear regression for per-round contribution
- Optional k-means clustering for playstyle profiling

---

## 🕵️ Data Scraping Plan

### Tracker.gg Data (Public)
To scrape:
- Match history & player overview
- Rivalries and duel summary
- Event log (timestamped killfeed)
- Positional maps for each event
- Agent, weapon, map, and scoreboard data

#### Method 1: HTML Parsing (if API restricted)
- Download match HTML via logged-in session
- Parse using BeautifulSoup
- Store as structured JSON or CSV
- Extract duel data from top rivalry section
- Use killfeed event log to reconstruct engagements
- Use screenshot OCR if necessary for coordinates

#### Method 2: Reverse Engineering API
1. Open Dev Tools in Chrome (F12)
2. Go to `Network` tab
3. Navigate through tracker.gg normally
4. Filter by `fetch` or `xhr`
5. Look for any JSON or API endpoints (often under `/v2/...`)
6. Copy the full cURL request and convert using `curlconverter.com` or Postman
7. Rebuild endpoints using Python (`requests` + session cookies or a dummy login)

---

## 🔐 Authentication Plan
- Use a spare Valorant account to log in to tracker.gg and get full access to match breakdowns
- Users must ensure their profiles are public
- Input format: `RiotName#Tag`

---

## 📊 Web App Vision
A Flask or FastAPI app that:
- Takes in player tags
- Scrapes recent games
- Integrates Aim Lab logs (uploaded via Google Sheet or form)
- Shows model output: WAR, aim score, duel rating
- Allows feedback entry and viewing trends over time

Optional: Deploy on Render or Vercel as a simple hosted tool.

---

## 🕵️‍♂️ Smurf Detection (Experimental)
- Use event logs and early-game dominance patterns
- Calculate duel dominance vs account age, match MMR, and kill streaks
- Potential target: `smurf_score = probability(player is outperforming by >X sigma)`

We will revisit this once the core WAR model is built.

---

## 🛠️ Cursor Kickoff Prompt
To start building the scraper in Cursor or your IDE, paste this as your initial dev task:

```plaintext
Build a Python script that:
- Logs in to tracker.gg using a dummy Valorant account
- Accepts a Riot ID and tag
- Scrapes the player’s 5 most recent competitive matches
- For each match, extracts scoreboard, killfeed events, rivalries, and event map data
- Outputs all data to structured JSON or CSV files
- Uses BeautifulSoup or API reverse engineering depending on what is exposed
```
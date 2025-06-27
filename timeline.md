# Project Roadmap: Valorant Performance Tracker

This README outlines the high-level timeline and milestones for building our end-to-end Valorant performance modeling and analysis tool.

---

## 🔰 Phase 1: Planning & Schema (✅ Complete)
- Define full data schema (match, aim lab, contextual)
- Choose storage format (CSV/Parquet/JSON + SQLite for app)
- Draft data safety and Riot compliance policy
- Inventory internal API endpoints to use

---

## 🕸️ Phase 2: Scraper Development
- [ ] Build local-auth wrapper using lockfile and token fetch
- [ ] Implement `match-history` + `match-details` ingestion
- [ ] Add rate limiting, retries, and error handling
- [ ] Save raw JSONs and clean match-level CSVs
- [ ] Optional: add CLI flags or minimal UI for launching scrapes

---

## 📊 Phase 3: Data Logging & Collection
- [ ] Finalize Google Sheet → CSV export for Aim Lab
- [ ] Define structured warmup log format (readiness, sleep, caffeine, etc.)
- [ ] Start collecting 10+ sessions of full data for Aidan and Beau
- [ ] Store all sessions in unified format for modeling

---

## 🔍 Phase 4: Analysis & Modeling
- [ ] Perform EDA on collected data (feature correlations, time series)
- [ ] Build baseline models (XGBoost, logistic regression)
- [ ] Implement deep learning WAR model
- [ ] Add smurf detection and duel dominance model (secondary)
- [ ] Use SHAP and calibration plots for interpretation

---

## 🖥️ Phase 5: Web App & Visualization
- [ ] Build Flask or FastAPI backend
- [ ] Upload/upload Aim Lab logs via UI
- [ ] Display WAR, aim score, duel winrate in dashboard
- [ ] Include user session tracker + feedback entry form
- [ ] Deploy on Render or Vercel

---

## 🔄 Phase 6: Feedback & Publishing
- [ ] Allow data export/download from app
- [ ] Enable delete + reset options
- [ ] Share MVP with trusted testers
- [ ] Publish GitHub repo, write launch post

# Valorant Performance Modeling: Data Schema and Storage Plan

## Objective

To collect, structure, and store all relevant gameplay, aim, and contextual data for building a deep learning model to estimate Wins Above Replacement (WAR) in Valorant, alongside potential applications like smurf detection and duel profiling.

---

## 1. Data Schema Overview

We aim to collect and store a comprehensive set of variables spanning gameplay, aim diagnostics, and contextual confounders. This will allow us to retain modeling flexibility and explore multiple hypotheses.

### Universal Keys (used for joins and identification):

- `riot_id` (string): Player identifier
- `match_id` (string): Unique match key
- `date` (datetime): Session date
- `round_number` (int, optional): For per-round analysis
- `map_name` (string), `agent` (string)

### Match Data (from tracker.gg)

- **Match-Level**: `acs`, `kda_ratio`, `kills`, `adr`, `hs_percent`, `opening_duels_won`, etc.
- **Event Log**: `timestamp`, `killer`, `victim`, `headshot`, `is_trade`, etc.
- **Rivalries**: `duels_won`, `duels_lost`, `rival_riot_id`, `duel_win_rate`
- **Map Positions** (if extractable): `player_position` (x, y), `event_type`, `event_timestamp`

### Contextual Variables

- `sleep_score`, `caffeine_intake_mg`, `adderall_dose_mg`, `stress_level`, `nap_minutes`
- `warmup_type`, `readiness_score`, `fun_score`, `comm_quality`, `work_day`

### Aim Lab Diagnostics (CSV upload)

- `task_name`, `score`, `accuracy`, `reaction_time`, `targets_hit`, `time_taken`
- Pivoted per session into wide format for modeling

---

## 2. Data Storage Plan

### Phase 1: Development & Modeling (Local Files)

**CSV + Parquet Files**

- Best for structured data: match summaries, Aim Lab logs, context logs
- Works seamlessly with pandas and Jupyter for EDA and model training
- Easily version-controlled and lightweight

**JSON Files**

- Ideal for storing complex nested data: killfeed events, map positions
- Supports rich structure from tracker.gg scrapes
- Intermediate format before flattening or analysis

### Phase 2: Web Application (Embedded SQL DB)

**SQLite or DuckDB**

- Embedded database engines suitable for lightweight apps
- Allow structured queries, JOINs, and indexed lookups
- Easy Python and web integration (e.g., Flask/FastAPI)
- Recommended for in-app data filtering, trend viewing, and state persistence

### Phase 3: Scalable/Public Version (Cloud Storage)

If expanded to support multi-user access or public deployment:

- **PostgreSQL** (via Supabase/Render): Scalable relational backend
- **Firebase**: Good for realtime or frontend-heavy designs
- **BigQuery**: For massive event data volumes (e.g., full killfeeds across matches)

---

## Rationale

We prioritize collecting **everything available** to preserve flexibility during the modeling stage. This "collect-max" approach prevents premature assumptions about feature importance. By structuring raw scrape data (JSON), transforming it into clean model-ready formats (CSV/Parquet), and enabling eventual web integration (SQLite), we retain agility while scaling for productization.

The pipeline is designed to minimize data loss, support rapid iteration, and prepare for future user-facing deployment.

---

Let us know if additional schemas (e.g., JSON Schema, SQL DDL) or templates (directory structure, ETL scripts) should be included next.

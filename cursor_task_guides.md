# Cursor Engineering Task Plan: Valorant Tracker Project

This document contains structured instructions for Cursor (AI development assistant) to implement key engineering tasks for the Valorant performance tracker. Each task is self-contained with prompts, goals, and validation logic.

---

## 🔐 Task: Lockfile-based Login

**Objective**: Enable secure local authentication via the Riot lockfile.

### Prompt to Use:

```plaintext
Build a Python function that reads the Riot Client lockfile from the user's local filesystem and extracts the port, password, and protocol. Use this to generate base64-encoded headers for local API authentication.
```

### Requirements:

- Read lockfile at default path on Windows
- Return port, password, and protocol
- Construct `Authorization` header for use in requests

### Self-Validation:

- Print extracted headers (masked) and validate they match the format `Basic base64encoded:user:pass`
- Attempt a test call to `/riotclient/region-locale` to validate the session is active

---

## 📋 Task: Match Scraper JSON → CSV

**Objective**: Convert scraped match JSON into model-ready CSVs

### Prompt to Use:

```plaintext
Build a Python function that reads match-details JSON files and extracts relevant player-level data per match: ACS, kills, deaths, assists, ADR, agent, map, round wins, etc. Save to a structured CSV.
```

### Requirements:

- Flatten nested match structure
- Extract player performance fields
- Output schema: one row per player per match

### Self-Validation:

- Print a preview of the CSV output (first 5 rows)
- Check for nulls and consistent column counts

---

## 🧪 Task: Aim Lab Ingest Parser

**Objective**: Parse CSVs exported from Google Sheets with Aim Lab session results

### Prompt to Use:

```plaintext
Create a parser that reads a CSV with Aim Lab tasks (Gridshot, Microshot Ultimate, etc.), where each row is a daily log. Extract task name, score, accuracy, and timestamp. Output one clean DataFrame per player.
```

### Requirements:

- Handle optional fields (reaction time, task duration)
- Standardize column names
- Support multiple users (optional column)

### Self-Validation:

- Print parsed DataFrame and check for duplicate sessions
- Verify all required columns are present

---

## 📓 Task: Warmup Log Template

**Objective**: Define and validate the format of contextual performance logs

### Prompt to Use:

```plaintext
Generate a JSON schema and corresponding CSV template for logging contextual performance variables: sleep score, caffeine intake, stimulant timing, stress, readiness, warmup routine, and game feel.
```

### Requirements:

- Include types, units, and value ranges
- Provide both CSV column names and JSON field keys

### Self-Validation:

- Generate an example CSV row and confirm it matches the JSON schema

---

## 📊 Task: EDA Notebook Setup

**Objective**: Create an initial Jupyter notebook for exploratory analysis

### Prompt to Use:

```plaintext
Create a Jupyter notebook that reads match stats, Aim Lab scores, and context logs. Generate basic plots and correlation heatmaps between ACS, Aim Lab accuracy, caffeine, and readiness.
```

### Requirements:

- Read multiple CSVs and join by date/match ID
- Use `matplotlib` and `seaborn` for visualizations

### Self-Validation:

- Produce 3+ valid plots
- Log Pearson correlations between ACS and aim/context variables

---

## 🔄 Task: Rate Limiting Wrapper

**Objective**: Add delay and retry logic to API requests

### Prompt to Use:

```plaintext
Implement a Python decorator or request wrapper that adds a 2-second delay between Valorant API calls and retries failed requests up to 3 times with exponential backoff.
```

### Requirements:

- Use `time.sleep`, `requests`, and `functools`
- Print retry attempt logs on failure

### Self-Validation:

- Simulate failed request and confirm retry logic
- Measure time between two consecutive requests

---

## 🧠 Task: Match Details Parser

**Objective**: Extract killfeed, round data, and player positions from `match-details`

### Prompt to Use:

```plaintext
Create a parser that extracts and flattens the `killEvents`, `roundResults`, and `playerLocations` from Valorant match-details JSON. Output one CSV per match with timestamped killfeed and location data.
```

### Requirements:

- Extract killer, victim, weapon, headshot, round, and location (x, y)
- Join all into a clean DataFrame

### Self-Validation:

- Confirm output has consistent timestamps and round numbers
- Cross-validate with total kills reported in match summary

---

Cursor should complete each task independently, validate its results using built-in logic, and log findings. Once validated, the outputs will be staged for integration into our modeling pipeline or web app.

Let me know when you're ready for me to pass the first task into Cursor!


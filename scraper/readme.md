# Scraper API Endpoints Overview

This document outlines the Valorant internal API endpoints we will use in our scraper app, including their purpose, usage context, and integration strategy. All endpoints are derived from the unofficial but well-documented [https://valapidocs.techchrism.me](https://valapidocs.techchrism.me).

---

## 🔐 Authentication (Local Lockfile)

### `GET lockfile`
- **Purpose**: Extracts port, password, and protocol used for local auth.
- **How**: Parse `lockfile` at path:
  - Windows: `C:/Users/<user>/AppData/Local/Riot Games/Riot Client/Config/lockfile`
- **Used For**: Generating access tokens for hitting secure endpoints.

---

## 📋 Match History

### `GET /match-history/v1/history/{puuid}`
- **Purpose**: Retrieves recent match IDs for a player.
- **Used For**: Iterating over recent games to gather full data.
- **Auth**: Requires `access_token` and `entitlement_token`.

---

## 🧠 Match Details

### `GET /match-details/v1/matches/{matchID}`
- **Purpose**: Provides full round-by-round details for a match.
- **Returns**:
  - Player stats (ACS, K/D/A, damage)
  - Killfeed event logs (with timestamps and player positions)
  - Spike plants/defuses
  - Round outcomes and agent info
- **Usage**: Core data for modeling WAR, event timelines, and duel logs.

---

## 🎯 MMR and Ranked Context

### `GET /mmr/v1/players/{puuid}`
- **Purpose**: Returns player’s current MMR and rank tier.
- **Used For**: Smurf detection and relative performance calibration.

### `GET /account-xp/v1/players/{puuid}`
- **Purpose**: Returns account level and XP progress.
- **Used For**: Identifying alt/smurf accounts.

### `GET /competitive/v1/players/{puuid}`
- **Purpose**: Historical ranked data including placement and act rank.
- **Used For**: Longitudinal MMR tracking and performance baseline.

---

## 🧪 Optional: Local WebSocket & Pre-Game State

### `GET /pregame/v1/players/{puuid}`
- **Purpose**: Detects if the player is currently in a match lobby.
- **Use Case**: Skip scraping if user is in-game (not needed now).

### `WebSocket / liveclientdata`
- **Purpose**: Real-time match telemetry (positions, kills, etc.)
- **Status**: Not used in this project (live scraping disabled).

---

## 🚦 Integration Strategy

1. **Step 1**: Use lockfile to get `access_token`, `entitlement_token`, and `puuid`
2. **Step 2**: Call `/match-history` to get recent match IDs
3. **Step 3**: Loop over `/match-details` to collect event logs and stats
4. **Step 4**: Supplement with `/mmr` and `/competitive` for metadata
5. **Step 5**: Store all JSONs, then transform to CSV/Parquet for modeling

---

## ⚠️ Notes
- All endpoints are reverse-engineered; subject to change across patches
- Include retry logic and request throttling (1–2s delay)
- Store raw JSONs to preserve source fidelity

This readme is the source of truth for our scraper integration. Keep it updated as API methods evolve or expand.

## 📊 VLR.gg Pro Match Scraper

The `vlr_scraper.py` script collects public statistics from [VLR.gg](https://www.vlr.gg) match pages. It is aimed at gathering
professional match data for modeling and analysis.

### Capabilities
- Retrieve match listings for a given event.
- Parse per-map score, team compositions, and detailed player statistics (ACS, K/D/A, KAST, ADR, HS%, FK, FD, etc.).
- Extract round-by-round results for each map.
- Capture performance metrics such as multi-kills, operator kills, and player-vs-player kill counts.
- Output data as structured JSON for downstream analysis.

### Usage

```bash
python scraper/vlr_scraper.py <match-url> -o match.json
```

Replace `<match-url>` with the full URL of a match page on VLR.gg. The script prints the scraped data to stdout or stores it in
`match.json` when the `-o/--out` option is provided.

> **Note:** VLR.gg may throttle or block automated requests. Consider including delays between requests and caching results.


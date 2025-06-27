# Data Ethics, Safety, and Storage Policy for Valorant Performance Tracker

## Objective
To outline ethical, secure, and Riot-aligned data practices for our Valorant performance modeling project. This policy ensures that any data scraping, storage, or analysis respects Riot's unofficial API boundaries and protects user privacy.

---

## Guiding Principles

- **User-Initiated Only**: All data scraping must be explicitly triggered by the user.
- **Post-Match Only**: No live or in-match scraping will be conducted to avoid any cheating concerns.
- **Player-Owned Data**: We will only collect data from players who have opted in and authenticated their own accounts.
- **Secure and Transparent**: All collected data will be handled securely and with user awareness.

---

## Data Collection Constraints

### ✅ What’s Allowed
- Scraping public data (match history, event logs) from tracker.gg or Valorant internal APIs
- Running data collection scripts **after matches are complete**
- Storing match, aim, and contextual logs **for users who explicitly opt in**
- Rate-limited scraping (e.g., 1–2 requests per second)

### ❌ What’s Not Allowed
- Scraping data from users who have not opted in
- Collecting data mid-match or during gameplay
- Accessing private or sensitive Riot endpoints
- Deploying scraping tools as public web services without rate limits or opt-in

---

## User Consent & Transparency

Users must:
- Initiate the scrape manually (CLI flag, button click, or trigger)
- Confirm understanding of what will be collected and how it’s stored
- Be able to view, export, or delete their data at any time

We will provide:
- A human-readable Data Use Policy
- Per-session confirmation of scrape and storage
- Optional toggles for local-only vs cloud storage

---

## Data Scope

We will collect the following **only after matches**:
- Match metadata (map, agent, ACS, KDA, etc.)
- Event logs (killfeed, damage, round outcomes)
- Aim Lab session logs (manual upload)
- Contextual session data (sleep, caffeine, readiness, etc.)

We will **not**:
- Collect or stream data during gameplay
- Inject or overlay content in the Valorant client
- Use any third-party authentication or memory access tools

---

## Storage Policies

- All data is associated only with the user who initiated collection
- Users can choose to store data locally or opt into dashboard sync
- No raw data is shared or sold
- Anonymized, aggregated metrics may be used for academic or leaderboard insights (with consent)

---

## Rate Limiting & Technical Safeguards

- Requests to Riot endpoints will be throttled (minimum 1–2s delay)
- Data will be fetched in batches (e.g., last 5–10 matches)
- Local auth via lockfile will be used to avoid sensitive credential handling

---

## Legal & Ethical Alignment

This project aligns with Riot’s spirit of open data access and community tooling:
- It is player-facing, opt-in, and does not impact gameplay
- It respects user consent, avoids abuse, and remains non-commercial (unless explicitly approved)
- It complements existing tools like tracker.gg and Aim Lab, which operate under similar principles

---

## TL;DR Safety Rules
| Policy Item | Status |
|-------------|--------|
| Post-match scraping only | ✅ |
| Player opt-in required | ✅ |
| Rate limiting enforced | ✅ |
| Live match or client modding | ❌ |
| Private data scraping | ❌ |

---

This document should guide any future public launch, open-source release, or productization efforts. Let users track their performance — ethically, securely, and within Riot’s tolerated bounds.


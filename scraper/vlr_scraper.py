"""Scraper for pro Valorant statistics from VLR.gg.

This module downloads match pages from VLR.gg and extracts
structured statistics at the match, map, team and player levels.
The goal is to provide highly granular data suitable for predictive
modeling of professional Valorant matches.

Example:
    python vlr_scraper.py https://www.vlr.gg/78811/... -o match.json
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.vlr.gg"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/113.0 Safari/537.36"
    )
}


@dataclass
class PlayerStats:
    """Container for a player's statistics for a single map."""

    name: str
    ign: Optional[str]
    agent: Optional[str]
    rating: Optional[float]
    acs: Optional[int]
    kills: Optional[int]
    deaths: Optional[int]
    assists: Optional[int]
    kast: Optional[float]
    adr: Optional[float]
    hs_pct: Optional[float]
    fk: Optional[int]
    fd: Optional[int]
    multikills: Optional[Dict[str, int]] = None
    op_kills: Optional[int] = None
    op_deaths: Optional[int] = None
    player_vs_player: Optional[Dict[str, int]] = None


@dataclass
class MapStats:
    """Statistics for a single map within a match."""

    map: str
    team1: str
    team2: str
    score1: int
    score2: int
    players1: List[PlayerStats]
    players2: List[PlayerStats]
    rounds: List[Dict[str, str]]


@dataclass
class MatchStats:
    """Top-level container for a match."""

    match_id: str
    event: Optional[str]
    team1: str
    team2: str
    score1: int
    score2: int
    maps: List[MapStats]


class VLRStatsScraper:
    """Scrapes match and event information from VLR.gg."""

    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def fetch(self, url: str) -> BeautifulSoup:
        """Retrieve a page and return a BeautifulSoup parser."""
        resp = self.session.get(url)
        resp.raise_for_status()
        return BeautifulSoup(resp.text, "lxml")

    # ------------------------------------------------------------------
    # Event utilities
    # ------------------------------------------------------------------
    def get_event_matches(self, event_id: str) -> List[str]:
        """Return a list of match URLs for a given event ID."""
        url = f"{BASE_URL}/event/{event_id}"
        soup = self.fetch(url)
        links = []
        for a in soup.select("a.match-item"):  # match listing entries
            href = a.get("href")
            if href and href.startswith("/"):
                links.append(BASE_URL + href.split("?")[0])
        return links

    # ------------------------------------------------------------------
    # Match parsing
    # ------------------------------------------------------------------
    def parse_match(self, url: str) -> MatchStats:
        """Parse a VLR.gg match page and return structured statistics."""
        soup = self.fetch(url)

        match_id = re.search(r"(\d+)", url).group(1)

        header = soup.select_one(".match-header")
        team_elems = header.select(".match-header-link .match-header-team-name")
        team1 = team_elems[0].get_text(strip=True)
        team2 = team_elems[1].get_text(strip=True)
        scores = [int(s.get_text(strip=True)) for s in header.select(".match-header-vs-score")] 
        score1, score2 = scores if len(scores) == 2 else (0, 0)

        event_elem = soup.select_one(".match-header-event a")
        event = event_elem.get_text(strip=True) if event_elem else None

        maps: List[MapStats] = []
        for container in soup.select("div.vm-stats-container"):  # one per map
            map_name = container.select_one(".map-header .map").get_text(strip=True)

            team_names = [t.get_text(strip=True) for t in container.select(".map-header .team")] 
            score_elems = container.select(".map-header .score")
            scores = [int(s.get_text(strip=True)) for s in score_elems]

            players_tables = container.select("table")
            players1 = self._parse_players(players_tables[0]) if players_tables else []
            players2 = self._parse_players(players_tables[1]) if len(players_tables) > 1 else []

            # Enrich players with performance statistics
            self._parse_performance(container, players1, players2)

            rounds = self._parse_rounds(container)

            maps.append(
                MapStats(
                    map=map_name,
                    team1=team_names[0] if team_names else team1,
                    team2=team_names[1] if len(team_names) > 1 else team2,
                    score1=scores[0] if scores else 0,
                    score2=scores[1] if len(scores) > 1 else 0,
                    players1=players1,
                    players2=players2,
                    rounds=rounds,
                )
            )

        return MatchStats(
            match_id=match_id,
            event=event,
            team1=team1,
            team2=team2,
            score1=score1,
            score2=score2,
            maps=maps,
        )

    # ------------------------------------------------------------------
    def _parse_players(self, table: BeautifulSoup) -> List[PlayerStats]:
        players: List[PlayerStats] = []
        for row in table.select("tbody tr"):
            cells = row.select("td")
            if not cells:
                continue
            name_elem = cells[0].select_one(".text-of a")
            name = name_elem.get_text(strip=True) if name_elem else cells[0].get_text(strip=True)
            ign = name_elem.get("href") if name_elem else None

            agent_elem = cells[0].select_one(".stats-player-img img")
            agent = agent_elem.get("alt") if agent_elem else None

            def to_int(text: str) -> Optional[int]:
                return int(text) if text and text.isdigit() else None

            def to_float(text: str) -> Optional[float]:
                text = text.replace("%", "") if text else text
                try:
                    return float(text)
                except (TypeError, ValueError):
                    return None

            rating = to_float(cells[1].get_text(strip=True)) if len(cells) > 1 else None
            acs = to_int(cells[2].get_text(strip=True)) if len(cells) > 2 else None

            kda_text = cells[3].get_text(strip=True) if len(cells) > 3 else ""
            k, d, a = (None, None, None)
            if kda_text:
                parts = re.split(r"[\s/]+", kda_text)
                if len(parts) >= 3:
                    k, d, a = map(to_int, parts[:3])

            plus = to_int(cells[4].get_text(strip=True)) if len(cells) > 4 else None
            kast = to_float(cells[5].get_text(strip=True)) if len(cells) > 5 else None
            adr = to_float(cells[6].get_text(strip=True)) if len(cells) > 6 else None
            hs_pct = to_float(cells[7].get_text(strip=True)) if len(cells) > 7 else None
            fk = to_int(cells[8].get_text(strip=True)) if len(cells) > 8 else None
            fd = to_int(cells[9].get_text(strip=True)) if len(cells) > 9 else None

            players.append(
                PlayerStats(
                    name=name,
                    ign=ign,
                    agent=agent,
                    rating=rating,
                    acs=acs,
                    kills=k,
                    deaths=d,
                    assists=a,
                    kast=kast,
                    adr=adr,
                    hs_pct=hs_pct,
                    fk=fk,
                    fd=fd,
                )
            )
        return players

    # ------------------------------------------------------------------
    def _parse_performance(
        self,
        container: BeautifulSoup,
        players1: List[PlayerStats],
        players2: List[PlayerStats],
    ) -> None:
        """Parse the performance tab to enrich player statistics.

        The performance tab includes multi-kill counts, operator kills,
        and a player-vs-player kill matrix. Because we cannot rely on
        JavaScript to switch tabs, all of the tables are present in the
        HTML and we heuristically identify them by their column headers.
        """

        tables = container.select("table")[2:]  # skip main scoreboard tables
        player_map = {p.name: p for p in players1 + players2}

        for table in tables:
            headers = [th.get_text(strip=True).lower() for th in table.select("th")]
            header_set = set(headers)

            # Multi-kill table has 2k/3k/4k/5k columns
            if {"2k", "3k", "4k", "5k"}.issubset(header_set):
                for row in table.select("tbody tr"):
                    cols = row.select("td")
                    if not cols:
                        continue
                    name = cols[0].get_text(strip=True)
                    stats = {}
                    labels = ["2k", "3k", "4k", "5k"]
                    for label, cell in zip(labels, cols[1:5]):
                        text = cell.get_text(strip=True)
                        try:
                            stats[label] = int(text)
                        except ValueError:
                            stats[label] = 0
                    if name in player_map:
                        player_map[name].multikills = stats

            # Operator kill table (contains 'op' in headers)
            elif any("op" in h for h in headers):
                for row in table.select("tbody tr"):
                    cols = row.select("td")
                    if not cols:
                        continue
                    name = cols[0].get_text(strip=True)
                    op_k = cols[1].get_text(strip=True) if len(cols) > 1 else ""
                    op_d = cols[2].get_text(strip=True) if len(cols) > 2 else ""
                    try:
                        op_kills = int(op_k)
                    except ValueError:
                        op_kills = None
                    try:
                        op_deaths = int(op_d)
                    except ValueError:
                        op_deaths = None
                    if name in player_map:
                        player_map[name].op_kills = op_kills
                        player_map[name].op_deaths = op_deaths

            # Player vs player matrix: blank first header followed by opponent names
            elif headers and headers[0] == "":
                opponents = headers[1:]
                for row in table.select("tbody tr"):
                    cols = row.select("td")
                    if not cols:
                        continue
                    name = cols[0].get_text(strip=True)
                    matrix = {}
                    for opp, cell in zip(opponents, cols[1:]):
                        text = cell.get_text(strip=True)
                        try:
                            matrix[opp] = int(text)
                        except ValueError:
                            matrix[opp] = None
                    if name in player_map:
                        player_map[name].player_vs_player = matrix

    # ------------------------------------------------------------------
    def _parse_rounds(self, container: BeautifulSoup) -> List[Dict[str, str]]:
        rounds: List[Dict[str, str]] = []
        for i, rnd in enumerate(container.select(".vm-stats-rounds .rnd"), start=1):
            classes = rnd.get("class", [])
            winner = "team1" if "mod-t1" in classes else "team2"
            result = ""  # e.g., clutch/thrifty/etc.
            for cls in classes:
                if cls.startswith("mod-") and cls not in {"mod-t1", "mod-t2", "mod-win", "mod-loss", "rnd"}:
                    result = cls.replace("mod-", "")
            rounds.append({"round": i, "winner": winner, "result": result})
        return rounds


def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape Valorant pro match stats from VLR.gg")
    parser.add_argument("match", help="Match URL or ID to scrape")
    parser.add_argument("-o", "--out", help="Write output JSON to file")
    args = parser.parse_args()

    scraper = VLRStatsScraper()
    url = args.match if args.match.startswith("http") else f"{BASE_URL}/{args.match}"
    stats = scraper.parse_match(url)
    data = asdict(stats)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    else:
        print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()

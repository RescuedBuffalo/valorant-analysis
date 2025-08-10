import os
import sys

from bs4 import BeautifulSoup

# Ensure the repository root is on the Python path so that the `scraper`
# package can be imported when tests are executed from any location.
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from scraper.vlr_scraper import VLRStatsScraper, PlayerStats


def test_parse_players_basic():
    html = '''
    <table>
      <tbody>
       <tr>
        <td>
          <div class="text-of"><a href="/player1">Player1</a></div>
          <div class="stats-player-img"><img alt="Sova"/></div>
        </td>
        <td>1.1</td>
        <td>200</td>
        <td>10 / 5 / 3</td>
        <td>+5</td>
        <td>75%</td>
        <td>150</td>
        <td>25%</td>
        <td>2</td>
        <td>1</td>
       </tr>
      </tbody>
    </table>
    '''
    soup = BeautifulSoup(html, 'lxml')
    table = soup.select_one('table')
    scraper = VLRStatsScraper()
    players = scraper._parse_players(table)
    assert len(players) == 1
    p = players[0]
    assert p.name == 'Player1'
    assert p.agent == 'Sova'
    assert p.rating == 1.1
    assert p.acs == 200
    assert (p.kills, p.deaths, p.assists) == (10, 5, 3)
    assert p.kast == 75.0
    assert p.adr == 150.0
    assert p.hs_pct == 25.0
    assert p.fk == 2
    assert p.fd == 1


def test_parse_performance_and_rounds():
    html = '''
    <div class="vm-stats-container">
       <table></table>
       <table></table>
       <table>
        <thead><tr><th>Player</th><th>2K</th><th>3K</th><th>4K</th><th>5K</th></tr></thead>
        <tbody>
          <tr><td>Player1</td><td>1</td><td>0</td><td>0</td><td>0</td></tr>
          <tr><td>Player2</td><td>0</td><td>1</td><td>0</td><td>0</td></tr>
        </tbody>
       </table>
       <table>
        <thead><tr><th>Player</th><th>Op Kills</th><th>Op Deaths</th></tr></thead>
        <tbody>
         <tr><td>Player1</td><td>2</td><td>1</td></tr>
         <tr><td>Player2</td><td>0</td><td>3</td></tr>
        </tbody>
       </table>
       <table>
        <thead><tr><th></th><th>Player1</th><th>Player2</th></tr></thead>
        <tbody>
         <tr><td>Player1</td><td>-</td><td>1</td></tr>
         <tr><td>Player2</td><td>0</td><td>-</td></tr>
        </tbody>
       </table>
       <div class="vm-stats-rounds">
         <span class="rnd mod-t1 mod-flawless"></span>
         <span class="rnd mod-t2 mod-clutch"></span>
       </div>
    </div>
    '''
    soup = BeautifulSoup(html, 'lxml')
    container = soup.select_one('div.vm-stats-container')
    scraper = VLRStatsScraper()
    players1 = [PlayerStats(name='Player1', ign=None, agent=None, rating=None, acs=None,
                            kills=None, deaths=None, assists=None, kast=None, adr=None,
                            hs_pct=None, fk=None, fd=None)]
    players2 = [PlayerStats(name='Player2', ign=None, agent=None, rating=None, acs=None,
                            kills=None, deaths=None, assists=None, kast=None, adr=None,
                            hs_pct=None, fk=None, fd=None)]
    scraper._parse_performance(container, players1, players2)
    assert players1[0].multikills == {'2k': 1, '3k': 0, '4k': 0, '5k': 0}
    assert players2[0].multikills == {'2k': 0, '3k': 1, '4k': 0, '5k': 0}
    assert (players1[0].op_kills, players1[0].op_deaths) == (2, 1)
    assert (players2[0].op_kills, players2[0].op_deaths) == (0, 3)
    assert players1[0].player_vs_player['player2'] == 1
    assert players2[0].player_vs_player['player1'] == 0

    rounds = scraper._parse_rounds(container)
    assert rounds == [
        {'round': 1, 'winner': 'team1', 'result': 'flawless'},
        {'round': 2, 'winner': 'team2', 'result': 'clutch'},
    ]

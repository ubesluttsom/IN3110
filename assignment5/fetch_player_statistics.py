import re
from os import makedirs
from bs4 import BeautifulSoup
from requesting_urls import get_html
from filter_urls import find_urls

def extract_url(html):
  """ Extract URL of a team's Wikipedia article from playoff brackets.
      Args:
        html (string): html to extract URL from
      Returns:
        Extracted wiki article URL
  """
  # This procedure is not needed with my implementation of `extract_teams()` as
  # it is.
  pass

def extract_teams(url="https://en.wikipedia.org/wiki/2021_NBA_playoffs"):
  """ Extract names of each team in playoff brackets.
      Args:
        url (string): URL to NBA playoffs Wikipedia article.
      Returns:
        Dictionary of extracted team names
  """

  # Using a dictionary. This way I can store both names and links. And, as a
  # bonus, dictionary keys is by definition a *set*, i.e. no multiple listings
  # of teams automatically.
  teams = dict()

  html = get_html(url)
  soup = BeautifulSoup(html, "html.parser")

  # Find the right table and extract table rows
  bracket_header = soup.find(id="Bracket")
  bracket_table  = bracket_header.find_all_next("table")[0]
  bracket_trs    = bracket_table.find_all("tr")

  # Iterate over all table rows, choose the ones with the right amount of
  # columns, from these extract team name and link and store in dictionary.
  # Expand relative links, as needed.
  for tr in bracket_trs:
    bracket_tds = tr.find_all("td")
    if not len(bracket_tds) in {5, 6, 7}:
      continue
    else:
      for td in bracket_tds:
        for a in td.find_all("a"):
          url  = a.get('href')
          team = a.get_text()
          if url[:2] == '/w':
            teams[team] = "https://en.wikipedia.org" + url
          elif url[:2] == '//':
            teams[team] = "https:" + url
          else:
            teams[team] = url

  return teams

def extract_players(url):
  """ Extract names of each player of a team in a season.
      Args:
        url (string): URL to Wikipedia article of the team's season.
      Returns:
        Dictionary of extracted team players, and link to their Wikipedia
        article.
  """

  # Using a dictionary. This way I can store both names and links. And, as a
  # bonus, dictionary keys is by definition a *set*, i.e. no multiple listings
  # of players automatically.
  players = dict()

  html = get_html(url)
  soup = BeautifulSoup(html, "html.parser")

  # Find the right table and extract table rows
  roster_header = soup.find(id="Roster")
  roster_table  = roster_header.find_all_next("table")[0]
  roster_trs    = roster_table.find_all("tr")

  # Iterate over all table rows, choose the ones with the right amount of
  # columns, from these extract player name + link and store in dictionary.
  # Expand relative links, as needed.
  for tr in roster_trs:
    table_columns = tr.find_all("td")

    # Skip some rows
    if len(table_columns) < 3:
      continue

    # Hard-coded player name column, for now.
    player_name = table_columns[2]
    for a in player_name.find_all("a"):
      url  = a.get('href')
      name = a.get_text()
      if url[:2] == '/w':
        players[name] = "https://en.wikipedia.org" + url
      elif url[:2] == '//':
        players[name] = "https:" + url
      else:
        players[name] = url

  return players

def extract_player_statistics(url):
  """ Extract statistics of an NBA player.
      Args:
        url (string): URL to Wikipedia article of the player.
      Returns:
        Dictionary of extracted statistics.
  """
  stats = dict()

  html = get_html(url)
  soup = BeautifulSoup(html, "html.parser")

  # Find the right table and extract table rows
  regular_season_header = soup.find(id="Regular_season")

  # Return `None` if we can't find the «Regular season» table
  if regular_season_header is None:
    return None

  regular_season_table  = regular_season_header.find_all_next("table")[0]
  regular_season_trs    = regular_season_table.find_all("tr")

  # Make a dictionary out of the first row, i.e. the header of the table
  table_header = {}
  for idx, th in enumerate(regular_season_trs[0].find_all("th")):
    table_header[idx] = th.get_text().split('\n')[0]

  # Iterate over all table rows, choose the ones with the right amount of
  # columns, from these extract player name + link and store in dictionary.
  # Expand relative links, as needed.
  for tr in regular_season_trs:
    table_columns  = tr.find_all("td")

    # Skip header and everything else but the 2020–21 season.
    if len(table_columns) != 13:
      continue
    elif table_columns[0].get_text() != '2020–21\n':
      continue

    # Look up index in header dictionary, then store stat with that as key.
    for idx, td in enumerate(table_columns):
      stats[table_header[idx]] = td.get_text().split('\n')[0]

  return stats

if __name__ == '__main__':
  teams = extract_teams()
  # print(teams)
  # print(teams.keys())

  player_stats = {}

  for team_urls in teams.values():
    players = extract_players(team_urls)
    # print(players)
    # print(players.keys())
    for player, player_url in players.items():
      player_stats[player] = extract_player_statistics(player_url)

  for player, stats in player_stats.items():
    if stats == None:
      print(f"{player}: None")
    else:
      try:
        print(f"{player}: PPG = {stats['PPG']}, BPG = {stats['BPG']}, RPG = {stats['RPG']}")
      except KeyError as err:
        print(f"{player}: KeyError! Could not find {err}.")

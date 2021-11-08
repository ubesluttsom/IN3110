import re
from os import makedirs
from bs4 import BeautifulSoup
from requesting_urls import get_html

def extract_events(url, debug=False) :
  """ Extract date, venue and discipline for competitions.  Your
  documentation here.
  Args:
    url(str): The url to extract events from.
  Returns:
    table_info(list of lists): A nested list where the rows represent each
    race date, and the columns are [date, venue, discipline].
  """
  disciplines = {
    "DH" : "Downhill",
    "SL" : "Slalom",
    "GS" : "Giant Slalom",
    "SG" : "Super Giant Slalom",
    "AC" : "Alpine Combined",
    "PG" : "Parallel Giant Slalom",
  }

  # get the html
  html = get_html(url)

  # make soup
  soup = BeautifulSoup(html, "html.parser")

  # Find the tag that contains the Calendar header span
  calendar_header = soup.find(id="Calendar")

  # Find the following table
  calendar_table = calendar_header.find_all_next("table")[0]

  # Find the rows of the first table
  rows = calendar_table.find_all("tr")

  # try parsing the row of `th` cells to identify the indices for Event, Venue,
  # and Type (discipline)

  found_event = None
  found_venue = None
  found_discipline = None
  found_date = None
  # Saving all necessary values in the list under
  events = []

  # how many columns does a full row have?
  full_row_length = 11
  # some rows have fewer because the `venue` spans multiple rows,
  # short_row_length means a repeated venue, which should be reused from the
  # previous iteration
  short_row_length = full_row_length - 2

  for row in rows:
    cells = row.find_all("td")

    # to help figure out what to write, show the contents of each row
    if debug:
      print(f"new row: {len(cells)} cells")
      for idx, cell in enumerate(cells):
        print(f"  cell {idx}: {cell}")

    # some rows have one number of columns, if it’s a different number (usually
    # 0 or 1), ignore it
    if not len(cells) in {9, 10, 11}:
      # skip rows that don’t have most columns
      continue
    # Hardcoding indexes works for now (you should find them using the Header!) TODO
    event = cells[1]
    # An event seems to always be a 1–3 digit number, so we can check that we
    # have an event with a simple regex
    if re.match(r"\d{1,3}", event.text.strip()):
      found_event = event.text.strip()
    else:
      found_event = None

    # Extract date
    found_date = cells[2].text.strip()

    if len(cells) == full_row_length:
      # If event is cancelled, the index below might need to be shifted.
      venue_cell = cells[3]
      found_venue = venue_cell.text.strip()
      discipline_index = 5
    else:
      # repeated venue, discipline is in a different column where is the
      # discipline column?
      discipline_index =  5 - (full_row_length - len(cells))

    discipline = cells[discipline_index]
    # find the discipline id
    # can you make a regex to find only the keys of the disciplines dictionary?
    # ( DH | ... )
    discipline_regex = '(DH|SL|GS|SG|AC|PG)'

    # this can also be done with just HTML parsing
    discipline_match = re.search(discipline_regex, discipline.text.strip())
    if discipline_match:
      # look up the full discipline name
      found_discipline = disciplines[discipline_match[0]]
    else:
      found_discipline = None

    if found_venue and found_event and found_discipline:
      # if we found something
      events.append((found_date, found_event, found_venue, found_discipline))

  return events

def create_betting_slip(events, save_as):
  """ Saves a markdown format betting slip to the location
  `./datetime_filter/<save_as>.md`.
  Args:
    events (list): takes a list of 3 - tuples containing date, venue and
                   type for each event.
    save_as (string): filename to save the markdown betting slip as.
  """
  # ensure directory exists
  makedirs("datetime_filter", exist_ok=True)
  with open(f"./datetime_filter/{save_as}.md", "w") as out_file:
    out_file.write(f"# BETTING SLIP ({save_as})\n\nName:\n\n")
    out_file.write( "Date | Event | Venue | Discipline | Who wins?\n")
    out_file.write( "--- | --- | --- | --- | ---\n")
    for e in events :
      date, event, venue, discipline = e
      out_file.write(f"{date} | {event} | {venue} | {discipline} | \n")

if __name__ == '__main__':
  events = extract_events("https://en.wikipedia.org/wiki/2021%E2%80%9322_FIS_Alpine_Ski_World_Cup")
  for event in events:
    print(event)
  create_betting_slip(events, "2021-22_FIS_Alpine_Ski_Cup")

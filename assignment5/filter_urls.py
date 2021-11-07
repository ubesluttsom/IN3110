import re
from requesting_urls import get_html

def find_urls(html_string, base_url=None, output=None):
  """ Excellent Docstring here
  """

  url_list = re.findall(r'href="([^"#]+)["#]', html_string)

  url_set = set()

  for url in url_list:
    if re.match(r'(^//.*)', url):
      url_set.add("https:" + url)
    elif re.match(r'(^/[^/].*)', url):
      url_set.add(base_url + url)
    else:
      url_set.add(url)

  if output != None:
    with open(output, mode='wt') as file:
      for url in url_set:
        file.write(url + '\n')

  return list(url_set)

def find_articles(html_string, output=None, base_url="https://en.wikipedia.org"):
  """ Absent Docstring here
  """

  url_set = set(find_urls(html_string, base_url=base_url))

  article_set = set()
  for url in url_set:
    if re.match(r'.*wikipedia.org\/wiki\/[^:]+$', url):
      article_set.add(url)

  if output != None:
    with open(output, mode='wt') as file:
      for article in article_set:
        file.write(article + '\n')

  return list(article_set)

def test_find_urls() :
  html = """
  <a href="#fragment-only"> anchor link </a>
  <a id="some-id" href="/relative/path#fragment"> relative link </a>
  <a href="//other.host/same-protocol"> same-protocol link </a>
  <a href="https://example.com"> absolute URL </a>
  """
  urls = find_urls(html, base_url ="https://en.wikipedia.org")
  assert set(urls) == {
      "https://en.wikipedia.org/relative/path",
      "https://other.host/same-protocol",
      "https://example.com"
      }

def test_find_articles() :
  html = get_html("http://en.wikipedia.org/wiki/Studio_Ghibli")
  urls = find_articles(html, base_url ="https://en.wikipedia.org")
  print(urls)

if __name__ == '__main__':
  test_find_urls()
  base  = "https://en.wikipedia.org"
  html1 = get_html("https://en.wikipedia.org/wiki/Nobel_Prize")
  html2 = get_html("https://en.wikipedia.org/wiki/Bundesliga")
  html3 = get_html("https://en.wikipedia.org/wiki/2019%E2%80%9320_FIS_Alpine_Ski_World_Cup")
  find_urls(html1, base_url=base, output="Nobel_Prize.urls.txt")
  find_urls(html2, base_url=base, output="Bundesliga.urls.txt")
  find_urls(html3, base_url=base, output="Alpine_Ski.urls.txt")
  find_articles(html1, base_url=base, output="Nobel_Prize.articles.txt")
  find_articles(html2, base_url=base, output="Bundesliga.articles.txt")
  find_articles(html3, base_url=base, output="Alpine_Ski.articles.txt")

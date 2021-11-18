import requests as req
from os import makedirs

def get_html(url, params=None, output=None):
  """Will make a request for a URL from a given website.

  Parameters:
  url: website URL
  params: dictionary containing key/value pairs to request
  a specific type of data, optional
  output: name of file where html is saved, optional

  Returns:
  html data from given URL
  """

  response = req.get(url, params=params)

  if output != None:
    makedirs("requesting_urls", exist_ok=True)
    with open(f"./requesting_urls/{output}", mode='wt') as file:
      file.write(response.text)

  return response.text

if __name__ == '__main__':
  html_str = get_html("http://en.wikipedia.org/wiki/Studio_Ghibli", output="Studio_Ghibli.html")
  html_str = get_html("http://en.wikipedia.org/wiki/Star_Wars", output="Star_Wars.html")
  html_str = get_html("http://en.wikipedia.org/w/index.php", params={"title": "Main_page", "action": "info"}, output="Main_page_info.html")

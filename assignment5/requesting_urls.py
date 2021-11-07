import requests as req

def get_html(url, params=None, output=None):
  """ My detailed Docstring Here
  """

  response = req.get(url, params=params)

  if output != None:
    with open(output, mode='wt') as file:
      file.write(response.text)

  return response.text

if __name__ == '__main__':
  html_str = get_html("http://en.wikipedia.org/wiki/Studio_Ghibli", output="Studio_Ghibli.html")
  html_str = get_html("http://en.wikipedia.org/wiki/Star_Wars", output="Star_Wars.html")
  html_str = get_html("http://en.wikipedia.org/w/index.php", params={"title": "Main_page", "action": "info"}, output="Main_page_info.html")
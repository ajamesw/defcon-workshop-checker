from defcon_workshop_checker.defcon_checker import getDefConLinks, checkLinksForStatus, URL 
import requests
from bs4 import BeautifulSoup, SoupStrainer

def test_base_url():
  assert '.html' in URL

# test to see if link list is populated from workshop page
def test_reglist():
  # collect registration links to check for openings
  regList = []
  res = requests.get(URL)

  for link in BeautifulSoup(res.text, 'html.parser', parse_only=SoupStrainer('a')):
    if link.has_attr('href'):
      if link.text.startswith('https://dc25_'):
        regList.append(link.text)

  assert len(regList) > 0
  for link in regList:
    assert '.com' in link

def test_link_status():
  pass

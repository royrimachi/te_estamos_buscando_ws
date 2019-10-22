import requests
import bs4

from common import config


class HomePage:
  
  def __init__(self, site_uid, url):
    self._config = config()['sites'][site_uid]
    self._queries = self._config['queries']
    self._html = None

    self._visit(url)

  @property
  def people_links(self):
    link_list = []
    for link in self._select(self._queries['people_links']):
      if link and link.has_attr('href'):
        link_list.append(link)

    return set(link['href'] for link in link_list)

  def _select(self, query_string):
    return self._html.select(query_string)

  def _visit(self, url):
    response = requests.get(url)

    # check if request was completed correctly    
    response.raise_for_status()

    self._html = bs4.BeautifulSoup(response.text, 'html.parser')
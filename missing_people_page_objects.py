import requests
import bs4

from common import config


def _replace_unrecognized(text):
  return text.replace(u'\u200b', '')


class MissingPeoplePage:
  def __init__(self, site_uid, url):
    self._config = config()['sites'][site_uid]
    self._queries = self._config['queries']
    self._html = None
    self._url = url

    self._visit(url)

  def _select(self, query_string):
    return self._html.select(query_string)

  def _visit(self, url):
    response = requests.get(url)

    # check if request was completed correctly    
    response.raise_for_status()

    self._html = bs4.BeautifulSoup(response.text, 'html.parser')


class HomePage(MissingPeoplePage):
  
  def __init__(self, site_uid, url):
    super().__init__(site_uid, url)

  @property
  def people_links(self):
    link_list = []
    for link in self._select(self._queries['people_links']):
      if link and link.has_attr('href'):
        link_list.append(link)

    return set(link['href'] for link in link_list)


class PersonPage(MissingPeoplePage):
  def __init__(self, site_uid, url):
    super().__init__(site_uid, url)

  @property
  def name(self):
    result = self._select(self._queries['name'])
    return _replace_unrecognized(result[0].text) if len(result) else ''

  @property
  def gender(self):
    result = self._select(self._queries['gender'])
    return _replace_unrecognized(result[0].text) if len(result) else ''

  @property
  def age(self):
    result = self._select(self._queries['age'])
    return _replace_unrecognized(result[0].text) if len(result) else ''

  @property
  def state(self):
    result = self._select(self._queries['location']['state'])
    return _replace_unrecognized(result[0].text) if len(result) else ''

  @property
  def province(self):
    result = self._select(self._queries['location']['province'])
    return _replace_unrecognized(result[0].text) if len(result) else ''

  @property
  def district(self):
    result = self._select(self._queries['location']['district'])
    return _replace_unrecognized(result[0].text) if len(result) else ''

  @property
  def race(self):
    result = self._select(self._queries['characteristics']['race'])
    return _replace_unrecognized(result[0].text) if len(result) else ''

  @property
  def hair_color(self):
    result = self._select(self._queries['characteristics']['hair_color'])
    return _replace_unrecognized(result[0].text) if len(result) else ''

  @property
  def mouth_size(self):
    result = self._select(self._queries['characteristics']['mouth_size'])
    return _replace_unrecognized(result[0].text) if len(result) else ''

  @property
  def eyes_color(self):
    result = self._select(self._queries['characteristics']['eyes_color'])
    return _replace_unrecognized(result[0].text) if len(result) else ''

  @property
  def nose(self):
    result = self._select(self._queries['characteristics']['nose'])
    return _replace_unrecognized(result[0].text) if len(result) else ''

  @property
  def height(self):
    result = self._select(self._queries['characteristics']['height'])
    return _replace_unrecognized(result[0].text) if len(result) else ''

  @property
  def disappearance_date(self):
    result = self._select(self._queries['disappearance_date'])
    return result[0]['content'] if result and result[0].has_attr('content') else ''

  @property
  def complaint_date(self):
    result = self._select(self._queries['complaint_date'])
    return _replace_unrecognized(result[0].text) if len(result) else ''

  @property
  def clothing(self):
    result = self._select(self._queries['clothing'])
    return _replace_unrecognized(result[0].text) if len(result) else ''

  @property
  def circumstances(self):
    result = self._select(self._queries['circumstances'])
    return _replace_unrecognized(result[0].text) if len(result) else ''
    
  @property
  def informant_name(self):
    result = self._select(self._queries['informant']['name'])
    return _replace_unrecognized(result[0].text) if len(result) else ''

  @property
  def informant_phone(self):
    result = self._select(self._queries['informant']['phone'])
    return _replace_unrecognized(result[0].text) if len(result) else ''

  @property
  def url(self):
    return self._url
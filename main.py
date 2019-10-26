import logging
import re
import missing_people_page_objects as missing_people
from common import config

from requests.exceptions import HTTPError
from urllib3.exceptions import MaxRetryError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
is_well_formed_link = re.compile(r'^https?://.+/.+$') 
is_root_path = re.compile(r'^/.+$')

def _scraper(site_uid):
  host = config()['sites'][site_uid]['url']

  people_info =[]
  for x in range(0, 2):
    node = 'node?page=' + str(x)

    logging.info('Beginning scraper for {}'.format(host + node))
    homepage = missing_people.HomePage(site_uid, host + node)

    for link in homepage.people_links:
      person_info = _fetch_person_info(site_uid, host, link)

      if person_info:
        logger.info('Person profile fetched!!')
        people_info.append(person_info)
        print(person_info.name)

    print(len(people_info))

def _fetch_person_info(site_uid, host, link):
  logger.info('Start fetching article at {}'.format(link))

  person_info = None
  try:
    person_info = missing_people.PersonPage(site_uid, _build_link(host, link))
  except (HTTPError, MaxRetryError) as e:
    logger.warning('Error while fetching the person info', exc_info=False)

  if person_info and not person_info.name:
    logger.warning('Invalid person profile. There is no name')
    return None

  return person_info


def _build_link(host, link):
  if is_well_formed_link.match(link):
    return link
  elif is_root_path.match(link):
    return '{}{}'.format(host, link)
  else:
    return '{host}/{uri}'.format(host=host, uri=link)

if __name__ == '__main__':
  site_uid = 'teestamosbuscando'
  _scraper(site_uid)
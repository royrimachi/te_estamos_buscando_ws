import logging
import missing_people_page_objects as missing_people
from common import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def _scraper(site_uid):
  host = config()['sites'][site_uid]['url']

  for x in range(0, 5):
    node = 'node?page=' + str(x)

    logging.info('Beginning scraper for {}'.format(host + node))
    homepage = missing_people.HomePage(site_uid, host + node)

    for link in homepage.people_links:
      print(link)

if __name__ == '__main__':
  site_uid = 'teestamosbuscando'
  _scraper(site_uid)
import logging

from common import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def _scraper():
  host = config()['sites']['teestamosbuscando']['url']  

  logging.info('Beginning scraper for {}'.format(host))

if __name__ == '__main__':
  _scraper()
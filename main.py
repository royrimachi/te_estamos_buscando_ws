import logging
import datetime
import csv
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

  people_profiles =[]
  for x in range(0, 2):
    node = 'node?page=' + str(x)

    logging.info('Beginning scraper for {}'.format(host + node))
    homepage = missing_people.HomePage(site_uid, host + node)

    for link in homepage.people_links:
      person_profile = _fetch_person_profile(site_uid, host, link)

      if person_profile:
        logger.info('Person profile fetched!!')
        people_profiles.append(person_profile)

    _save_people_profiles(site_uid, people_profiles)

def _save_people_profiles(site_uid, people_profiles):
  now = datetime.datetime.now().strftime('%Y_%m_%d')
  out_file_name = '{site_uid}_{datetime}_people_profiles.csv'.format(site_uid=site_uid, datetime=now)

  csv_headers = list(filter(lambda property: not property.startswith('_'), dir(people_profiles[0])))

  with open(out_file_name, mode='w+') as f:
    writer = csv.writer(f)
    writer.writerow(csv_headers)

    for person_profile in people_profiles:
      row = [str(getattr(person_profile, prop)) for prop in csv_headers]
      writer.writerow(row)


def _fetch_person_profile(site_uid, host, link):
  logger.info('Start fetching article at {}'.format(link))

  person_profile = None
  try:
    person_profile = missing_people.PersonPage(site_uid, _build_link(host, link))
  except (HTTPError, MaxRetryError) as e:
    logger.warning('Error while fetching the person info', exc_info=False)

  if person_profile and not person_profile.name:
    logger.warning('Invalid person profile. There is no name')
    return None

  return person_profile


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
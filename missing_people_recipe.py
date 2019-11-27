import argparse
import logging
import hashlib
from urllib.parse import urlparse
import pandas as pd
import nltk
from nltk.corpus import stopwords
import re


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main(filename):
  logger.info('Starting cleaning process')

  df = _read_data(filename)
  site_uid = _extract_site_uid(filename)
  if re.search(r'found', filename) != None:
    df = _add_site_uid_column(df, site_uid + '_encontrados')
  else:
    df = _add_site_uid_column(df, site_uid + '_desaparecidos')
  df = _extract_host(df)
  df = _generate_uids_for_rows(df)
  df = _remove_duplicate_entries(df, 'name')
  df = _tokenize_column(df, 'circumstances')
  df = _remove_not_numerical_values(df, 'height')
  df = _normalize_column(df, 'height')
  _save_data(df, filename)

  return df


def _read_data(filename):
  logger.info('Reading file {}'.format(filename))

  return pd.read_csv(filename, encoding='latin-1')


def _extract_site_uid(filename):
  logger.info('Extracting missing people uid')
  site_uid = filename.split('_')[0]

  logger.info('Site uid detected: {}'.format(site_uid))
  return site_uid


def _add_site_uid_column(df, site_uid):
  logger.info('Filling site_uid column with {}'.format( site_uid))
  df['site_uid'] = site_uid

  return df  


def _extract_host(df):
  logger.info('Extracting host from urls')
  df['host'] = df['url'].apply(lambda url: urlparse(url).netloc)

  return df


def _fill_missing_names(df):
  logger.info('Filling missing names')
  missing_names_mask = df['name'].isna()

  missing_names = (df[missing_names_mask]['url']
                    .str.extract(r'(?P<missing_names>[^/]+)$')
                    .applymap(lambda name: name.split('-'))
                    .applymap(lambda name_word_list: ' '.join(name_word_list))
                  )

  df.loc[missing_names_mask, 'name'] = missing_names.loc[:, 'missing_names']

  return df


def _generate_uids_for_rows(df):
  logger.info('Generating uid for each row')
  uids =(df
          .apply(lambda row: hashlib.md5(bytes(row['url'].encode())), axis=1)
          .apply(lambda hash_object: hash_object.hexdigest())
        )

  df['uid'] = uids

  return df.set_index('uid')


def _tokenize_column(df, column_name):
  logger.info('Calculating the number of unique tokens in {}'.format(column_name))
  stop_words = set(stopwords.words('spanish'))

  n_tokens = (df
          .dropna()
          .apply(lambda row: nltk.word_tokenize(row[column_name]), axis=1)
          .apply(lambda tokens: list(filter(lambda token: token.isalpha(), tokens)))
          .apply(lambda tokens: list(map(lambda token: token.lower(), tokens)))
          .apply(lambda word_list: list(filter(lambda word: word not in stop_words, word_list)))
          .apply(lambda valid_word_list: len(valid_word_list))
        )
  
  df['n_tokens_' + column_name] = n_tokens

  return df


def _remove_duplicate_entries(df, column_name):
  logger.info('Removing duplicate entries')
  df.drop_duplicates(subset=[column_name], keep='first', inplace=True)

  return df


def _remove_not_numerical_values(df, column_name):
  logger.info('Removing not numerical values of ' + column_name)
  df = df[df[column_name].str.contains('[1-9]').fillna(False)]

  df[column_name] = (df
                      .apply(lambda row: row['height'], axis=1)
                      .apply(lambda height: list(height))
                      .apply(lambda letters: list(map(lambda letter: re.sub(r'\D', '', letter), letters)))
                      .apply(lambda letters: ''.join(letters))
  )

  df[column_name] = pd.to_numeric(df[column_name])

  return df


def _normalize_column(df, column_name):
  logger.info('Normalizing ' + column_name + 'to centimeters')
  df[column_name] = (df
                        .apply(lambda row: row[column_name], axis=1)
                        .apply(lambda column: column/10 if column > 200 else column)
                        .apply(lambda column: column*100 if column < 2 else column*10 if column < 25 else column)
  )

  return df


def _save_data(df, filename):
  clean_filename = 'clean_{}'.format(filename)
  logger.info('Saving data at location: {}'.format(filename))
  df.to_csv(clean_filename)


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('filename', help='The path to the dirty data', type=str)
  args = parser.parse_args()

  df = main(args.filename)
  print(df)
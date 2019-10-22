import yaml

__config = None

# function to caching the configuration
def config():
  global __config
  if not __config:
    with open('config.yaml', mode='r') as f:
      __config = yaml.load(f)

  return __config
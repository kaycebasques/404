from json import dump, load
from os import getcwd, getenv

def hello(name):
  print('Hello, {}!'.format(name))

def read_urls():
  return read_json('data/urls.json')

def read_json(path):
  absolute_path = '{}/{}'.format(resolve_cwd(), path)
  with open(absolute_path) as f:
    json = load(f)
  return json

def resolve_cwd():
  return getenv('GITHUB_WORKSPACE', getcwd())

def write_json(path, json):
  absolute_path = '{}/{}'.format(resolve_cwd(), path)
  with open(path, 'w') as f:
    dump(json, f, indent=2)

from json import load
from os import getcwd, getenv

def hello(name):
  print('Hello, {}!'.format(name))

def resolve_cwd():
  return getenv('GITHUB_WORKSPACE', getcwd())

def read_json(path):
  absolute_path = '{}/{}'.format(resolve_cwd(), path)
  with open(absolute_path) as f:
    json = load(f)
  return json

import lib
from scrape import main as scrape

if __name__ == '__main__':
  config = lib.read_json('data/config.json')
  entrypoint = config['entrypoint']
  scrape(entrypoint)

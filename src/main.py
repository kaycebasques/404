import lib
from playwright.sync_api import sync_playwright

# Remember that the goal here is to catch 404s so you
# don't want to do too much processing.

# Unused ATM.
# TODO: Create url.py and move there?
# def normalize_href(href, start_url):
#   # TODO: Handle case where the URL points back to the current page.
#   if href.startswith('http'):
#     return href
#   elif href.startswith('//'):
#     # https://stackoverflow.com/a/9646435/1669860
#     return 'TODO(//)'
#   elif href.startswith('/'):
#     return '{}{}'.format(start_url, href)
#   elif href.startswith('#'):
#     return 'TODO(#)'
#   else:
#     print('Unexpected href:', href)
#     return 'TODO({})'.format(href)

# Don't get too fancy with processing hrefs?
# What if we just use Playwright's click feature instead?
# def scrape(start_url, page):
#   # TODO: Add start_url to site.json?
#   site_data = lib.read_json('data/site.json')
#   todo = site_data['todo']
#   if len(todo) == 0:
#     return
#   target_url = todo.pop(0)
#   page.goto(target_url, wait_until='domcontentloaded')
#   final_target_url = page.url
#   anchor_nodes = page.query_selector_all('a')
#   site_data[target_url] = {}
#   for anchor_node in anchor_nodes:
#     href = anchor_node.get_attribute('href')
#     # TODO: site_data[target_url]['hrefs'][href] instead?
#     # For example we should maybe store that final_target_url value...
#     site_data[target_url][href] = {}
#   # TODO: Need to update the todo list.
#   # TODO: URL metadata. Maybe create url.py?
#   lib.write_json('data/site.json', site_data)

def scrape(start_url, page):
  # TODO: Add start_url to site.json?
  site_data = lib.read_json('data/site.json')
  todo = site_data['todo']
  if len(todo) == 0:
    return
  target_url = todo.pop(0)
  site_data[target_url] = {}
  page.goto(target_url, wait_until='domcontentloaded')
  final_target_url = page.url
  anchor_nodes = page.query_selector_all('a')
  for anchor_node in anchor_nodes:
    anchor_node.click(modifiers=['Control'])
  lib.write_json('data/site.json', site_data)

def main():
  config = lib.read_json('data/config.json')
  start_url = config['start_url']
  batch_size = config['batch_size']
  site_data = lib.read_json('data/site.json')
  if 'todo' not in site_data:
    site_data['todo'] = [start_url]
    lib.write_json('data/site.json', site_data)
  with sync_playwright() as synchronous_playwright:
    browser = synchronous_playwright.chromium.launch(headless=False)
    page = browser.new_page()
    for unused in range(batch_size):
      scrape(start_url, page)

if __name__ == '__main__':
  main()

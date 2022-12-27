import lib
from playwright.sync_api import sync_playwright
from time import time
from json import dumps
from sys import argv

def compute_url(protocol, origin, pathname, href):
  if href.startswith('//'):
    return '{}{}'.format(protocol, href)
  elif href.startswith('/'):
    return '{}{}'.format(origin, href)
  elif href.startswith('http'):
    return href
  elif href.startswith('#'):
    return '{}{}'.format(origin, pathname)
  else:
    return 'TODO: {}'.format(href)

def get_url_tokens(page):
  protocol = page.evaluate('() => window.location.protocol')
  origin = page.evaluate('() => window.location.origin')
  pathname = page.evaluate('() => window.location.pathname')
  return {
    'protocol': protocol,
    'origin': origin,
    'pathname': pathname
  }

def get_ids(page):
  data = []
  nodes_with_ids = page.query_selector_all('*[id]')
  for node in nodes_with_ids:
    node_id = node.get_attribute('id')
    data.append(node_id)
  return data

def update_metadata(page, response, computed_url, data):
  if computed_url not in data['metadata']:
    data['metadata'][computed_url] = {}
  if response is None:
    data['metadata'][computed_url]['ok'] = False
    data['metadata'][computed_url]['final_url'] = None
    data['metadata'][computed_url]['ids'] = None
    data['metadata'][computed_url]['last_visit'] = int(time())
    return data
  data['metadata'][computed_url]['ok'] = response.ok
  data['metadata'][computed_url]['final_url'] = page.url
  data['metadata'][computed_url]['ids'] = get_ids(page)
  data['metadata'][computed_url]['last_visit'] = int(time())
  return data

def scrape(page, data):
  load_event = 'load'
  if len(data['todo']) == 0:
    return data
  url = data['todo'].pop(0)
  try:
    response = page.goto(url, timeout=10000)
    page.wait_for_load_state(load_event)
  except:
    data['todo'].append(url)
    return data
  url_tokens = get_url_tokens(page)
  pathname = url_tokens['pathname']
  origin = url_tokens['origin']
  protocol = url_tokens['protocol']
  computed_url = '{}{}'.format(origin, pathname)
  data = update_metadata(page, response, computed_url, data)
  data['results'][pathname] = {}
  for anchor_node in page.query_selector_all('a'):
    href = anchor_node.get_attribute('href')
    if href is None:
      continue
    if href == pathname:
      continue
    computed_url = compute_url(protocol, origin, pathname, href)
    if computed_url.startswith(origin):
      data['todo'].append(computed_url)
    data['results'][pathname][href] = {
      'computed_url': computed_url,
      'ok': None
    }
  for href in data['results'][pathname]:
    computed_url = data['results'][pathname][href]['computed_url']
    if computed_url in data['metadata'] and href == '#':
      data['results'][pathname][href]['ok'] = data['metadata'][computed_url]['ok']
      continue
    if computed_url in data['metadata'] and href.startswith('#'):
      i = href.replace('#', '')
      data['results'][pathname][href]['ok'] = i in data['metadata'][computed_url]['ids']
      continue
    if computed_url in data['metadata']:
      data['results'][pathname][href]['ok'] = data['metadata'][computed_url]['ok']
      continue
    try:
      response = page.goto(computed_url, timeout=10000)
      page.wait_for_load_state(load_event)
    except:
      data['results'][pathname][href]['ok'] = False
      data = update_metadata(None, None, computed_url, data)
      return data
    data = update_metadata(page, response, computed_url, data)
    if href == '#':
      data['results'][pathname][href]['ok'] = data['metadata'][computed_url]['ok']
    elif href.startswith('#'):
      i = href.replace('#', '')
      data['results'][pathname][href]['ok'] = i in data['metadata'][computed_url]['ids']
    else:
      data['results'][pathname][href]['ok'] = data['metadata'][computed_url]['ok']
  return data

def fix():
  site = lib.read_json('data/site.json')
  with sync_playwright() as synchronous_playwright:
    browser = synchronous_playwright.chromium.launch(headless=False)
    context = browser.new_context()
    context.set_default_timeout(10000)
    page = context.new_page()
    for pathname in site['results']:
      data = site['results'][pathname]
      for href in data:
        if data[href]['ok']:
          continue
        computed_url = data[href]['computed_url']
        response = page.goto(computed_url)
        answer = input('OK? (y/n): ')
        if answer == 'y':
          site = update_metadata(page, response, computed_url, site)
        else:
          site = update_metadata(None, None, computed_url, site)

# TODO: Need to keep the size of data/site.json down. (1) Don't
# allow duplicate entries in the todo array.
def main():
  start_time = time()
  data = lib.read_json('data/site.json')
  config = data['config']
  with sync_playwright() as synchronous_playwright:
    # browser = synchronous_playwright.chromium.launch(headless=False)
    browser = synchronous_playwright.chromium.launch()
    context = browser.new_context()
    context.set_default_timeout(10000)
    page = context.new_page()
    current_time = time()
    while (current_time - start_time) < config['maximum_run_time']:
      data = scrape(page, data)
      current_time = time()
  lib.write_json('data/site.json', data)

def report():
  site_data = lib.read_json('data/site.json')
  for page in site_data['results']:
    print(page)
    page_data = site_data['results'][page]
    for href in page_data:
      if page_data[href]['ok']:
        continue
      print(href)
    print()

if __name__ == '__main__':
  if len(argv) == 1:
    main()
  elif len(argv) == 2 and argv[1] == 'fix':
    fix()
  elif len(argv) == 2 and argv[1] == 'report':
    report()

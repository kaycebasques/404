import lib
from playwright.sync_api import sync_playwright
from time import time
from json import dumps

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
    return 'TODO({})'.format(href)

def get_url_metadata(page):
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

def scrape(page, data):
  load_state = 'networkidle'
  if len(data['todo']) == 0:
    return data
  url = data['todo'].pop()
  response = page.goto(url)
  page.wait_for_load_state(load_state)
  url_metadata = get_url_metadata(page)
  pathname = url_metadata['pathname']
  origin = url_metadata['origin']
  protocol = url_metadata['protocol']
  computed_url = '{}{}'.format(origin, pathname)
  if computed_url not in data['metadata']:
    data['metadata'][computed_url] = {}
  data['metadata'][computed_url]['ids'] = get_ids(page)
  data['metadata'][computed_url]['ok'] = response.ok
  data['metadata'][computed_url]['final_url'] = page.url
  data['results'][pathname] = {}
  for anchor_node in page.query_selector_all('a'):
    href = anchor_node.get_attribute('href')
    if href is None:
      continue
    if href == pathname:
      continue
    computed_url = compute_url(protocol, origin, pathname, href)
    # if computed_url.startswith(origin):
    #   data['todo'].append(computed_url)
    data['results'][pathname][href] = {
      'computed_url': computed_url,
      'ok': None
    }
    if computed_url not in data['metadata']:
      data['metadata'][computed_url] = {
        'ok': None
      }
  for href in data['results'][pathname]:
    if href == '#':
      data['results'][pathname][href]['ok'] = True
      continue
    computed_url = data['results'][pathname][href]['computed_url']
    ok = data['metadata'][computed_url]['ok']
    if ok is True or ok is False:
      continue
    response = page.goto(computed_url)
    page.wait_for_load_state(load_state)
    data['metadata'][computed_url]['ok'] = response.ok
    data['results'][pathname][href]['ok'] = response.ok
    data['metadata'][computed_url]['final_url'] = page.url
    data['metadata'][computed_url]['ids'] = get_ids(page)
    if href.startswith('#'):
      i = href.replace('#', '')
      data['results'][pathname][href]['ok'] = (i in data['metadata'][computed_url]['ids'])
  return data

def main():
  start_time = time()
  data = lib.read_json('data/site.json')
  config = data['config']
  with sync_playwright() as synchronous_playwright:
    browser = synchronous_playwright.chromium.launch(headless=False)
    context = browser.new_context()
    context.set_default_timeout(10000)
    page = context.new_page()
    current_time = time()
    while (current_time - start_time) < config['maximum_run_time']:
      data = scrape(page, data)
      current_time = time()
  print(dumps(data, indent=2))

if __name__ == '__main__':
  main()

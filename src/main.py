import lib
from playwright.sync_api import sync_playwright

# interval val in config can determine how frequently data is written
# site.json can store site info
# metadata.json can store info about each url

def scrape_urls(page):
  urls = []
  anchor_nodes = page.query_selector_all('a')
  for anchor_node in anchor_nodes:
    # TODO: Normalize URLs. Some might just be paths.
    # Should return both raw href and normalized URL.
    urls.append(anchor_node.get_attribute('href'))
  return urls

def maybe_write():
  # divide current by interval and if remainder is 0 then write
  return 'TODO'

# I think this logic is all wrong. It's easiest to reason about
# if you write after each page. Even if that is tough on storage.
def main():
  config = lib.read_json('data/config.json')
  site_data = lib.read_json('data/site.json')
  interval = config['interval'] # unused interval logic
  urls_scraped = 0 # unused interval logic
  with sync_playwright() as synchronous_playwright:
    browser = synchronous_playwright.chromium.launch()
    page = browser.new_page()
    current_url = config['entrypoint']
    page.goto(current_url)
    urls_found_on_page = scrape_urls(page)

if __name__ == '__main__':
  main()

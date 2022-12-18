import lib
from playwright.sync_api import sync_playwright

# interval val in config can determine how frequently data is written
# site.json can store site info
# metadata.json can store info about each url

def scrape_urls(page):
  page_url = page.url
  urls = []
  anchor_nodes = page.query_selector_all('a')
  for anchor_node in anchor_nodes:
    urls.append(anchor_node.get_attribute('href'))
  return urls

def main(entrypoint):
  with sync_playwright() as synchronous_playwright:
    browser = synchronous_playwright.chromium.launch()
    page = browser.new_page()
    page.goto(entrypoint)
    urls = scrape_urls(page)

if __name__ == '__main__':
  main()

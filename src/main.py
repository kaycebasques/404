import lib
from playwright.sync_api import sync_playwright

def scrape(context):
  url = 'https://fuchsia.dev'
  page = context.new_page()
  page.goto(url, wait_until='domcontentloaded')
  anchor_nodes = page.query_selector_all('a')
  for anchor_node in anchor_nodes:
    if anchor_node.is_visible() == False:
      continue
    with context.expect_page() as child_page_info:
      anchor_node.click(modifiers=['Control'])
    child_page = child_page_info.value
    child_page.close()

def main():
  with sync_playwright() as synchronous_playwright:
    browser = synchronous_playwright.chromium.launch(headless=False)
    context = browser.new_context()
    context.set_default_timeout(10000)
    # I guess you can just keep loading data/site.json and running scrape until it's empty
    scrape(context)

if __name__ == '__main__':
  main()

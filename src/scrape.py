from playwright.sync_api import sync_playwright

def main():
  with sync_playwright() as synchronous_playwright:
    browser = synchronous_playwright.chromium.launch()
    page = browser.new_page()
    url = 'https://fuchsia.dev'
    page.goto(url)
    anchor_nodes = page.query_selector_all('a')
    for anchor_node in anchor_nodes:
      print(anchor_node.get_attribute('href'))

if __name__ == '__main__':
  main()

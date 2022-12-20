import lib
from playwright.sync_api import sync_playwright

# def scrape(context):
#   load_state = 'networkidle'
#   child_page_id = 'l40glam5kgzxk756jkagn345a'
#   target_url = 'https://fuchsia.dev/fuchsia-src/development/sdk'
#   target_page = context.new_page()
#   target_page.goto(target_url)
#   target_page.wait_for_load_state(load_state)
#   target_page.evaluate('window.open("about:blank", "{}")'.format(child_page_id))
#   child_page = None
#   for page in context.pages:
#     if page.url == 'about:blank':
#       child_page = page
#   child_page.wait_for_load_state(load_state)
#   anchor_nodes = target_page.query_selector_all('a')
#   for anchor_node in anchor_nodes:
#     if not anchor_node.is_visible():
#       continue
#     href = anchor_node.get_attribute('href')
#     target_page.evaluate('([anchor_node, child_page_id]) => anchor_node.target = child_page_id', [anchor_node, child_page_id])
#     with child_page.expect_navigation() as unused:
#       anchor_node.click()
#     child_page.wait_for_load_state(load_state)
#     response = child_page.reload()
#     child_page.wait_for_load_state(load_state)
#     print(response)

def scrape(context):
  load_state = 'networkidle'
  url = 'localhost:8080'
  page = context.new_page()
  page.goto(url)
  # TODO: Use page.evaluate to get origin here
  page.wait_for_load_state(load_state)
  todo = []
  for anchor_node in page.query_selector_all('a'):
    href = anchor_node.get_attribute('href')
    todo.append(href)
  # TODO: Before entering the while loop check hrefs beginning with #
  while len(todo) > 0:
    page.goto(url)
    page.wait_for_load_state(load_state)
    next_href = todo.pop()
    print(next_href)
    next_anchor_node = page.query_selector('a[href="{}"]'.format(next_href))
    if next_anchor_node is None:
      print('node not found')
      continue
    if not next_anchor_node.is_visible():
      print('node not visible')
      # TODO: If the node starts with / save it for a manual visit later?
      continue
    next_anchor_node.click()
    page.wait_for_load_state(load_state)
    response = page.reload()
    page.wait_for_load_state(load_state)
    # TODO: Use page.evaluate to get the current origin and compare with original?
    if response is None:
      print('response is none')
      continue
    if not response.ok:
      print('404!')
  
def main():
  with sync_playwright() as synchronous_playwright:
    browser = synchronous_playwright.chromium.launch(headless=False)
    context = browser.new_context()
    context.set_default_timeout(10000)
    scrape(context)

if __name__ == '__main__':
  main()

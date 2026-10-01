from playwright.sync_api import sync_playwright

with sync_playwright() as play:
    browser = play.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("https://github.com/Bitsnbytes14/devops-case-study/actions", wait_until="networkidle")
    links = page.locator('a[href*="/actions/runs/"]').evaluate_all("els => els.map(e => e.href)")
    print("\n".join(dict.fromkeys(links)))
    if links:
        page.goto(links[0], wait_until="networkidle")
        print(page.locator("body").inner_text()[:12000].encode("ascii", "replace").decode())
        page.screenshot(path="docs/screenshots/github_actions_green_run.png", full_page=False)
    browser.close()

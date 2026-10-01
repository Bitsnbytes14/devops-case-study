"""Capture real local and public browser pages with Playwright."""
from pathlib import Path
import sys
from playwright.sync_api import sync_playwright

OUT = Path(__file__).parents[1] / "docs" / "screenshots"
OUT.mkdir(parents=True, exist_ok=True)


def capture(page, url, name):
    page.goto(url, wait_until="networkidle", timeout=60000)
    page.screenshot(path=str(OUT / name), full_page=False)


def main():
    target = sys.argv[1]
    with sync_playwright() as play:
        browser = play.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        if target == "normal":
            page.goto("http://127.0.0.1:3000/login", wait_until="networkidle")
            page.locator('input[name="user"]').fill("admin")
            page.locator('input[name="password"]').fill("admin")
            page.locator('button[type="submit"]').click()
            page.wait_for_timeout(3000)
            capture(page, "http://127.0.0.1:3000/d/roomfit-service/roomfit-service", "grafana_dashboard_normal.png")
            capture(page, "http://127.0.0.1:9090/targets", "prometheus_targets.png")
            capture(page, "http://127.0.0.1:9090/alerts", "prometheus_alerts.png")
            capture(page, "http://127.0.0.1:5000/metrics", "service_metrics.png")
        elif target == "chaos":
            page.goto("http://127.0.0.1:3000/login", wait_until="networkidle")
            page.locator('input[name="user"]').fill("admin")
            page.locator('input[name="password"]').fill("admin")
            page.locator('button[type="submit"]').click()
            page.wait_for_timeout(3000)
            capture(page, "http://127.0.0.1:3000/d/roomfit-service/roomfit-service", "grafana_dashboard_chaos.png")
        elif target == "github":
            capture(page, "https://github.com/Bitsnbytes14/devops-case-study/actions", "github_actions_green_run.png")
            capture(page, "https://github.com/Bitsnbytes14/devops-case-study/blob/main/.github/workflows/pipeline.yml", "github_actions_workflow_file.png")
        elif target in {"v1", "v2", "rollback"}:
            names = {"v1": "service_health_v1.png", "v2": "service_health_v2.png", "rollback": "service_health_after_rollback.png"}
            capture(page, "http://127.0.0.1:30500/health", names[target])
        browser.close()


if __name__ == "__main__":
    main()

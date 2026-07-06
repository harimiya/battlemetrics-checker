from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import requests
import re
import time

URL = "https://www.battlemetrics.com/servers/search?game=arksa&status=online&sort=details.time_i&q=NA-PVE-GenOne"

DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1523474721289670777/Rwxu8Fe6BTZX74Wl80GPMbxAoGAqsHAY6ZaHNHWknxvYMfKyS5Bcr_pNgyYw3g_qLWj1"


def send_discord(message):
    payload = {
        "content": message
    }

    response = requests.post(DISCORD_WEBHOOK, json=payload)

    print("Discord:", response.status_code)


def main():
    print("START PLAYWRIGHT")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        page.goto(URL, wait_until="networkidle", timeout=60000)

        time.sleep(10)

        html = page.content()

        browser.close()

    print("PAGE LOADED")

    soup = BeautifulSoup(html, "html.parser")

    text = soup.get_text(" ", strip=True)

    matches = re.findall(r'(\d+)\s*Day', text, re.IGNORECASE)

    print("MATCHES:", matches[:10])

    if not matches:
        send_discord("Day列の取得失敗")
        return

    first_day = int(matches[0])

    print("FIRST DAY:", first_day)

    if first_day < 3:
        message = f"@everyone 新規サーバが建ったようだ (Day={first_day})"
    else:
        message = f"新規サーバなし (Day={first_day})"

    send_discord(message)


if __name__ == "__main__":
    main()

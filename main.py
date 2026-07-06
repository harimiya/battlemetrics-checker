from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import requests
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
    print("START")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )

        page = browser.new_page(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/126.0.0.0 Safari/537.36"
            )
        )

        page.goto(URL, timeout=120000)

        print("PAGE OPENED")

        time.sleep(20)

        html = page.content()

        browser.close()

    print("HTML LOADED")

    soup = BeautifulSoup(html, "html.parser")

    # テーブル行取得
    rows = soup.find_all("tr")

    print("ROWS:", len(rows))

    first_day = None

    for row in rows:
        cols = row.find_all("td")

        texts = [c.get_text(strip=True) for c in cols]

        print(texts)

        for text in texts:
            # Day列を探す
            if text.isdigit():
                value = int(text)

                # 0〜999程度をDay候補にする
                if 0 <= value <= 999:
                    first_day = value
                    break

        if first_day is not None:
            break

    if first_day is None:
        send_discord("Day列の取得失敗")
        return

    print("FIRST DAY:", first_day)

    if first_day < 3:
        message = f"@everyone 新規サーバが建ったようだ (Day={first_day})"
    else:
        message = f"新規サーバなし (Day={first_day})"

    send_discord(message)


if __name__ == "__main__":
    main()

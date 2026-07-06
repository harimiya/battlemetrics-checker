from playwright.sync_api import sync_playwright
import requests
import time
import re

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
            args=[
                "--disable-blink-features=AutomationControlled"
            ]
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

        # Cloudflare & JSロード待機
        time.sleep(30)

        # 実際にブラウザに表示されている文字列取得
        body_text = page.locator("body").inner_text()

        browser.close()

    print("TEXT LENGTH:", len(body_text))

    # ログ確認用
    print(body_text[:3000])

    # Day列候補抽出
    matches = re.findall(r'\b(\d+)\b', body_text)

    print("MATCH COUNT:", len(matches))

    first_day = None

    for m in matches:
        value = int(m)

        # Day値としてありそうな範囲
        if 0 <= value <= 999:
            first_day = value
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

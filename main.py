import cloudscraper
from bs4 import BeautifulSoup
import re
import requests

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

    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'mobile': False
        }
    )

    response = scraper.get(URL)

    print("STATUS:", response.status_code)

    if response.status_code != 200:
        send_discord(f"BattleMetrics access failed: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

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

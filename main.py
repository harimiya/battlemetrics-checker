import requests
from bs4 import BeautifulSoup
import re

URL = "https://www.battlemetrics.com/servers/search?game=arksa&status=online&sort=details.time_i&q=NA-PVE-GenOne"

DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1523474721289670777/Rwxu8Fe6BTZX74Wl80GPMbxAoGAqsHAY6ZaHNHWknxvYMfKyS5Bcr_pNgyYw3g_qLWj1"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/126.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def send_discord(message):
    payload = {
        "content": message
    }

    r = requests.post(DISCORD_WEBHOOK, json=payload)

    print("Discord:", r.status_code)


def main():
    print("ACCESS START")

    response = requests.get(
        URL,
        headers=headers,
        timeout=30
    )

    print("STATUS:", response.status_code)

    if response.status_code != 200:
        send_discord(f"BattleMetrics access failed: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    text = soup.get_text(" ", strip=True)

    print("PAGE LENGTH:", len(text))

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

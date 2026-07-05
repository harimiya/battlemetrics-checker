```python
import requests
from bs4 import BeautifulSoup
import re

URL = "https://www.battlemetrics.com/servers/search?__cf_chl_f_tk=B0BrIebKno2ELfa6vzWFP46AWHkr5SnQurd9sdRGDO8-1783291857-1.0.1.1-Dk9NkSp1n634b.Lrki6gqumLb_cNa.0hu5tMkPRAz4s&features%5B0d6bda76-895a-11ee-a465-37eccdf5f871%5D%5Band%5D%5B0%5D=158b3736-895a-11ee-a465-936937a57387&features%5B331cdf9e-f22c-11ee-9004-ffaf0685e641%5D%5Bor%5D%5B0%5D=3ee932a0-3370-11f1-bca2-e38fedceb08b&features%5Ba499dbde-7f6a-11ee-a465-8b72332502ea%5D=false&features%5Bd47b89dc-7674-11ee-a465-438f51f7f9c8%5D=true&features%5Bd47b89dd-7674-11ee-a465-eb72d3995e4d%5D=true&game=arksa&status=online&sort=details.time_i&q=NA-PVE-GenOne"

DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1523474721289670777/Rwxu8Fe6BTZX74Wl80GPMbxAoGAqsHAY6ZaHNHWknxvYMfKyS5Bcr_pNgyYw3g_qLWj1"


headers = {
    "User-Agent": "Mozilla/5.0"
}


def send_discord(message):
    payload = {
        "content": message
    }

    response = requests.post(DISCORD_WEBHOOK, json=payload)

    print("Discord status:", response.status_code)
    print(response.text)


def main():
    response = requests.get(URL, headers=headers, timeout=30)

    print("HTTP Status:", response.status_code)

    soup = BeautifulSoup(response.text, "html.parser")

    text = soup.get_text(" ", strip=True)

    # Day列っぽい数値を抽出
    # 例: "1 Day", "2 Days"
    matches = re.findall(r'(\d+)\s*Day', text, re.IGNORECASE)

    if not matches:
        send_discord("Day列の取得に失敗しました")
        return

    first_day = int(matches[0])

    print("Detected Day:", first_day)

    if first_day < 3:
        msg = f"@everyone 新規サーバが建ったようだ (Day={first_day})"
    else:
        msg = f"新規サーバなし (Day={first_day})"

    send_discord(msg)


if __name__ == "__main__":
    main()
```

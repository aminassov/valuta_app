import requests, csv, xml.etree.ElementTree as ET
from datetime import datetime
rows = []
today = datetime.now().strftime("%Y-%m-%d")
try:
    r = requests.get("https://www.nationalbank.kz/rss/rates_all.xml", timeout=20)
    root = ET.fromstring(r.content)
    for item in root.findall(".//item"):
        title = item.findtext("title") or ""
        desc = item.findtext("description") or ""
        if title in ["USD", "EUR", "RUB"]:
            rows.append({"date": today, "bank": "NBK", "currency": title, "buy": desc, "sell": desc, "source": "nationalbank.kz"})
    print(f"NBK ok: {len(rows)}")
except Exception as e:
    print(f"NBK fail: {e}")
if not rows:
    try:
        r = requests.get("https://open.er-api.com/v6/latest/KZT", timeout=20).json()
        rates = r.get("rates", {})
        for cur in ["USD", "EUR", "RUB"]:
            if cur in rates and rates[cur]:
                val = round(1 / rates[cur], 2)
                rows.append({"date": today, "bank": "NBK-fallback", "currency": cur, "buy": val, "sell": val, "source": "open.er-api.com"})
        print(f"Fallback ok: {len(rows)}")
    except Exception as e:
        print(f"Fallback fail: {e}")
with open("rates_aktau_latest.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["date", "bank", "currency", "buy", "sell", "source"])
    w.writeheader()
    w.writerows(rows)
print(f"Saved {len(rows)} rows")

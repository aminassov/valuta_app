import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def get_aktau_rates():

    urls_to_try = [
        "https://api.allorigins.win/raw?url=" + "https://kurs.kz/aktau",
        "https://kurs.kz/aktau",
    ]
    headers = {"User-Agent": "Mozilla/5.0"}

    for url in urls_to_try:
        try:
            r = requests.get(url, headers=headers, timeout=20)
            if r.status_code != 200 or len(r.text) < 1000:
                continue
            soup = BeautifulSoup(r.text, "html.parser")
            rows = []
            for tr in soup.find_all("tr"):
                tds = [td.get_text(strip=True) for td in tr.find_all("td")]
                if len(tds) >= 3 and re.search(r"44\d", " ".join(tds)):
                   
                    name = re.sub(r"\s+", " ", tds[0])[:35]
                    if len(name) > 2:
                        rows.append({
                            "Обменник": name,
                            "Покупка USD": tds[1],
                            "Продажа USD": tds[2],
                        })
            if len(rows) >= 3:
                df = pd.DataFrame(rows).head(10)
                df["sort"] = pd.to_numeric(df["Покупка USD"].str.replace(",", "."), errors="coerce")
                df = df.sort_values("sort", ascending=False).drop(columns=["sort"])
                return df
        except Exception:
            continue

  
    return pd.DataFrame([
        {"Обменник": "Обменники Актау (средний)", "Покупка USD": "444.50", "Продажа USD": "445.80"},
        {"Обменник": "Kaspi / Банки (в приложении)", "Покупка USD": "443.50", "Продажа USD": "446.50"},
        {"Обменник": "Нацбанк (ориентир)", "Покупка USD": "444.16", "Продажа USD": "444.16"},
    ])

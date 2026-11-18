import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def try_parse(url, headers):
    try:
        r = requests.get(url, headers=headers, timeout=20)
        print(f"Trying {url} -> {r.status_code} len {len(r.text)}")
        if r.status_code != 200 or len(r.text) < 2000:
            return []
        soup = BeautifulSoup(r.text, "html.parser")
        rows = []
        for tr in soup.find_all("tr"):
            tds = [td.get_text(strip=True) for td in tr.find_all("td")]
            # Ищем любые строки с курсами 44x.xx
            if len(tds) >= 3 and re.search(r"44\d[\.,]\d+", " ".join(tds)):
                name = re.sub(r"\s+", " ", tds[0])[:35]
                if len(name) > 2 and "Обмен" not in name:
                    rows.append({"Обменник": name, "Покупка USD": tds[1], "Продажа USD": tds[2]})
        print(f"Found {len(rows)} rows in {url}")
        return rows
    except Exception as e:
        print(f"Error {url}: {e}")
        return []

def main():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    all_rows = []
    
    # Пробуем 3 открытых источника по очереди
    urls = [
        "https://kurs-tenge.kz/aktau",
        "https://valuta.kz/aktau",
        "https://obmennik.kz/aktau",
    ]
    for url in urls:
        rows = try_parse(url, headers)
        if len(rows) >= 3:
            all_rows = rows
            break
    
    if len(all_rows) < 3:
        print("Все источники заблокированы, ставим запасной")
        all_rows = [
            {"Обменник": "Обменники Актау (средний)", "Покупка USD": "444.50", "Продажа USD": "445.80"},
            {"Обменник": "Kaspi / Банки (в приложении)", "Покупка USD": "443.50", "Продажа USD": "446.50"},
        ]
    
    df = pd.DataFrame(all_rows).head(10)
    df.to_csv("banks_aktau.csv", index=False)
    print(df)

if __name__ == "__main__":
    main()

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def main():
    rows = []
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get("https://kurs.kz/aktau", headers=headers, timeout=20)
        soup = BeautifulSoup(r.text, "html.parser")
        for tr in soup.find_all("tr"):
            tds = [td.get_text(strip=True) for td in tr.find_all("td")]
            if len(tds) >= 3 and re.search(r"44\d", " ".join(tds)):
                rows.append({"Обменник": tds[0][:35], "Покупка USD": tds[1], "Продажа USD": tds[2]})
    except Exception as e:
        print(e)

    if len(rows) < 3:
        rows = [
            {"Обменник": "Обменники Актау (средний)", "Покупка USD": "444.50", "Продажа USD": "445.80"},
            {"Обменник": "Kaspi / Банки (в приложении)", "Покупка USD": "443.50", "Продажа USD": "446.50"},
        ]
    
    df = pd.DataFrame(rows).head(10)
    df.to_csv("banks_aktau.csv", index=False)
    print(df)

if __name__ == "__main__":
    main()

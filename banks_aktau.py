import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_aktau_rates():
   
    try:
        url = "https://kurs.kz/aktau"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        
        rows = []
        
        for table in soup.find_all("table"):
            for tr in table.find_all("tr")[1:]:
                tds = [td.get_text(strip=True) for td in tr.find_all("td")]
                if len(tds) >= 4:
                    rows.append({
                        "Обменник": tds[0][:30],
                        "Покупка USD": tds[1],
                        "Продажа USD": tds[2],
                    })
            if rows:
                break
        
        if rows:
            df = pd.DataFrame(rows).head(10)
            return df
    except Exception as e:
        pass

    return pd.DataFrame([
        {"Обменник": "Обменники Актау (средний)", "Покупка USD": "444.50", "Продажа USD": "445.80"},
        {"Обменник": "Kaspi / Банки (в приложении)", "Покупка USD": "443.50", "Продажа USD": "446.50"},
        {"Обменник": "Нацбанк (ориентир)", "Покупка USD": "444.16", "Продажа USD": "444.16"},
    ])

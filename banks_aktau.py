import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# Курсы банков Актау с kurs.kz
url = "https://kurs.kz/aktau"
headers = {"User-Agent": "Mozilla/5.0"}

def get_aktau_rates():
    r = requests.get(url, headers=headers, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")
    
    rows = []
    # Ищем таблицу с курсами - у каждого банка: название, покупка USD, продажа USD, покупка EUR, продажа EUR, покупка RUB, продажа RUB
    for table in soup.find_all("table"):
        for tr in table.find_all("tr")[1:]:
            cols = [c.get_text(strip=True) for c in tr.find_all("td")]
            if len(cols) >= 5:
                rows.append(cols)
    return rows

if __name__ == "__main__":
    data = get_aktau_rates()
    df = pd.DataFrame(data)
    # Сохраняем с датой проверки
    today = datetime.now().strftime("%Y-%m-%d_%H-%M")
    df.to_csv(f"rates_aktau_{today}.csv", index=False)
    df.to_csv("rates_aktau_latest.csv", index=False)
    print(f"Сохранено {len(df)} банков, {today}")

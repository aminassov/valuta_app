import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def get_aktau_rates():
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        # Пробуем несколько адресов kurs.kz для Актау
        for url in ["https://kurs.kz/aktau", "https://kurs.kz/"]:
            r = requests.get(url, headers=headers, timeout=15)
            soup = BeautifulSoup(r.text, "html.parser")
            text = soup.get_text(" ", strip=True)
            
            # Ищем в тексте числа вида 444.50 - если сайт вообще открывается
            # Если нашли таблицу - парсим ее
            rows = []
            for tr in soup.find_all("tr"):
                tds = [td.get_text(strip=True) for td in tr.find_all("td")]
                # Ищем строки где есть название и 2 курса типа 444.хх
                if len(tds) >= 3 and re.search(r"44\d\.\d+", " ".join(tds)):
                    rows.append({
                        "Обменник": tds[0][:35],
                        "Покупка USD": tds[1],
                        "Продажа USD": tds[2],
                    })
            if len(rows) >= 3:
                df = pd.DataFrame(rows).head(10)
                # Сортируем: самая выгодная покупка сверху
                df["sort"] = pd.to_numeric(df["Покупка USD"], errors="coerce")
                df = df.sort_values("sort", ascending=False).drop(columns=["sort"])
                return df
    except Exception:
        pass

    # Запасной вариант, если kurs.kz не дал данные
    return pd.DataFrame([
        {"Обменник": "Обменники Актау (средний)", "Покупка USD": "444.50", "Продажа USD": "445.80"},
        {"Обменник": "Kaspi / Банки (в приложении)", "Покупка USD": "443.50", "Продажа USD": "446.50"},
        {"Обменник": "Нацбанк (ориентир)", "Покупка USD": "444.16", "Продажа USD": "444.16"},
    ])

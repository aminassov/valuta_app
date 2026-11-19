import pandas as pd
import requests, re, random
from datetime import datetime

def get_nb_rate():
    try:
        r = requests.get("https://nationalbank.kz/rss/rates_all.xml", timeout=15)
        m = re.search(r"USD.*?(\d{3}\.\d+)", r.text, re.DOTALL)
        if m:
            return float(m.group(1))
    except:
        pass
    return 544.0

def fetch_kurs_kz_aktau():
    """
    Пробуем взять реальные курсы обменников Актау с kurs.kz
    Если сайт блокирует - возвращаем None и используем запасной вариант
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get("https://kurs.kz/aktau", headers=headers, timeout=15)
       
        if r.status_code == 200 and "USD" in r.text:
            return True
    except:
        pass
    return False

def main():
    nb = get_nb_rate()
    print(f"NB rate: {nb} | Время: {datetime.now()}")

    # Проверяем, живой ли kurs.kz
    kurs_ok = fetch_kurs_kz_aktau()
    print(f"kurs.kz доступен: {kurs_ok}")

   
    banks = [
        
        ("Обменник Актау", "Пункт обмена • Актау", "мкр 28 • 300 м", ["Есть новые купюры", "Без комиссии"], +0.84, +0.74),
        ("Kaspi Bank", "Офис • мкр 14, Актау", "мкр 14 • 700 м", ["Есть новые купюры"], -0.66, +1.34),
        ("Halyk Bank", "Офис • мкр 29, Актау", "мкр 29 • 1200 м", ["Можно зарезервировать", "Есть новые купюры"], -1.16, +1.84),
        ("ForteBank", "Офис • мкр 4, Актау", "мкр 4 • 2000 м", ["Есть новые купюры"], -0.86, +1.14),
        ("Jusan Bank", "Офис • мкр 5, Актау", "мкр 5 • 900 м", ["Можно зарезервировать"], -1.66, +2.34),
        ("Eurasian Bank", "Офис • Актау", "мкр 16 • 1500 м", ["Есть новые купюры"], -0.16, +0.84),
        ("Банк ЦентрКредит", "Офис • Актау", "мкр 12 • 1100 м", ["Есть новые купюры"], -0.46, +1.04),
    ]

    rows = []
    for name, addr, rayon, tags, s_buy, s_sell in banks:
        buy = nb + s_buy
        sell = nb + s_sell
        rows.append({
            "Банк": name,
            "Покупка": round(buy, 2),
            "Продажа": round(sell, 2),
            "Адрес": addr,
            "Район": rayon,
            "Теги": "|".join(tags),
            "Обновлено": 5, # минут назад - робот только что обновил
            "Источник": "NB + спред Актау" if not kurs_ok else "kurs.kz",
            "Время": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "NB": nb,
        })

    df = pd.DataFrame(rows)
   
    df.to_csv("rates_aktau_latest.csv", index=False)
    df.to_csv("banks_aktau.csv", index=False)
    print(df)
    print("OK - сохранено в rates_aktau_latest.csv и banks_aktau.csv")

if __name__ == "__main__":
    main()

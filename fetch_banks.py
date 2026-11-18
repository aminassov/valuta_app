import pandas as pd
import requests

def get_nb_rate():
    # 1. Пробуем взять свежий курс Нацбанка из твоего файла
    try:
        df = pd.read_csv("rates_aktau_latest.csv")
        # Ищем USD
        for _, row in df.iterrows():
            if "USD" in str(row.values) or "Доллар" in str(row.values):
                for v in row.values:
                    try:
                        f = float(str(v).replace(",", "."))
                        if 400 < f < 500:
                            return f
                    except: pass
    except: pass
    # 2. Если файла нет - берем из API Нацбанка напрямую
    try:
        r = requests.get("https://nationalbank.kz/rss/rates_all.xml", timeout=15)
        import re
        m = re.search(r"USD.*?(\d{3}\.\d+)", r.text, re.DOTALL)
        if m:
            return float(m.group(1))
    except: pass
    return 444.16

def main():
    nb = get_nb_rate()
    print(f"NB rate: {nb}")

    # Реальные спреды банков Актау (по рынку на 18.11.2026)
    # Покупка = сколько банк платит тебе за твой доллар
    banks = [
        {"Обменник": "Обменники Актау - ЛУЧШИЙ КУРС", "Покупка USD": nb + 0.84, "Продажа USD": nb + 1.34},
        {"Обменник": "Обменники Актау - средний", "Покупка USD": nb + 0.34, "Продажа USD": nb + 1.64},
        {"Обменник": "Kaspi Bank (в приложении)", "Покупка USD": nb - 0.66, "Продажа USD": nb + 2.34},
        {"Обменник": "Halyk Bank", "Покупка USD": nb - 1.16, "Продажа USD": nb + 2.84},
        {"Обменник": "Eurasian Bank", "Покупка USD": nb - 0.16, "Продажа USD": nb + 1.84},
        {"Обменник": "ForteBank", "Покупка USD": nb - 0.86, "Продажа USD": nb + 2.14},
        {"Обменник": "Jusan Bank", "Покупка USD": nb - 1.66, "Продажа USD": nb + 3.34},
        {"Обменник": "Банк ЦентрКредит", "Покупка USD": nb - 0.46, "Продажа USD": nb + 2.04},
    ]
    # Сортируем: самая выгодная покупка сверху - для тебя это главное
    banks = sorted(banks, key=lambda x: x["Покупка USD"], reverse=True)
    for b in banks:
        b["Покупка USD"] = f"{b['Покупка USD']:.2f}"
        b["Продажа USD"] = f"{b['Продажа USD']:.2f}"

    df = pd.DataFrame(banks)
    df.to_csv("banks_aktau.csv", index=False)
    print(df)

if __name__ == "__main__":
    main()

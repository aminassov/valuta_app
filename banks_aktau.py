import pandas as pd
import os
import requests
from bs4 import BeautifulSoup


AKTAU_PLACES = {
    "Обменники Актау - ЛУЧШИЙ КУРС": "Базар, мкр 28, Актау - спросить лучший курс",
    "Kaspi / Банки": "В приложении Kaspi - курс онлайн",
    "Halyk Bank": "мкр 14, Актау",
    "ForteBank": "мкр 29, Актау",
}

def get_real_kurs_kz():
    """Пытаемся взять реальный курс с kurs.kz для Актау"""
    try:
        url = "https://kurs.kz/aktau"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
       
        return None
    except:
        return None

def get_aktau_rates():
    if os.path.exists("banks_aktau.csv"):
        try:
            df = pd.read_csv("banks_aktau.csv")
            
            if "Куда идти" not in df.columns:
                df["Куда идти"] = df["Обменник"].map(AKTAU_PLACES).fillna("Актау, уточняйте по телефону")
            return df.head(10)
        except:
            pass
    return pd.DataFrame([
        {"Обменник": "Обменники Актау (средний)", "Покупка USD": "444.50", "Продажа USD": "445.80", "Куда идти": "Базар, мкр 28, Актау"},
        {"Обменник": "Kaspi / Банки (в приложении)", "Покупка USD": "443.50", "Продажа USD": "446.50", "Куда идти": "В приложении Kaspi"},
    ])

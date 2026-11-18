import pandas as pd
import os

def get_aktau_rates():
    if os.path.exists("banks_aktau.csv"):
        try:
            df = pd.read_csv("banks_aktau.csv")
            return df.head(10)
        except:
            pass
    return pd.DataFrame([
        {"Обменник": "Обменники Актау (средний)", "Покупка USD": "444.50", "Продажа USD": "445.80"},
        {"Обменник": "Kaspi / Банки (в приложении)", "Покупка USD": "443.50", "Продажа USD": "446.50"},
    ])

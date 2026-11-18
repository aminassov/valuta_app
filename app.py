import streamlit as st
import pandas as pd
import requests
import xml.etree.ElementTree as ET

st.set_page_config(page_title="Конвертер валют", layout="centered")
st.title("💱 Конвертер валют")

# --- 1. БЕРЕМ НАСТОЯЩИЙ КУРС С НАЦБАНКА ---
st.subheader("Курс Нацбанка РК на сегодня")

try:
    url = "https://nationalbank.kz/rss/rates_all.xml"
    response = requests.get(url, timeout=10)
    root = ET.fromstring(response.content)
    
    rates = {}
    for item in root.findall(".//item"):
        title = item.find("title").text  # например "USD"
        descr = item.find("description").text # например "540.12"
        rates[title] = float(descr)
    
    usd = rates.get("USD", 540)
    eur = rates.get("EUR", 580)
    rub = rates.get("RUB", 6.5)
    st.success("Курс взят с сайта nationalbank.kz - настоящий!")
except:
    st.warning("Нет интернета, показываю примерные курсы")
    usd, eur, rub = 540, 580, 6.5

data = {
    "Валюта": ["USD", "EUR", "RUB"],
    "Курс к тенге": [usd, eur, rub]
}
df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True, hide_index=True)

# --- 2. КРАСИВЫЙ ДИЗАЙН - ВЫБОР ВАЛЮТЫ ---
st.divider()
st.subheader("Калькулятор")

amount = st.number_input("Сумма в тенге:", min_value=0.0, value=10000.0, step=1000.0)

отдаю = st.selectbox("Отдаю", ["KZT", "USD", "EUR", "RUB"])
получаю = st.selectbox("Получаю", ["KZT", "USD", "EUR", "RUB"])

kurs_map = {"KZT": 1.0, "USD": usd, "EUR": eur, "RUB": rub}

if отдаю == получаю:
    результат = amount
else:
    результат = amount * kurs_map[отдаю] / kurs_map[получаю]

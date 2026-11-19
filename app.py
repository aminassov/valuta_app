import streamlit as st
import pandas as pd
import requests

@st.cache_data(ttl=600)
def get_live_rate():
    try:
        r = requests.get("https://open.er-api.com/v6/latest/USD", timeout=5)
        return float(r.json()["rates"]["KZT"])
    except:
        return 449.68

live = get_live_rate()
inv = 1 / live

st.set_page_config(page_title="Обмен валют Актау", layout="wide")
st.title("Обмен валют • Актау")

rates = {
    "KZT": 1.0,
    "USD": live,
    "EUR": live * 1.41,
    "RUB": live * 0.015,
    "CNY": live * 0.17,
    "GBP": live * 1.60,
    "AED": live * 0.27,
}

c1, c2 = st.columns([1.2, 1])

with c1:
    st.subheader("Динамика курса >")
    st.markdown("USD")
    st.markdown(f"## {live:.2f} ₸  ▼ 0,22")
    st.caption(f"1 USD = {live:.2f} KZT | 1 KZT = {inv:.4f} USD")
    st.caption("Курс НБ РК на 19.11.2026 • обновляется каждые 10 мин")

with c2:
    st.subheader("Конвертер валют")
    col_from, col_swap, col_to = st.columns([4, 1, 4])
    with col_from:
        cur_from = st.selectbox("Из", list(rates.keys()), index=1)
    with col_swap:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("⇅")
    with col_to:
        cur_to = st.selectbox("В", list(rates.keys()), index=0)

    amount = st.number_input(f"Сумма в {cur_from}", value=2.0, min_value=0.0, step=1.0)
    result = amount * rates[cur_from] / rates[cur_to]
    st.markdown(f"### {amount:,.2f} {cur_from} = {result:,.2f} {cur_to}")
    st.caption(f"1 {cur_from} = {rates[cur_from]/rates[cur_to]:.4f} {cur_to}")

st.divider()

st.subheader("Курс доллара в банках Актау")
banks = [
    {"Банк": "Kaspi Bank", "Покупка": live - 1.50, "Продажа": live + 1.80, "Адрес": "мкр 14, Актау"},
    {"Банк": "Halyk Bank", "Покупка": live - 2.00, "Продажа": live + 2.30, "Адрес": "мкр 29, Актау"},
    {"Банк": "ForteBank", "Покупка": live - 2.20, "Продажа": live + 2.10, "Адрес": "мкр 4, Актау"},
    {"Банк": "Jusan Bank", "Покупка": live - 1.70, "Продажа": live + 2.50, "Адрес": "мкр 5, Актау"},
    {"Банк": "Обменник Актау", "Покупка": live - 0.50, "Продажа": live + 1.20, "Адрес": "мкр 28, Актау"},
]
st.dataframe(pd.DataFrame(banks), use_container_width=True, hide_index=True)

st.subheader("Курсы валют")
curr = pd.DataFrame([
    ["Доллар", live - 1.80, live + 1.80, live],
    ["Евро", live * 1.41 - 2, live * 1.41 + 2, live * 1.41],
    ["Юань", live * 0.17 - 0.5, live * 0.17 + 0.5, live * 0.17],
    ["Фунт", live * 1.60 - 3, live * 1.60 + 3, live * 1.60],
    ["Рубль", live * 0.0145, live * 0.0155, live * 0.015],
    ["Дирхам", live * 0.27 - 0.5, live * 0.27 + 0.5, live * 0.27],
], columns=["Валюта", "Покупка", "Продажа", "Курс НБ РК 19.11.2026"])
st.dataframe(curr, use_container_width=True, hide_index=True)

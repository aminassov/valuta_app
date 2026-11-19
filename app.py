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
    "KZT": 1.0, "USD": live, "EUR": live * 1.41,
    "RUB": live * 0.015, "CNY": live * 0.17,
    "GBP": live * 1.60, "AED": live * 0.27,
}

c1, c2 = st.columns([1.2, 1])
with c1:
    st.subheader("Динамика курса")
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
st.subheader("🏦 Офисы банков")


offices = [
   
    {"Банк": "Kaspi Bank", "Адрес": "мкр 14, д. 12, Актау", "Часы": "Пн-Вс: 09:00 – 20:00", "Покупка": live-1.5, "Продажа": live+1.8, "lat": 43.652, "lon": 51.175},
    {"Банк": "Kaspi Bank", "Адрес": "мкр 27, ТЦ Актау, Актау", "Часы": "Пн-Вс: 10:00 – 22:00", "Покупка": live-1.3, "Продажа": live+1.6, "lat": 43.661, "lon": 51.185},
    {"Банк": "Kaspi Bank", "Адрес": "мкр 29, пр. Абая, Актау", "Часы": "Пн-Сб: 09:00 – 19:00", "Покупка": live-1.6, "Продажа": live+1.9, "lat": 43.665, "lon": 51.190},
 
    {"Банк": "Halyk Bank", "Адрес": "мкр 29, ул. Абая, Актау", "Часы": "Пн-Пт: 09:00 – 18:00", "Покупка": live-2.0, "Продажа": live+2.3, "lat": 43.663, "lon": 51.188},
    {"Банк": "Halyk Bank", "Адрес": "мкр 8, д. 5, Актау", "Часы": "Пн-Сб: 09:00 – 19:00", "Покупка": live-2.1, "Продажа": live+2.4, "lat": 43.646, "lon": 51.172},

    {"Банк": "ForteBank", "Адрес": "мкр 4, д. 20, Актау", "Часы": "Пн-Пт: 09:00 – 18:00", "Покупка": live-2.2, "Продажа": live+2.1, "lat": 43.640, "lon": 51.170},
    {"Банк": "ForteBank", "Адрес": "мкр 16, БЦ Актау, Актау", "Часы": "Пн-Вс: 09:00 – 20:00", "Покупка": live-2.0, "Продажа": live+2.0, "lat": 43.655, "lon": 51.178},
    
    {"Банк": "Jusan Bank", "Адрес": "мкр 5, д. 8, Актау", "Часы": "Пн-Пт: 09:00 – 18:00", "Покупка": live-1.7, "Продажа": live+2.5, "lat": 43.644, "lon": 51.174},
   
    {"Банк": "Обменник Актау", "Адрес": "мкр 28, рынок, Актау", "Часы": "Пн-Вс: 08:00 – 23:00", "Покупка": live-0.5, "Продажа": live+1.2, "lat": 43.658, "lon": 51.182},
]
df = pd.DataFrame(offices)


bank = st.selectbox("Выбери банк — кликни на название:", ["Все банки"] + sorted(df["Банк"].unique().tolist()))

if bank == "Все банки":
    show = df
else:
    show = df[df["Банк"] == bank]


st.map(show[["lat","lon"]], zoom=12)


for _, row in show.iterrows():
    with st.container(border=True):
        c_left, c_right = st.columns([2, 1])
        with c_left:
            st.markdown(f"**{row['Адрес']}**")
            st.caption(f"🕒 {row['Часы']}")
            st.markdown(f"Покупка: **{row['Покупка']:.2f} ₸** &nbsp;&nbsp; Продажа: **{row['Продажа']:.2f} ₸**")
        with c_right:
            url = f"https://www.google.com/maps/search/?api=1&query={row['lat']},{row['lon']}"
            st.link_button("🗺️ Маршрут", url, use_container_width=True)
            if st.button("Зарезервировать сумму", key=f"{row['Адрес']}", use_container_width=True):
                st.success(f"Заявка на {row['Адрес']} отправлена! С тобой свяжутся.")

st.divider()
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

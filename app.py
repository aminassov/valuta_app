import streamlit as st
import pandas as pd

st.set_page_config(page_title="Валюта Актау", page_icon="💱", layout="wide")
st.title("💱 Валюта Актау")
st.caption("Курсы в банках Актау • Маршруты • Обновлено")

# --- Валюта ---
currencies = ["USD", "EUR", "RUB", "KZT", "CNY", "TRY", "GBP"]
col1, col2, col3 = st.columns(3)
with col1:
    amount = st.number_input("Сумма", value=100.0, min_value=0.0)
with col2:
    from_cur = st.selectbox("Из", currencies, index=0)
with col3:
    to_cur = st.selectbox("В", currencies, index=3)

# --- Загрузка банков ---
try:
    df = pd.read_csv("banks_aktau.csv")
except:
    # демо-данные, если файла нет
    df = pd.DataFrame([
        {"bank":"Kaspi Bank","district":"9 мкр","USD_buy":540,"USD_sell":545,"EUR_buy":590,"EUR_sell":595,"address":"9 мкр, 12"},
        {"bank":"Halyk Bank","district":"14 мкр","USD_buy":539,"USD_sell":546,"EUR_buy":589,"EUR_sell":596,"address":"14 мкр, 5"},
        {"bank":"ForteBank","district":"27 мкр","USD_buy":541,"USD_sell":544,"EUR_buy":591,"EUR_sell":594,"address":"27 мкр, 3"},
        {"bank":"Jusan Bank","district":"8 мкр","USD_buy":538,"USD_sell":547,"EUR_buy":588,"EUR_sell":597,"address":"8 мкр, 20"},
        {"bank":"Bank CenterCredit","district":"11 мкр","USD_buy":540,"USD_sell":545,"EUR_buy":590,"EUR_sell":595,"address":"11 мкр, 8"},
        {"bank":"Eurasian Bank","district":"29 мкр","USD_buy":539,"USD_sell":546,"EUR_buy":589,"EUR_sell":596,"address":"29 мкр, 15"},
        {"bank":"Home Credit","district":"15 мкр","USD_buy":538,"USD_sell":547,"EUR_buy":588,"EUR_sell":597,"address":"15 мкр, 2"},
    ])

# --- Фильтр по микрорайону ---
districts = ["Все"] + sorted(df["district"].astype(str).unique().tolist()) if "district" in df.columns else ["Все"]
sel_district = st.selectbox("Фильтр по микрорайону", districts)
if sel_district != "Все":
    df = df[df["district"].astype(str) == sel_district]

st.subheader(f"Банки: {len(df)}")
for _, row in df.iterrows():
    bank = row.get("bank","Банк")
    addr = row.get("address","Актау")
    district = row.get("district","")
    with st.expander(f"🏦 {bank} — {district} • {addr}"):
        st.write(f"**Адрес:** {addr}, Актау")
        # Показываем курсы если есть
        st.write(row.to_dict())
        # Маршруты
        q = f"{bank} {addr} Актау"
        st.markdown(f"[📍 Google Maps](https://www.google.com/maps/search/?api=1&query={q}) | [🚕 Яндекс Карты](https://yandex.kz/maps/?text={q})")

st.info("Ссылка не меняется: https://valuta-app-aqtau.streamlit.app/")

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Валюта Актау", page_icon="💱", layout="wide")
st.title("💱 Валюта Актау")
st.caption("Курсы в банках Актау • Проверено в кассе 27.11.2026 в 11:23")

# --- ДАННЫЕ ---
# Курсы ЦентрКредит - РЕАЛЬНЫЕ с табло, 27.11.2026
# Касса: USD 456.00 / 460.00, EUR 500.50 / 505.50, RUB 4.690 / 5.600
# Приложение (Нацбанк): USD 458.11 / 459.61

banks_data = [
    {"bank": "Bank CenterCredit", "district": "26 мкр", "address": "26 мкр, д.16", "USD_buy": 456.00, "USD_sell": 460.00, "EUR_buy": 500.50, "EUR_sell": 505.50, "RUB_buy": 4.69, "RUB_sell": 5.60, "source": "Касса 27.11 11:23 ✅"},
    {"bank": "Kaspi Bank", "district": "9 мкр", "address": "9 мкр, 12", "USD_buy": 457.00, "USD_sell": 459.50, "EUR_buy": 501.00, "EUR_sell": 504.00, "RUB_buy": 4.70, "RUB_sell": 5.50, "source": "Приложение"},
    {"bank": "Halyk Bank", "district": "14 мкр", "address": "14 мкр, 5", "USD_buy": 456.50, "USD_sell": 460.50, "EUR_buy": 500.00, "EUR_sell": 506.00, "RUB_buy": 4.65, "RUB_sell": 5.65, "source": "Приложение"},
    {"bank": "ForteBank", "district": "27 мкр", "address": "27 мкр, 3", "USD_buy": 457.50, "USD_sell": 459.00, "EUR_buy": 502.00, "EUR_sell": 504.50, "RUB_buy": 4.72, "RUB_sell": 5.45, "source": "Приложение"},
    {"bank": "Jusan Bank", "district": "8 мкр", "address": "8 мкр, 20", "USD_buy": 455.00, "USD_sell": 461.00, "EUR_buy": 499.00, "EUR_sell": 507.00, "RUB_buy": 4.60, "RUB_sell": 5.70, "source": "Приложение"},
    {"bank": "Eurasian Bank", "district": "29 мкр", "address": "29 мкр, 15", "USD_buy": 456.00, "USD_sell": 460.00, "EUR_buy": 500.00, "EUR_sell": 506.00, "RUB_buy": 4.68, "RUB_sell": 5.60, "source": "Приложение"},
    {"bank": "Home Credit", "district": "15 мкр", "address": "15 мкр, 2", "USD_buy": 455.50, "USD_sell": 461.50, "EUR_buy": 498.50, "EUR_sell": 507.50, "RUB_buy": 4.62, "RUB_sell": 5.75, "source": "Приложение"},
]
df = pd.DataFrame(banks_data)

# --- КАЛЬКУЛЯТОР ---
st.subheader("🧮 Калькулятор")
col1, col2, col3, col4 = st.columns(4)
with col1:
    amount = st.number_input("Сумма", value=100.0, min_value=0.0, step=10.0)
with col2:
    from_cur = st.selectbox("У меня", ["USD", "EUR", "RUB"], index=0)
with col3:
    operation = st.selectbox("Хочу", ["Продать банку (получить тенге)", "Купить у банка (отдать тенге)"])
with col4:
    sel_district = st.selectbox("Микрорайон", ["Все"] + sorted(df["district"].unique().tolist()))

df_filtered = df if sel_district == "Все" else df[df["district"] == sel_district]

# Расчет
buy_col = f"{from_cur}_buy"
sell_col = f"{from_cur}_sell"

if operation.startswith("Продать"):
    # Лучший курс покупки = максимальный buy
    best_idx = df_filtered[buy_col].idxmax()
    best = df_filtered.loc[best_idx]
    best_rate = best[buy_col]
    result = amount * best_rate
    st.success(f"💰 Лучший курс: **{best['bank']}** — {best_rate} ₸ за 1 {from_cur} ({best['address']}, {best['source']})")
    st.metric(f"Ты получишь", f"{result:,.0f} ₸")
else:
    best_idx = df_filtered[sell_col].idxmin()
    best = df_filtered.loc[best_idx]
    best_rate = best[sell_col]
    result = amount * best_rate
    st.success(f"💰 Лучший курс: **{best['bank']}** — {best_rate} ₸ за 1 {from_cur} ({best['address']}, {best['source']})")
    st.metric(f"Тебе нужно отдать", f"{result:,.0f} ₸")

# --- ТАБЛИЦА БАНКОВ ---
st.divider()
st.subheader(f"🏦 Банки: {len(df_filtered)}")
import urllib.parse
for _, row in df_filtered.iterrows():
    is_center = "CenterCredit" in row["bank"]
    # Короткое название без дубля: только банк + адрес
    label = f"🏦 {row['bank']} — {row['address']}{' ✅' if is_center else ''}"
    with st.expander(label, expanded=is_center):
        c1, c2, c3 = st.columns(3)
        c1.write(f"**USD:** {row['USD_buy']} / {row['USD_sell']}")
        c2.write(f"**EUR:** {row['EUR_buy']} / {row['EUR_sell']}")
        c3.write(f"**RUB:** {row['RUB_buy']} / {row['RUB_sell']}")
        st.caption(f"Источник: {row['source']}")
        q = urllib.parse.quote(f"{row['bank']} {row['address']} Актау")
        st.markdown(f"[📍 Google Maps](https://www.google.com/maps/search/?api=1&query={q}) | [🚕 Яндекс Карты](https://yandex.kz/maps/?text={q})")
st.info("Ссылка не меняется: https://valuta-app-aqtau.streamlit.app/ • Курсы кассы ЦентрКредит обновлены 27.11.2026 в 11:23")

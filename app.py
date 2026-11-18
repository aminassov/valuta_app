import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Конвертер валют Актау", layout="centered")
st.title("💱 Конвертер валют - Актау")
rates = {"USD": 540.0, "EUR": 580.0, "RUB": 6.5, "KZT": 1.0}
date_str = "сегодня"
is_fallback = False

file_to_read = None
if os.path.exists("rates_aktau_latest.csv"):
    try:
        tmp = pd.read_csv("rates_aktau_latest.csv")
        if len(tmp) > 0:
            file_to_read = "rates_aktau_latest.csv"
    except:
        pass

if file_to_read is None and os.path.exists("rates_history.csv"):
    file_to_read = "rates_history.csv"
    is_fallback = True

if file_to_read:
    try:
        df_rates = pd.read_csv(file_to_read)
        if file_to_read == "rates_history.csv":
            last_date = df_rates["date"].max()
            df_rates = df_rates[df_rates["date"] == last_date]
        for _, row in df_rates.iterrows():
            cur = str(row["currency"]).strip()
            val = float(row["buy"])
            rates[cur] = val
        if len(df_rates) > 0:
            date_str = str(df_rates.iloc[0]["date"])
    except Exception as e:
        st.warning(f"Не смог прочитать файл с курсами: {e}")

st.subheader(f"Курс Нацбанка РК на {date_str}")
if is_fallback:
    st.info("Сегодня Нацбанк не обновился, показываю последний зафиксированный курс")
else:
    st.success("Курсы обновляются автоматически каждый день в 09:00 по Актау")

data = {
    "Валюта": ["USD", "EUR", "RUB"],
    "Курс к тенге": [rates["USD"], rates["EUR"], rates["RUB"]]
}
st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)
st.divider()
st.markdown("### Калькулятор")

отдаю = st.selectbox("Отдаю", ["KZT", "USD", "EUR", "RUB"])
amount = st.number_input(f"Сумма в {отдаю}", value=300.0, min_value=0.0)
получаю = st.selectbox("Получаю", ["KZT", "USD", "EUR", "RUB"])

if отдаю == получаю:
    результат = amount
    курс_auto = 1.0
else:
    курс_auto = rates[отдаю] / rates[получаю]
    результат = amount * курс_auto

st.info(f"Автоматический курс: 1 {отдаю} = {курс_auto:.4f} {получаю}")
st.success(f"Получаю: {результат:.2f} {получаю}")
st.caption(f"Курс Нацбанка на {date_str}. Для точного расчета в обменнике Актау уточняй курс покупки/продажи.")
st.markdown("---")
st.subheader("🏦 Где выгоднее в Актау - Топ обменников")

try:
    from banks_aktau import get_aktau_rates
    df_banks = get_aktau_rates()
    st.dataframe(df_banks, use_container_width=True, hide_index=True)
    st.caption("Продаешь USD - смотри на самую высокую ПОКУПКУ. Покупаешь USD - смотри на самую низкую ПРОДАЖУ. Данные: kurs.kz")
except Exception as e:
    st.info("Не удалось загрузить курсы обменников, попробуй обновить страницу")

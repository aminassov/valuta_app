import streamlit as st
import pandas as pd

st.set_page_config(page_title="Курсы Актау", layout="wide")

if "open_bank" not in st.session_state:
    st.session_state.open_bank = None

# --- ВСПЛЫВАЮЩЕЕ ОКНО КАК У КАМКОМБАНК ---
@st.dialog("Детали пункта обмена", width="large")
def show_bank_detail(row, mode, amount):
    # Шапка
    st.markdown(f"### {row['Цвет']} {row['Банк']}")
    st.caption("Офис")

    c_left, c_right = st.columns([1.2, 1])

    with c_left:
        # Карта Актау - 2GIS
        map_url = f"https://2gis.kz/aktau/search/{row['Банк']} Актау"
        st.markdown(f"""
        <div style="background:#1E222B; border-radius:12px; padding:10px;">
        <a href="{map_url}" target="_blank" style="color:white; text-decoration:none;">
        <div style="background:#2A2F3A; border-radius:10px; height:180px; display:flex; align-items:center; justify-content:center; font-size:40px;">🗺️<br></div>
        <div style="font-size:13px; color:#0095FF; margin-top:8px;">📍 Открыть в 2GIS →</div>
        </a>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"**Адрес**<br>{row['Адрес']}", unsafe_allow_html=True)
        st.markdown(f"📍 **{row['Район']}**")
        st.link_button("Построить маршрут", map_url)
        st.markdown(f"🟢 **Открыто до 21:00**<br>ПН-ВС: 09:00-21:00", unsafe_allow_html=True)
        st.caption(f"🕐 Часы: {row['Часы']}")

    with c_right:
        # Курсы справа как на скрине
        st.markdown(f"""
        <div style="background:#1E222B; border-radius:12px; padding:16px;">
            <div style="display:flex; gap:20px;">
                <div>
                    <div style="color:#9AA0AE; font-size:13px;">Я покупаю</div>
                    <div style="font-size:24px; font-weight:700; color:white;">{row['Продажа']:.2f} ₸</div>
                </div>
                <div>
                    <div style="color:#9AA0AE; font-size:13px;">Я продаю</div>
                    <div style="font-size:24px; font-weight:700; color:white;">{row['Покупка']:.2f} ₸</div>
                </div>
            </div>
            <div style="color:#9AA0AE; font-size:13px; margin-top:10px;">🕐 Обновлено {row['Обновлено']} мин. назад</div>
            <div style="background:#262B36; border-radius:10px; padding:12px; margin-top:12px;">
                🔔 <b>Не пропустите выгодный курс в приложении</b> >
            </div>
            <div style="margin-top:14px;">✅ <b>Бесплатный резерв суммы</b></div>
            <div style="color:#9AA0AE; font-size:13px;">Банк сохранит нужную сумму для вас до конца дня</div>
        </div>
        """, unsafe_allow_html=True)

        if mode == "Я покупаю":
            total = int(amount * row['Продажа'])
            st.markdown(f"**{amount} $ ADD = {total:,} ₸**")
        else:
            total = int(amount * row['Покупка'])
            st.markdown(f"**{amount} $ ADD = {total:,} ₸**")

        if st.button("Резервировать сумму", type="primary", use_container_width=True):
            st.success(f"✅ Готово! {row['Банк']} зарезервировал {amount} $ для вас до конца дня. Перезвонят: {row['Телефон']}")
        st.link_button(f"📞 {row['Телефон']}", f"tel:{row['Телефон']}")

    if st.button("Закрыть"):
        st.session_state.open_bank = None
        st.rerun()

# --- ОСНОВНОЙ ЭКРАН ---
st.markdown("### Сравнивайте лучшие курсы валют в банках Актау на сегодня.")

col1, col2, col3 = st.columns([1.2, 1.2, 1])
with col1:
    mode = st.selectbox("Все курсы", ["Все курсы", "Я покупаю", "Я продаю"])
with col2:
    amount = st.number_input("Сумма", value=1000, step=100)
with col3:
    currency = st.selectbox("Валюта", ["USD", "EUR", "RUB"])

data = [
    {"Банк": "Kaspi Bank", "Покупка": 543.20, "Продажа": 545.50, "Адрес": "Офис • мкр 14, Актау", "Район": "мкр 14 • 700 м", "Обновлено": 8, "Теги": ["Есть новые купюры"], "Цвет": "🔴", "Телефон": "+7 727 258 59 89", "Часы": "Пн-Пт 09:00-18:00, Сб 10:00-14:00"},
    {"Банк": "Halyk Bank", "Покупка": 542.80, "Продажа": 546.00, "Адрес": "Офис • мкр 29, Актау", "Район": "мкр 29 • 1200 м", "Обновлено": 12, "Теги": ["Можно зарезервировать", "Есть новые купюры"], "Цвет": "🟢", "Телефон": "+7 727 259 07 77", "Часы": "Пн-Пт 09:00-17:30"},
    {"Банк": "Обменник Актау", "Покупка": 544.00, "Продажа": 544.90, "Адрес": "Пункт обмена • мкр 28, Актау", "Район": "мкр 28 • 300 м", "Обновлено": 4, "Теги": ["Есть новые купюры", "Без комиссии", "Обмен старых на новые"], "Цвет": "🟡", "Телефон": "+7 700 123 45 67", "Часы": "Ежедневно 09:00-21:00"},
]
df = pd.DataFrame(data)
if mode == "Я покупаю":
    df = df.sort_values("Продажа", ascending=True)
elif mode == "Я продаю":
    df = df.sort_values("Покупка", ascending=False)

st.markdown(f"**{len(df)} предложений** • Обновлено каждые 30 мин")

for idx, row in df.iterrows():
    tags = " ".join([f" `{t}` " for t in row["Теги"]])
    st.markdown(f"{tags}")
    c1, c2, c3, c4 = st.columns([2.2, 1.1, 1.1, 1.3])
    with c1:
        st.markdown(f"**{row['Цвет']} {row['Банк']}**\n\n🏠 {row['Адрес']}\n\n📍 {row['Район']}")
    with c2:
        st.caption("Я покупаю")
        st.markdown(f"### {row['Продажа']:.2f} ₸")
    with c3:
        st.caption("Я продаю")
        st.markdown(f"### {row['Покупка']:.2f} ₸")
    with c4:
        st.caption("О банке >")
        if st.button("Подробнее", key=f"det_{idx}_{row['Банк']}", type="primary"):
            st.session_state.open_bank = row["Банк"]
            st.rerun()
    # Если нажали Подробнее - открываем окно как у КАМКОМБАНК
    if st.session_state.open_bank == row["Банк"]:
        show_bank_detail(row, mode, amount)
        st.session_state.open_bank = None

st.caption("Курсы обновляются каждые 30 мин • Актау")

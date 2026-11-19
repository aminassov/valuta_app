import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Курсы Актау", layout="wide")

if "open_bank" not in st.session_state:
    st.session_state.open_bank = None

st.markdown("""
<style>
body { background-color:#12141A; }
.card { background:#1E222B; border-radius:16px; padding:16px 20px; margin-bottom:12px; }
.tag { background:#1A4D2E; color:#7ED99A; border-radius:6px; padding:4px 8px; font-size:12px; margin-right:6px; }
.tag2 { background:#3B2F4A; color:#C9A0FF; border-radius:6px; padding:4px 8px; font-size:12px; margin-right:6px; }
.stButton button { background:#0095FF; color:white; border-radius:12px; font-weight:600; }
</style>
""", unsafe_allow_html=True)

st.markdown("Сравнивайте лучшие курсы валют в банках Актау на сегодня.")


c_chart, c_conv = st.columns([2, 1])
with c_chart:
    st.markdown("### Динамика курса >")
    
    y = [512, 505, 498, 515, 528, 535, 542, 540, 548, 544, 545, 544]
    x = np.linspace(0, 1, 100)
    y_plot = np.interp(x, np.linspace(0, 1, len(y)), y)
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=y_plot, mode='lines', line=dict(color='#00E676', width=2), fill='tozeroy', fillcolor='rgba(0,230,118,0.15)'))
    fig.update_layout(paper_bgcolor='#1E222B', plot_bgcolor='#1E222B', height=160, margin=dict(l=0,r=0,t=10,b=10), xaxis=dict(showgrid=False, showticklabels=False), yaxis=dict(showgrid=False, showticklabels=False))
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown("#### 🇺🇸 USD &nbsp; 544,00 ₸ <span style='color:#FF5252; font-size:16px;'>▼ 0,22</span> &nbsp; <span style='color:#9AA0AE; font-size:13px;'>март &nbsp; апр &nbsp; май &nbsp; июнь &nbsp; июль &nbsp; авг &nbsp; сент &nbsp; окт &nbsp; ноя</span>", unsafe_allow_html=True)

with c_conv:
    st.markdown("### Конвертер")
    amt = st.number_input("Сумма", value=1, key="conv_amt")
    st.markdown(f"<div style='text-align:center; font-size:20px;'>⇅</div><div style='font-size:18px;'>1 USD = 544,00 KZT<br>1 KZT = 0,0018 USD</div><div style='font-size:22px; font-weight:700; margin-top:10px;'>{amt} USD = {amt*544:,.0f} KZT</div>", unsafe_allow_html=True)

st.markdown("## Все курсы банков <span style='color:#0095FF;'>Актау</span>", unsafe_allow_html=True)


f1, f2, f3 = st.columns([2.2, 1.5, 1.2])
with f1:
    mode = st.segmented_control("Режим", ["Все курсы", "Я покупаю", "Я продаю"], default="Все курсы")
with f2:
    amount = st.number_input("Сумма", value=1000, step=100)
with f3:
    currency = st.selectbox("Валюта", ["USD", "EUR", "RUB"])
    show_map = st.checkbox("📍 Показать на карте")


c = st.columns(7)
with c[0]: only_all = st.checkbox("Все фильтры")
with c[1]: sort_near = st.checkbox("Найти рядом")
with c[2]: only_new = st.checkbox("Новые и старые купюры")
with c[3]: only_reserve = st.checkbox("Есть резерв")
with c[4]: only_open = st.checkbox("Открыты сейчас")
with c[5]: only_office = st.checkbox("Офисы и банкоматы")
with c[6]: no_fee = st.checkbox("Без комиссии")


data = [
    {"Банк": "Kaspi Bank", "Покупка": 543.20, "Продажа": 545.50, "Адрес": "Офис • мкр 14, Актау", "Район": "мкр 14 • 700 м", "Обновлено": 3, "Теги": ["Можно зарезервировать", "Есть новые купюры", "Обмен старых на новые"], "Цвет": "🔴", "Телефон": "+7 727 258 59 89", "Часы": "Пн-Пт 09:00-18:00", "Описание": "Официальный курс Kaspi. Без комиссии."},
    {"Банк": "Halyk Bank", "Покупка": 542.80, "Продажа": 546.00, "Адрес": "Офис • мкр 29, Актау", "Район": "мкр 29 • 1200 м", "Обновлено": 3, "Теги": ["Есть новые купюры"], "Цвет": "🟢", "Телефон": "+7 727 259 07 77", "Часы": "Пн-Пт 09:00-17:30", "Описание": "Можно зарезервировать курс на 30 мин."},
    {"Банк": "ForteBank", "Покупка": 542.50, "Продажа": 545.80, "Адрес": "Офис • мкр 4, Актау", "Район": "мкр 4 • 2000 м", "Обновлено": 3, "Теги": ["Есть новые купюры"], "Цвет": "🟣", "Телефон": "+7 717 258 08 08", "Часы": "Пн-Пт 09:00-18:00", "Описание": "Принимают старые и новые купюры."},
    {"Банк": "Jusan Bank", "Покупка": 543.00, "Продажа": 546.20, "Адрес": "Офис • мкр 5, Актау", "Район": "мкр 5 • 900 м", "Обновлено": 3, "Теги": ["Можно зарезервировать"], "Цвет": "🟠", "Телефон": "+7 771 000 77 11", "Часы": "Пн-Пт 09:00-18:00", "Описание": "Быстрый обмен без очереди."},
    {"Банк": "Обменник Актау", "Покупка": 544.00, "Продажа": 544.90, "Адрес": "Пункт обмена • мкр 28, Актау", "Район": "мкр 28 • 300 м", "Обновлено": 3, "Теги": ["Есть новые купюры", "Без комиссии"], "Цвет": "🟡", "Телефон": "+7 700 123 45 67", "Часы": "Ежедневно 09:00-21:00", "Описание": "Лучший курс в Актау сегодня."},
]
df = pd.DataFrame(data)
if only_reserve:
    df = df[df["Теги"].apply(lambda x: "Можно зарезервировать" in x)]
if only_new:
    df = df[df["Теги"].apply(lambda x: "Есть новые купюры" in x)]


if mode == "Я покупаю":
    df = df.sort_values("Продажа", ascending=True)
elif mode == "Я продаю":
    df = df.sort_values("Покупка", ascending=False)

st.markdown(f"**{len(df)} предложений** &nbsp;&nbsp; ⇅ Популярные")

for idx, row in df.iterrows():
    tags_html = "".join([f'<span class="tag">{t}</span>' if t != "Обмен старых на новые" else f'<span class="tag2">{t}</span>' for t in row["Теги"]])
    # Карточка как КАМКОМБАНК
    c1, c2, c3, c4 = st.columns([2.2, 1.1, 1.1, 1.3])
    with c1:
        st.markdown(f"{tags_html}<br><br>**{row['Цвет']} {row['Банк']}**<br>🏠 {row['Адрес']}<br>🔴 {row['Район']}<br><span style='color:#9AA0AE; font-size:12px;'>Еще пункты обмена ∨</span>", unsafe_allow_html=True)
    with c2:
        st.caption("Я покупаю")
        st.markdown(f"### {row['Продажа']:.2f} ₸")
    with c3:
        st.caption("Я продаю")
        st.markdown(f"### {row['Покупка']:.2f} ₸")
    with c4:
        st.caption("О банке >")
        b1, b2, b3 = st.columns([1,1,1.5])
        with b1: st.link_button("📍", f"https://2gis.kz/aktau/search/{row['Банк']} Актау")
        with b2: st.link_button("📞", f"tel:{row['Телефон']}")
        with b3:
            if st.button("Подробнее", key=f"det_{idx}_{row['Банк']}"):
                st.session_state.open_bank = row["Банк"] if st.session_state.open_bank != row["Банк"] else None
                st.rerun()
    if mode == "Я покупаю":
        bottom = f"{amount} $ ADD = {int(amount * row['Продажа']):,} ₸"
    else:
        bottom = f"{amount} $ ADD = {int(amount * row['Покупка']):,} ₸"
    st.markdown(f"<div style='display:flex; justify-content:space-between;'><span style='color:#7ED99A; font-size:13px;'>{bottom}</span><span style='color:#7A7F8A; font-size:12px;'>Обновлено {row['Обновлено']} мин. назад</span></div><hr>", unsafe_allow_html=True)

    if st.session_state.open_bank == row["Банк"]:
        
        dl, dr = st.columns([1.2, 1])
        with dl:
            st.markdown(f"**Адрес**<br>{row['Адрес']}<br>📍 {row['Район']}")
            st.link_button("Построить маршрут", f"https://2gis.kz/aktau/search/{row['Банк']} Актау")
            st.markdown(f"🟢 Открыто до 21:00<br>🕐 {row['Часы']}")
        with dr:
            st.markdown(f"Я покупаю **{row['Продажа']:.2f} ₸** | Я продаю **{row['Покупка']:.2f} ₸**<br>Обновлено {row['Обновлено']} мин. назад<br>✅ Бесплатный резерв суммы")
            if st.button("Резервировать сумму", key=f"res_{idx}", type="primary"):
                st.success(f"✅ {row['Банк']} зарезервировал {amount} $ до конца дня. Перезвонят: {row['Телефон']}")


st.markdown("## Динамика стоимости доллара США в тенге")
st.caption("Изменения за год (12 месяцев)")
hist = pd.DataFrame([
    ["19 ноября 2026 г. (сегодня)", "1 USD = 544,00 KZT", "-1,45 ₸", "+0,00263%"],
    ["19 октября 2026 г.", "1 USD = 545,45 KZT", "+0,54 ₸", "-0,0296%"],
    ["19 сентября 2026 г.", "1 USD = 548,20 KZT", "+1,34 ₸", "-0,00719%"],
], columns=["Дата", "Среднемесячный курс", "Курс в начале месяца", "Курс в конце месяца"])
st.dataframe(hist, use_container_width=True, hide_index=True)

st.caption("Курсы обновляются каждые 30 мин • Актау • Все банки Актау")

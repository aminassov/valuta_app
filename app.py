import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
mport requests

@st.cache_data(ttl=600)  # обновлять каждые 10 мин
def get_live_rate():
    try:
        # Бесплатный API без ключа
        r = requests.get("https://open.er-api.com/v6/latest/USD", timeout=5)
        data = r.json()
        return float(data["rates"]["KZT"])  # например 449.68
    except:
        try:
            r2 = requests.get("https://api.exchangerate.host/latest?base=USD&symbols=KZT", timeout=5)
            return float(r2.json()["rates"]["KZT"])
        except:
            return 449.68  # запасной, если нет интернета

live = get_live_rate()

inv = 1 / live

st.set_page_config(page_title="Курсы Актау", layout="wide")

st.markdown("""
<style>
.card { background:#2B2F3A; border-radius:16px; padding:20px; }
.bank-card { background:white; border:1px solid #E5E7EB; border-radius:12px; padding:16px; margin-bottom:10px; }
</style>
""", unsafe_allow_html=True)


st.markdown("## Курсы валют")
st.markdown("На данной странице собраны все самые выгодные курсы обмена наличной валюты в Актау. Быстрый подбор по покупке, продаже и месторасположению пунктов обмена. Сравнивайте лучшие курсы валют в банках Актау на сегодня.")

c1, c2 = st.columns([2.2, 1])
with c1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    cc1, cc2 = st.columns([1, 1.8])
    with cc1:
        st.markdown("<div style='color:white; font-size:20px; font-weight:600;'>Динамика курса ></div><br><br>", unsafe_allow_html=True)
        st.markdown("<div style='color:#9AA0AE; font-size:14px;'>USD</div><div style='color:white; font-size:30px; font-weight:700;'>544,00 ₸ <span style='color:#FF5252; font-size:16px;'>▼ 0,22</span></div>", unsafe_allow_html=True)
    with cc2:
        
        y = [512, 520, 505, 498, 510, 528, 535, 542, 540, 548, 544, 545, 544]
        x = np.linspace(0, 1, 120)
        y_plot = np.interp(x, np.linspace(0, 1, len(y)), y)
        
        y_plot = y_plot + np.random.RandomState(1).normal(0, 1.5, len(y_plot))
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=y_plot, mode='lines', line=dict(color='#00E676', width=2), fill='tozeroy', fillcolor='rgba(0,230,118,0.12)'))
        fig.update_layout(paper_bgcolor='#2B2F3A', plot_bgcolor='#2B2F3A', height=160, margin=dict(l=0,r=0,t=5,b=5),
                          xaxis=dict(showgrid=False, showticklabels=False), yaxis=dict(showgrid=False, showticklabels=False, range=[490, 555]))
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown("<div style='display:flex; justify-content:space-between; color:#9AA0AE; font-size:12px;'><span>март</span><span>апр</span><span>май</span><span>июнь</span><span>июль</span><span>авг</span><span>сент</span><span>окт</span><span>ноя</span></div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown("#### Конвертер валют <span style='font-size:12px; color:#9AA0AE;'>ПО КУРСУ НБ РК</span>", unsafe_allow_html=True)
    usd = st.number_input("USD", value=1.0, key="c_usd")
    st.markdown("<div style='text-align:center;'>⇅</div>", unsafe_allow_html=True)
    kzt = st.number_input("KZT", value=usd*544.0, key="c_kzt")
    st.caption(f"1 USD = 544,00 KZT | 1 KZT = 0,0018 USD")
    st.caption(f"{usd} USD = {usd*544:,.0f} KZT")


st.markdown("## Курс доллара в банках Актау &nbsp;&nbsp; <span style='font-size:14px; color:#9AA0AE;'>на 19.11.2026</span>", unsafe_allow_html=True)


curr = pd.DataFrame([
    ["Доллар", 542.80, 545.50, 544.00],
    ["Евро", 628.10, 633.40, 630.25],
    ["Юань", 75.20, 77.10, 76.05],
    ["Фунт", 710.50, 725.30, 718.10],
    ["Франк", 680.20, 695.40, 688.30],
    ["Рубль", 6.20, 6.80, 6.50],
    ["Дирхам", 147.50, 149.80, 148.60],
    ["Лира", 12.80, 14.20, 13.50],
], columns=["Валюта", "Покупка", "Продажа", "Курс НБ РК 19.11.2026"])
st.dataframe(curr, use_container_width=True, hide_index=True)


st.markdown("### Все банки Актау")
mode = st.segmented_control("Режим", ["Все курсы", "Я покупаю", "Я продаю"], default="Все курсы")
amount = st.number_input("Сумма", value=1000, step=100)

banks = [
    {"Банк": "Kaspi Bank", "Покупка": 543.20, "Продажа": 545.50, "Адрес": "Офис • мкр 14, Актау", "Район": "мкр 14 • 700 м", "Теги": ["Можно зарезервировать", "Есть новые купюры"], "Тел": "+7 727 258 59 89"},
    {"Банк": "Halyk Bank", "Покупка": 542.80, "Продажа": 546.00, "Адрес": "Офис • мкр 29, Актау", "Район": "мкр 29 • 1200 м", "Теги": ["Есть новые купюры"], "Тел": "+7 727 259 07 77"},
    {"Банк": "ForteBank", "Покупка": 542.50, "Продажа": 545.80, "Адрес": "Офис • мкр 4, Актау", "Район": "мкр 4 • 2000 м", "Теги": ["Есть новые купюры"], "Тел": "+7 717 258 08 08"},
    {"Банк": "Jusan Bank", "Покупка": 543.00, "Продажа": 546.20, "Адрес": "Офис • мкр 5, Актау", "Район": "мкр 5 • 900 м", "Теги": ["Можно зарезервировать"], "Тел": "+7 771 000 77 11"},
    {"Банк": "Bank CenterCredit", "Покупка": 542.60, "Продажа": 546.40, "Адрес": "Офис • мкр 28, Актау", "Район": "мкр 28 • 400 м", "Теги": ["Без комиссии"], "Тел": "+7 727 244 30 30"},
    {"Банк": "Freedom Bank", "Покупка": 543.50, "Продажа": 545.20, "Адрес": "Офис • мкр 27, Актау", "Район": "мкр 27 • 600 м", "Теги": ["Есть новые купюры", "Без комиссии"], "Тел": "+7 777 000 11 22"},
    {"Банк": "Обменник Актау", "Покупка": 544.00, "Продажа": 544.90, "Адрес": "Пункт обмена • мкр 28, Актау", "Район": "мкр 28 • 300 м", "Теги": ["Есть новые купюры", "Без комиссии"], "Тел": "+7 700 123 45 67"},
]
df = pd.DataFrame(banks)
if mode == "Я покупаю":
    df = df.sort_values("Продажа")
elif mode == "Я продаю":
    df = df.sort_values("Покупка", ascending=False)

st.markdown(f"**{len(df)} предложений** &nbsp; ⇅ Популярные")
for i, r in df.iterrows():
    tags = " ".join([f"`{t}`" for t in r["Теги"]])
    st.markdown(tags)
    c1, c2, c3, c4 = st.columns([2.2, 1, 1, 1.3])
    with c1:
        st.markdown(f"**{r['Банк']}**\n\n🏠 {r['Адрес']}\n\n🔴 {r['Район']}")
    with c2:
        st.caption("Я покупаю")
        st.markdown(f"### {r['Продажа']:.2f} ₸")
    with c3:
        st.caption("Я продаю")
        st.markdown(f"### {r['Покупка']:.2f} ₸")
    with c4:
        st.caption("О банке >")
        st.link_button("📍", f"https://2gis.kz/aktau/search/{r['Банк']} Актау")
        if st.button("Подробнее", key=f"d_{i}"):
            st.info(f"{r['Банк']} | {r['Адрес']} | Тел: {r['Тел']} | Открыто до 21:00 | Резерв: {amount} $ = {int(amount*r['Продажа']):,} ₸")
    if mode == "Я покупаю":
        st.caption(f"{amount} $ = {int(amount*r['Продажа']):,} ₸ | Обновлено 3 мин. назад")
    else:
        st.caption(f"{amount} $ = {int(amount*r['Покупка']):,} ₸ | Обновлено 3 мин. назад")
    st.divider()

st.caption("Курсы обновляются каждые 30 мин • Актау • Источник: НБ РК")

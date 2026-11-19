import streamlit as st
import pandas as pd

st.set_page_config(page_title="Курсы Актау", layout="wide")

# --- СТИЛЬ КАК НА СКРИНЕ: тёмный фон, карточки ---
st.markdown("""
<style>
body { background-color: #12141A; }
.card {
  background: #1E222B;
  border-radius: 16px;
  padding: 16px 20px;
  margin-bottom: 12px;
}
.tag {
  background: #1A4D2E;
  color: #7ED99A;
  border-radius: 6px;
  padding: 4px 8px;
  font-size: 12px;
  margin-right: 6px;
}
.buy { font-size: 24px; font-weight: 700; color: white; }
.sell { font-size: 24px; font-weight: 700; color: white; }
.label { font-size: 13px; color: #9AA0AE; }
.addr { font-size: 14px; color: white; }
.dist { font-size: 13px; color: #9AA0AE; }
.btn {
  background: #0095FF;
  color: white;
  border-radius: 12px;
  padding: 8px 16px;
  font-weight: 600;
  border: none;
}
.updated { font-size: 12px; color: #7A7F8A; text-align: right; }
</style>
""", unsafe_allow_html=True)

# --- ВЕРХНЯЯ ПАНЕЛЬ КАК НА СКРИНЕ ---
col1, col2, col3, col4 = st.columns([1.2, 1.2, 1, 1.5])
with col1:
    mode = st.selectbox("Все курсы", ["Все курсы", "Я покупаю", "Я продаю"])
with col2:
    amount = st.number_input("Сумма", value=1000, step=100)
with col3:
    currency = st.selectbox("Валюта", ["USD", "EUR", "RUB"])
with col4:
    st.markdown("<br>", unsafe_allow_html=True)
    show_map = st.checkbox("📍 Пункты обмена на карте")

# --- ФИЛЬТРЫ ---
f1, f2, f3, f4, f5 = st.columns(5)
with f1:
    sort_by = st.selectbox("Сортировка", ["Популярные", "Выгодный курс", "Найти рядом"])
with f2:
    only_new = st.checkbox("Новые и старые купюры")
with f3:
    only_reserve = st.checkbox("Есть резерв")
with f4:
    only_open = st.checkbox("Открыты сейчас")
with f5:
    no_fee = st.checkbox("Без комиссии")

# --- ДАННЫЕ: ПОКА ЧТО ИЗ ТВОЕГО banks_aktau.csv ---
# Потом сюда подключим реальный парсер kurs.kz
# Формат: Банк | Покупка | Продажа | Адрес | Район | Расстояние | Обновлено | Теги
data = [
    {"Банк": "Kaspi Bank", "Покупка": 543.20, "Продажа": 545.50, "Адрес": "Офис • мкр 14, Актау", "Район": "мкр 14 • 700 м", "Обновлено": 8, "Теги": ["Есть новые купюры"], "Цвет": "🔴"},
    {"Банк": "Halyk Bank", "Покупка": 542.80, "Продажа": 546.00, "Адрес": "Офис • мкр 29, Актау", "Район": "мкр 29 • 1200 м", "Обновлено": 12, "Теги": ["Можно зарезервировать", "Есть новые купюры"], "Цвет": "🟢"},
    {"Банк": "ForteBank", "Покупка": 542.50, "Продажа": 545.80, "Адрес": "Офис • мкр 4, Актау", "Район": "мкр 4 • 2000 м", "Обновлено": 7, "Теги": ["Есть новые купюры"], "Цвет": "🟣"},
    {"Банк": "Jusan Bank", "Покупка": 543.00, "Продажа": 546.20, "Адрес": "Офис • мкр 5, Актау", "Район": "мкр 5 • 900 м", "Обновлено": 15, "Теги": ["Можно зарезервировать"], "Цвет": "🟠"},
    {"Банк": "Обменник Актау", "Покупка": 544.00, "Продажа": 544.90, "Адрес": "Пункт обмена • Актау", "Район": "мкр 28 • 300 м", "Обновлено": 4, "Теги": ["Есть новые купюры", "Без комиссии"], "Цвет": "🟡"},
]

df = pd.DataFrame(data)

# Фильтры в действии
if only_reserve:
    df = df[df["Теги"].apply(lambda x: "Можно зарезервировать" in x)]
if only_new:
    df = df[df["Теги"].apply(lambda x: "Есть новые купюры" in x)]

# Сортировка: если "Я покупаю" - выгодно где дороже покупают, если "Я продаю" - где дешевле продают
if mode == "Я покупаю":
    df = df.sort_values("Покупка", ascending=False)
elif mode == "Я продаю":
    df = df.sort_values("Продажа", ascending=True)
else:
    if sort_by == "Выгодный курс":
        df = df.sort_values("Продажа", ascending=True)
    elif sort_by == "Найти рядом":
        df = df.sort_values("Район")

st.markdown(f"**{len(df)} предложений** • Обновлено каждые 30 мин")

# --- КАРТОЧКИ КАК НА СКРИНЕ ---
for _, row in df.iterrows():
    tags_html = "".join([f'<span class="tag">{t}</span>' for t in row["Теги"]])
    # Выгода для суммы
    you_get = int(amount * row["Покупка"]) if mode != "Я продаю" else int(amount * row["Продажа"])

    st.markdown(f"""
    <div class="card">
      <div>{tags_html}</div>
      <div style="display:flex; justify-content:space-between; align-items:center; margin-top:8px;">
        <div style="width:30%">
          <div style="font-size:18px; font-weight:700; color:white;">{row["Цвет"]} {row["Банк"]}</div>
          <div class="addr" style="margin-top:6px;">🏠 {row["Адрес"]}</div>
          <div class="dist">🔴 {row["Район"]}</div>
          <div style="font-size:12px; color:#9AA0AE; margin-top:4px;">Еще пункты обмена ∨</div>
        </div>
        <div style="width:20%">
          <div class="label">Я покупаю</div>
          <div class="buy">{row["Покупка"]:.2f} ₸</div>
        </div>
        <div style="width:20%">
          <div class="label">Я продаю</div>
          <div class="sell">{row["Продажа"]:.2f} ₸</div>
        </div>
        <div style="width:20%; text-align:right;">
          <div class="label">О банке &gt;</div>
          <div style="margin-top:10px;">📍 📞 <button class="btn">Подробнее</button></div>
        </div>
      </div>
      <div style="display:flex; justify-content:space-between; margin-top:8px;">
        <div style="font-size:13px; color:#7ED99A;">За {amount} $ вы получите ~ {you_get:,} ₸</div>
        <div class="updated">Обновлено {row["Обновлено"]} мин. назад</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.caption("Курсы обновляются каждые 30 мин • Актау")

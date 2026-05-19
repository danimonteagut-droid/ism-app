import streamlit as st
import pandas as pd
from datetime import datetime
import yfinance as yf

st.set_page_config(page_title="ISM - Índice de Salud del Mercado", layout="wide")
st.title("📊 Índice de Salud del Mercado (ISM)")
st.markdown("**Modelo creado para evaluar el estado real de los mercados financieros**")

# ==================== DATOS EN TIEMPO REAL ====================
if st.button("🔄 Actualizar datos de mercado"):
    st.cache_data.clear()

@st.cache_data(ttl=60)
def get_market_data():
    try:
        vix = yf.Ticker("^VIX").history(period="1d")['Close'].iloc[-1]
        oil = yf.Ticker("BZ=F").history(period="1d")['Close'].iloc[-1]
        dxy = yf.Ticker("DX-Y.NYB").history(period="1d")['Close'].iloc[-1]
        gold = yf.Ticker("GC=F").history(period="1d")['Close'].iloc[-1]
        return round(vix, 2), round(oil, 2), round(dxy, 2), round(gold, 2)
    except:
        return None, None, None, None

vix, oil, dxy, gold = get_market_data()

# ==================== VALORES MANUALES EDITABLES ====================
st.subheader("📝 Ajusta los valores manuales")

scores = {
    "Resultados Empresariales": st.number_input("Resultados Empresariales", min_value=1.0, max_value=5.0, value=4.5, step=0.1),
    "Oferta y Demanda": st.number_input("Oferta y Demanda", min_value=1.0, max_value=5.0, value=3.0, step=0.1),
    "Flujos de Liquidez": st.number_input("Flujos de Liquidez", min_value=1.0, max_value=5.0, value=4.0, step=0.1),
    "Ciclo del Dólar": st.number_input("Ciclo del Dólar", min_value=1.0, max_value=5.0, value=4.0, step=0.1),
    "PIB/Crecimiento Económico": st.number_input("PIB/Crecimiento", min_value=1.0, max_value=5.0, value=4.0, step=0.1),
    "Sentimiento del Mercado": st.number_input("Sentimiento del Mercado", min_value=1.0, max_value=5.0, value=3.6, step=0.1),
    "Inflación": st.number_input("Inflación", min_value=1.0, max_value=5.0, value=2.0, step=0.1),
    "Tipos de Interés": st.number_input("Tipos de Interés", min_value=1.0, max_value=5.0, value=2.0, step=0.1),
    "Eventos Geopolíticos": st.number_input("Eventos Geopolíticos", min_value=1.0, max_value=5.0, value=3.0, step=0.1),
    "Confianza Consumidor/Inversor": st.number_input("Confianza Consumidor", min_value=1.0, max_value=5.0, value=3.5, step=0.1),
    "Tasa de Desempleo": st.number_input("Tasa de Desempleo", min_value=1.0, max_value=5.0, value=3.5, step=0.1),
    "Valoraciones de Mercado": st.number_input("Valoraciones de Mercado", min_value=1.0, max_value=5.0, value=3.2, step=0.1),
    "Volatilidad (VIX)": st.number_input("Volatilidad (VIX)", min_value=1.0, max_value=5.0, value=3.2, step=0.1),
}

# ==================== CÁLCULO ====================
weights = [18,15,12,10,10,9,4,4,7,6,5,5,4]
df = pd.DataFrame({
    "Variable": list(scores.keys()),
    "Peso (%)": weights,
    "Score": list(scores.values())
})
df["Ponderado"] = (df["Score"] * df["Peso (%)"] / 100).round(3)
total_ism = df["Ponderado"].sum().round(2)

# ==================== DASHBOARD ====================
col1, col2, col3 = st.columns(3)
col1.metric("**Índice ISM Actual**", f"{total_ism}")
col2.metric("**Interpretación**", "Neutral / Cauteloso")
col3.metric("**Fecha**", datetime.now().strftime("%d de mayo de 2026"))

st.subheader("📈 Datos de Mercado en Tiempo Real")
if vix is None:
    st.warning("⚠️ No se pudieron actualizar los datos en tiempo real.")
else:
    st.success(f"**VIX:** {vix} | **Petróleo Brent:** {oil} | **Dólar Index:** {dxy} | **Oro:** {gold}")

st.subheader("Detalle de Variables")
st.dataframe(df, use_container_width=True)

if total_ism >= 4.3:
    st.success("**Sesgo Ofensivo Moderado** → Mercado saludable")
elif total_ism >= 3.9:
    st.warning("**Neutral / Cauteloso** → Selectividad alta recomendada")
else:
    st.error("**Sesgo Defensivo** → Mayor precaución")

st.caption("App desarrollada con ❤️ y la ayuda de Grok (xAI)")

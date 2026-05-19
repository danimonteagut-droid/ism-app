import streamlit as st
import pandas as pd
from datetime import datetime
import yfinance as yf

st.set_page_config(page_title="ISM - Índice de Salud del Mercado", layout="wide")

st.title("📊 Índice de Salud del Mercado (ISM)")
st.markdown("**Herramienta para evaluar el estado actual de los mercados financieros**")

# ==================== DATOS EN TIEMPO REAL ====================
st.subheader("📈 Datos de Mercado en Tiempo Real")
if st.button("🔄 Actualizar datos automáticos"):
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

if vix is None:
    st.info("ℹ️ Datos en tiempo real no disponibles en este momento.")
else:
    st.success(f"**VIX:** {vix} | **Petróleo Brent:** {oil} | **Dólar Index:** {dxy} | **Oro:** {gold}")

# ==================== VALORES MANUALES EDITABLES ====================
st.subheader("📝 Ajustar valores manuales")

scores = {
    "Resultados Empresariales": st.number_input("Resultados Empresariales", 1.0, 5.0, 4.5, 0.1),
    "Oferta y Demanda": st.number_input("Oferta y Demanda", 1.0, 5.0, 3.0, 0.1),
    "Flujos de Liquidez": st.number_input("Flujos de Liquidez", 1.0, 5.0, 4.0, 0.1),
    "Ciclo del Dólar": st.number_input("Ciclo del Dólar", 1.0, 5.0, 4.0, 0.1),
    "PIB/Crecimiento Económico": st.number_input("PIB/Crecimiento", 1.0, 5.0, 4.0, 0.1),
    "Sentimiento del Mercado": st.number_input("Sentimiento del Mercado", 1.0, 5.0, 3.6, 0.1),
    "Inflación": st.number_input("Inflación", 1.0, 5.0, 2.0, 0.1),
    "Tipos de Interés": st.number_input("Tipos de Interés", 1.0, 5.0, 2.0, 0.1),
    "Eventos Geopolíticos": st.number_input("Eventos Geopolíticos", 1.0, 5.0, 3.0, 0.1),
    "Confianza Consumidor/Inversor": st.number_input("Confianza Consumidor", 1.0, 5.0, 3.5, 0.1),
    "Tasa de Desempleo": st.number_input("Tasa de Desempleo", 1.0, 5.0, 3.5, 0.1),
    "Valoraciones de Mercado": st.number_input("Valoraciones de Mercado", 1.0, 5.0, 3.2, 0.1),
    "Volatilidad (VIX)": st.number_input("Volatilidad (VIX)", 1.0, 5.0, 3.2, 0.1),
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

st.subheader("Detalle de Variables")
st.dataframe(df, use_container_width=True)

# Interpretación mejorada
if total_ism >= 4.3:
    st.success("**Sesgo Ofensivo Moderado** → Mercado saludable. Buen entorno para posiciones de crecimiento.")
elif total_ism >= 3.9:
    st.warning("**Neutral / Cauteloso** → Selectividad alta recomendada. Combinar growth con value.")
else:
    st.error("**Sesgo Defensivo** → Mayor precaución. Priorizar hedges y activos defensivos.")

st.caption("App desarrollada con ❤️ y la ayuda de Grok (xAI) | Uso solo informativo - No es asesoramiento financiero")

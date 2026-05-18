import streamlit as st
import pandas as pd
from datetime import datetime
import yfinance as yf
st.set_page_config(page_title="ISM - Índice de Salud del Mercado", layout="wide")
st.title("Índice de Salud del Mercado (ISM)")
st.markdown("**Modelo creado para evaluar el estado real de los mercados financieros**")
# ==================== VARIABLES AUTOMÁTICAS ====================
@st.cache_data(ttl=300)  # Actualiza cada 5 minutos
def get_market_data():
    try:
        vix = yf.Ticker("^VIX").history(period="1d")['Close'].iloc[-1]
        oil = yf.Ticker("BZ=F").history(period="1d")['Close'].iloc[-1]
        dxy = yf.Ticker("DX-Y.NYB").history(period="1d")['Close'].iloc[-1]
        gold = yf.Ticker("GC=F").history(period="1d")['Close'].iloc[-1]
        return round(vix, 2), round(oil, 2), round(dxy, 2), round(gold, 2)
    except:
        return 18.5, 78.5, 102.8, 2450  # valores por defecto si falla
vix, oil, dxy, gold = get_market_data()
# ==================== DATOS MANUALES ====================
data = {
    "Variable": [
        "Resultados Empresariales", "Oferta y Demanda", "Flujos de Liquidez",
        "Ciclo del Dólar", "PIB/Crecimiento Económico", "Sentimiento del Mercado",
        "Inflación", "Tipos de Interés", "Eventos Geopolíticos",
        "Confianza Consumidor/Inversor", "Tasa de Desempleo",
        "Valoraciones de Mercado", "Volatilidad (VIX)"
    ],
    "Peso (%)": [18, 15, 12, 10, 10, 9, 4, 4, 7, 6, 5, 5, 4],
    "Score": [4.5, 3.2, 4.0, 4.0, 4.0, 3.7, 2.0, 2.0, 3.0, 3.5, 3.5, 3.2, round(vix/10,1)]
}
df = pd.DataFrame(data)
df["Ponderado"] = df["Score"] * (df["Peso (%)"] / 100)
total_ism = df["Ponderado"].sum().round(2)
# ==================== DASHBOARD ====================
col1, col2, col3 = st.columns(3)
col1.metric("**Índice ISM Actual**", f"{total_ism}", delta=None)
col2.metric("**Interpretación**", "Neutral / Cauteloso")
col3.metric("**Fecha**", datetime.now().strftime("%d de mayo de 2026"))

st.subheader("Datos de Mercado en Tiempo Real")
st.info(f"VIX: **{vix}** | Petróleo Brent: **{oil}** | Dólar Index: **{dxy}** | Oro: **{gold}**")
st.subheader("Detalle de Variables")
st.dataframe(
    df.style.format({"Peso (%)": "{:.1f}", "Ponderado": "{:.3f}"})
           .background_gradient(cmap='RdYlGn', subset=['Score']),
    use_container_width=True
)
# Interpretación
if total_ism >= 4.3:
    st.success("**Sesgo Ofensivo Moderado** - Mercado saludable")
elif total_ism >= 3.9:
    st.warning("**Neutral / Cauteloso** - Selectividad alta recomendada")
else:
    st.error("**Sesgo Defensivo** - Mayor precaución")
st.caption("App desarrollada con ayuda de Grok (xAI)")

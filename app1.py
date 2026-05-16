import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Índice de Salud del Mercado (ISM)", layout="wide")
st.title("Índice de Salud del Mercado (ISM)")
st.markdown("**Tu modelo para evaluar el estado actual de los mercados**")

# Datos actuales (los puedes actualizar manualmente por ahora)
data = {
    "Variable": [
        "Resultados Empresariales", "Oferta y Demanda", "Flujos de Liquidez",
        "Ciclo del Dólar", "PIB/Crecimiento", "Sentimiento del Mercado",
        "Inflación", "Tipos de Interés", "Eventos Geopolíticos",
        "Confianza Consumidor/Inversor", "Tasa de Desempleo",
        "Valoraciones de Mercado", "Volatilidad (VIX)"

    ],
    "Peso (%)": [18, 15, 12, 10, 10, 9, 4, 4, 7, 6, 5, 5, 4],
    "Score": [4.5, 3.5, 4.0, 4.0, 4.0, 3.5, 2.0, 2.0, 3.0, 3.5, 3.5, 3.0, 3.0]

}

df = pd.DataFrame(data)
df["Ponderado"] = df["Score"] * (df["Peso (%)"] / 100)

total_ism = df["Ponderado"].sum()

# Mostrar resultados
col1, col2, col3 = st.columns(3)
col1.metric("**Índice ISM Actual**", f"{total_ism:.2f}", "0.00")
col2.metric("**Interpretación**", "Saludable / Cauteloso")
col3.metric("**Fecha**", datetime.now().strftime("%d de mayo de 2026"))

st.subheader("Detalle de Variables")
st.dataframe(df.style.format({"Peso (%)": "{:.1f}", "Ponderado": "{:.3f}"}), use_container_width=True)

st.subheader("Interpretación según el ISM")
if total_ism >= 4.1:
    st.success("**Sesgo Ofensivo Moderado** - Mercado saludable")
elif total_ism >= 3.5:
    st.warning("**Neutral / Cauteloso** - Selectividad alta")
else:
    st.error("**Sesgo Defensivo** - Mayor precaución")

# Instrucciones
st.info("Para actualizar los scores, modifica los valores en la columna 'Score' y guarda el archivo.")
 
st.caption("Desarrollado para tu canal")

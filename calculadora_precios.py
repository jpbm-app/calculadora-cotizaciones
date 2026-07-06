import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Cotizador Profesional", layout="centered")
st.title("🏗️ Cotizador de Proyectos")

# Conexión definida en los Secrets (que configuraremos en el paso 3)
conn = st.connection("gsheets", type=GSheetsConnection)

# Formulario
with st.form("cotizador"):
    producto = st.text_input("Nombre del Producto")
    proveedor = st.text_input("Nombre del Proveedor")
    costo = st.number_input("Costo base ($)", min_value=0.0, value=15000.0, step=100.0)
    tipo_venta = st.selectbox("Margen de ganancia", ["Menor (25%)", "Intermedia (18%)", "Mayor (16%)"])
    submit = st.form_submit_button("Guardar en Drive")

if submit:
    margenes = {"Menor (25%)": 0.25, "Intermedia (18%)": 0.18, "Mayor (16%)": 0.16}
    precio_final = costo / (1 - margenes[tipo_venta])
    
    # Preparar datos (debe coincidir con los encabezados del Paso 1)
    nueva_fila = pd.DataFrame([{
        "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Producto": producto,
        "Proveedor": proveedor,
        "Costo": costo,
        "Precio_Venta": round(precio_final, 0)
    }])
    
    # Leer actual y agregar
    datos_actuales = conn.read()
    conn.update(data=pd.concat([datos_actuales, nueva_fila]))
    st.success(f"Precio sugerido: ${precio_final:,.0f} guardado en Sheets.")

# Historial
if st.checkbox("Ver Historial Completo"):
    st.dataframe(conn.read())

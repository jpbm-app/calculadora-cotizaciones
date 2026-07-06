import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Cotizador Profesional", layout="centered")
st.title("🏗️ Cotizador de Proyectos")

conn = st.connection("gsheets", type=GSheetsConnection)

# Formulario de entrada
with st.form("cotizador"):
    producto = st.text_input("Nombre del Producto")
    proveedor = st.text_input("Nombre del Proveedor")
    costo = st.number_input("Costo base ($)", min_value=0.0, value=15000.0, step=100.0)
    
    # Selector de margen
    margen_seleccionado = st.selectbox("Margen de ganancia", ["Menor (25%)", "Intermedia (18%)", "Mayor (16%)"])
    
    # Cálculo inmediato en pantalla
    margenes = {"Menor (25%)": 0.25, "Intermedia (18%)": 0.18, "Mayor (16%)": 0.16}
    precio_calculado = costo / (1 - margenes[margen_seleccionado])
    
    st.write(f"### Precio de Venta Sugerido: ${precio_calculado:,.0f}")
    
    submit = st.form_submit_button("Guardar en Drive")

if submit:
    # Preparar la nueva fila con el precio ya calculado
    nueva_fila = pd.DataFrame([{
        "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Producto": producto,
        "Proveedor": proveedor,
        "Costo": costo,
        "Precio_Venta": round(precio_calculado, 0)
    }])
    
    # Guardar en Sheets
    conn.add_rows(nueva_fila)
    st.success("¡Datos guardados con éxito en Drive!")

# Historial
if st.checkbox("Ver Historial Completo"):
    st.dataframe(conn.read())

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
    costo = st.number_input("Costo base (CLP)", min_value=0.0, value=0.0, step=100.0)
    
    # Nuevos campos flexibles
    margen_libre = st.number_input("Margen de ganancia (%)", min_value=0.0, value=25.0, step=1.0)
    descuento = st.number_input("Descuento aplicado (%)", min_value=0.0, value=0.0, step=1.0)
    foto_url = st.text_input("URL de la Foto")
    
    # Cálculo: (Costo * (1 + margen/100)) * (1 - descuento/100)
    # Formateamos a entero (.0f) para quitar decimales y agregamos el sufijo CLP
    precio_venta = (costo * (1 + margen_libre/100)) * (1 - descuento/100)
    
    st.write(f"### 💰 Precio de Venta Final: {precio_venta:,.0f} CLP")
    
    submit = st.form_submit_button("Guardar Cotización en Drive")

if submit:
    if costo > 0:
        nueva_fila = pd.DataFrame([{
            "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Producto": producto,
            "Proveedor": proveedor,
            "Costo": int(costo),
            "Margen_%": margen_libre,
            "Descuento_%": descuento,
            "Precio_Venta": int(precio_venta),
            "Foto": foto_url
        }])
        
        conn.add_rows(nueva_fila)
        st.success("¡Cotización guardada exitosamente!")
    else:
        st.error("Por favor, ingresa un costo base válido.")

# Historial
if st.checkbox("Ver Historial Completo"):
    st.dataframe(conn.read())

import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Cotizador Profesional", layout="centered")
st.title("🏗️ Cotizador de Proyectos")

conn = st.connection("gsheets", type=GSheetsConnection)

with st.form("cotizador"):
    producto = st.text_input("Nombre del Producto")
    proveedor = st.text_input("Nombre del Proveedor")
    costo = st.number_input("Costo base (CLP)", min_value=0.0, value=0.0, step=100.0, format="%d")
    
    margen_libre = st.number_input("Margen de ganancia (%)", min_value=0.0, value=25.0, step=1.0, format="%d")
    descuento_porc = st.number_input("Descuento aplicado (%)", min_value=0.0, value=0.0, step=1.0, format="%d")
    foto_url = st.text_input("URL de la Foto")
    
    # Cálculos detallados
    subtotal = costo * (1 + margen_libre / 100)
    monto_descuento = subtotal * (descuento_porc / 100)
    total_final = subtotal - monto_descuento
    
    # Mostrar resultados sin decimales
    st.write(f"**Subtotal (Precio Preliminar):** {subtotal:,.0f} CLP")
    st.write(f"**Descuento aplicado:** -{monto_descuento:,.0f} CLP")
    st.subheader(f"💰 Precio de Venta Final: {total_final:,.0f} CLP")
    
    submit = st.form_submit_button("Guardar Cotización en Drive")

if submit:
    if costo > 0:
        # Obtener datos actuales y agregar la nueva fila
        df = conn.read()
        nueva_fila = pd.DataFrame([{
            "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Producto": producto,
            "Proveedor": proveedor,
            "Costo": int(costo),
            "Subtotal": int(subtotal),
            "Descuento_CLP": int(monto_descuento),
            "Total_Final": int(total_final),
            "Foto": foto_url
        }])
        
        # Combinar y actualizar la hoja completa (más estable)
        updated_df = pd.concat([df, nueva_fila], ignore_index=True)
        conn.update(data=updated_df)
        st.success("¡Cotización guardada exitosamente!")
    else:
        st.error("Por favor, ingresa un costo base válido.")

if st.checkbox("Ver Historial Completo"):
    st.dataframe(conn.read())

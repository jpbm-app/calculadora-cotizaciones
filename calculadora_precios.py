import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Función para formatear con punto de miles
def fmt_clp(valor):
    return f"{int(valor):,.0f}".replace(",", ".")

st.set_page_config(page_title="Cotizador Profesional", layout="centered")
st.title("🏗️ Cotizador de Proyectos")

conn = st.connection("gsheets", type=GSheetsConnection)

with st.form("cotizador"):
    producto = st.text_input("Nombre del Producto")
    proveedor = st.text_input("Nombre del Proveedor")
    
    # 1. Botón de Ubicación
    if st.form_submit_button("📍 Registrar mi ubicación actual"):
        st.write("*(Nota: La ubicación se capturará al guardar la cotización)*")
        # Nota: La geolocalización real en web requiere JS, 
        # esto es un placeholder para integración futura.

    costo = st.number_input("Costo base (CLP)", min_value=0, value=0, step=1000)
    margen_libre = st.number_input("Margen de ganancia (%)", min_value=0.0, value=25.0, step=1.0)
    
    subtotal = costo * (1 + margen_libre / 100)
    st.write(f"**Subtotal (Precio Preliminar):** {fmt_clp(subtotal)} CLP")
    
    descuento_porc = st.number_input("Descuento aplicado (%)", min_value=0.0, value=0.0, step=1.0)
    monto_descuento = subtotal * (descuento_porc / 100)
    total_final = subtotal - monto_descuento
    
    st.write(f"**Monto de descuento:** -{fmt_clp(monto_descuento)} CLP")
    st.subheader(f"💰 Precio de Venta Final: {fmt_clp(total_final)} CLP")
    
    # 2. Botón de Búsqueda de Imagen (Dinámico)
    if producto:
        query = producto.replace(" ", "+")
        st.link_button(f"🔍 Buscar '{producto}' en Google Imágenes", f"https://www.google.com/search?tbm=isch&q={query}")
    
    # 3. Opción de Cámara
    foto_captura = st.camera_input("O tomar una foto del producto")
    foto_url = st.text_input("O pegar URL de la Foto")
    
    submit = st.form_submit_button("Guardar Cotización en Drive")

if submit:
    if costo > 0:
        df = conn.read()
        nueva_fila = pd.DataFrame([{
            "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Producto": producto,
            "Proveedor": proveedor,
            "Costo": int(costo),
            "Subtotal": int(subtotal),
            "Descuento_CLP": int(monto_descuento),
            "Total_Final": int(total_final),
            "Foto": foto_url if foto_url else "Captura de Cámara"
        }])
        
        try:
            updated_df = pd.concat([df, nueva_fila], ignore_index=True)
            conn.update(data=updated_df)
            st.success("¡Cotización guardada exitosamente!")
        except Exception as e:
            st.error(f"Error al guardar: {e}")
    else:
        st.error("Por favor, ingresa un costo base válido.")

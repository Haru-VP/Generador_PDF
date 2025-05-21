import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.units import cm
import tempfile
import os

# Título de la app
st.set_page_config(page_title="Generador de Presupuestos", layout="centered")
st.title("Generador de Presupuestos de Consultoría")

# Formulario
with st.form("form_presupuesto"):
    descripcion = st.text_input("🔹 Descripción del proyecto")
    horas = st.number_input("🔹 Horas estimadas", min_value=1, step=1)
    valor_hora = st.number_input("🔹 Valor por hora (USD$)", min_value=1, step=1)
    tiempo = st.text_input("🔹 Tiempo de entrega (estimado)")
    logo = st.file_uploader("🔹 Subir logo (opcional)", type=["png", "jpg", "jpeg"])
    generar = st.form_submit_button("📄 Generar PDF")

# Al presionar generar
if generar:
    valor_total = horas * valor_hora
    
    # Crear archivo temporal para el PDF
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    c = canvas.Canvas(temp.name, pagesize=A4)
    width, height = A4

    # Colores y estilos
    color_principal = HexColor("#00A5B9")
    color_texto = HexColor("#212121")
    gris_claro = HexColor("#F5F5F5")

   # ENCABEZADO con fondo y bordes redondeados
    encabezado_altura = 4.5*cm  # más alto
    c.setFillColor(color_principal)
    c.roundRect(0.5*cm, height - encabezado_altura - 0.5*cm, width - 1*cm, encabezado_altura, 15, stroke=0, fill=1)

    # Título dentro del encabezado
    c.setFont("Helvetica-Bold", 22)
    c.setFillColor("white")
    c.drawCentredString(width / 2, height - 2.9*cm, "Presupuesto de Consultoría")

    # Logo dentro del encabezado
    if logo is not None:
        logo_bytes = logo.read()
        temp_logo = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        temp_logo.write(logo_bytes)
        temp_logo.close()

        logo_width = 3.5*cm
        logo_height = 3*cm
        logo_x = width - logo_width - 1.5*cm  # margen derecho
        logo_y = height - encabezado_altura + (encabezado_altura - logo_height) / 2 - 0.5*cm  # centrado vertical con ajuste

        c.drawImage(temp_logo.name, logo_x, logo_y, width=logo_width, height=logo_height, preserveAspectRatio=True, mask='auto')


    # Pasos incluidos
    c.setFillColor(color_principal)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2*cm, height - 8*cm, "Pasos incluidos:") #distancia entre encabezado y pasos

    c.setFont("Helvetica", 11)
    c.setFillColor(color_texto)
    pasos = [
        "- Recopilación de requisitos",
        "- Reuniones semanales de seguimiento",
        "- Presentación del prototipo",
        "- Pruebas con clientes"
    ]
    y = height - 9*cm #distancia entre "Pasos incluidos" y viñetas
    for paso in pasos:
        c.drawString(2.5*cm, y, paso)
        y -= 0.6*cm

    # Detalles del presupuesto
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(color_principal)
    c.drawString(2*cm, y - 1*cm, "Detalle del presupuesto")

    detalles = [
        ("Descripción del proyecto:", descripcion),
        ("Horas estimadas:", str(horas)),
        ("Valor de la hora trabajada (USD):", f"{valor_hora}"),
        ("Tiempo de entrega (estimado):", tiempo),
        ("TOTAL (USD$):", f"${valor_total}")
    ]

    c.setFont("Helvetica", 11)
    y -= 2*cm
    for campo, valor in detalles:
        c.setFillColor(gris_claro)
        c.roundRect(2*cm, y - 0.3*cm, 16*cm, 0.8*cm, 5, stroke=0, fill=1)
        c.setFillColor(color_texto)
        c.drawString(2.2*cm, y, campo)
        c.drawString(11*cm, y, valor)
        y -= 1*cm

    c.setFont("Helvetica-Oblique", 9)
    c.setFillColor(HexColor("#888888"))
    c.drawString(2*cm, 1.5*cm, "Esta cotización es válida por 10 días.")
    
    # PIE DE PÁGINA decorativo
    pie_altura = 2*cm
    c.setFillColor(color_principal)
    c.roundRect(0.5*cm, 0.5*cm, width - 1*cm, pie_altura, 15, stroke=0, fill=1)

    # Texto del pie
    c.setFont("Helvetica", 9)
    c.setFillColor("white")
    c.drawCentredString(width / 2, 1.4*cm, "Generado automáticamente - válido por 10 días")

    c.save()

    # Mostrar botón de descarga
    with open(temp.name, "rb") as f:
        st.success("✅ Presupuesto generado exitosamente")
        st.download_button(
            label="📥 Descargar presupuesto PDF",
            data=f,
            file_name="Presupuesto.pdf",
            mime="application/pdf"
        )

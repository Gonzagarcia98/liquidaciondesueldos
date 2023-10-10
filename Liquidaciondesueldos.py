import reportlab as RL
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import streamlit as st

#Titulo y subtitulo
st.title('Calculadora de sueldos CAME')
st.header('Calculadora de aportes y cargas sociales para empresas')

#Input inicial
st.text_input('Enter some text')
Sueldo_bruto = float(input())

#Monto inicial
#Aportes empleado 
#Definimos variables y calculos
Aporte_jubilatorio = (0.11*Sueldo_bruto)
Obra_social = (0.06*Sueldo_bruto)
Pami = (0.03*Sueldo_bruto)
FAECyS = (0.005*Sueldo_bruto)
Sindicato = (0.02*Sueldo_bruto)

#Calculamos el sueldo neto luego de aportes
Sueldo_neto = Sueldo_bruto-(Aporte_jubilatorio+Obra_social+Pami+FAECyS+Sindicato)

#Cargas sociales empleador
#Definimos variables y calculos
Jubilacion = 0.16*Sueldo_bruto
Obra_social_empleador = 0.03*Sueldo_bruto
Pami_empleador = 0.019*Sueldo_bruto
Anses = 0.047*Sueldo_bruto
Fne = 0.0094*Sueldo_bruto
Seguro_vida = 0.003*Sueldo_bruto

#Calculamos el total de cargas sociales
Cargas_sociales = Jubilacion+Obra_social_empleador+Pami_empleador+Anses+Fne+Seguro_vida
Cargas_sociales


lista_variables = [Aporte_jubilatorio, Obra_social,Pami,FAECyS,Sindicato,Jubilacion,Obra_social_empleador,Pami_empleador,Anses,Fne,Seguro_vida,Cargas_sociales,Sueldo_neto]
for i in range (len(lista_variables)) :
    lista_variables[i] = '{:,.2f}'.format(lista_variables[i]).replace(',', ' ')
    lista_variables[i] = lista_variables[i].replace(".",",")
    lista_variables[i] = lista_variables[i].replace(" ",".")
print(f"El sueldo neto a cobrar luego del descuento de los aportes es de: ${lista_variables[12]}")
print(f"Los aportes que realiza el empleador en concepto de cargas sociales son de: ${lista_variables[11]}")


pdf_filename = "Liquidación de sueldos 2.pdf"
c = canvas.Canvas(pdf_filename, pagesize=letter)
texto = f"Los aportes que realiza el empleador en concepto de cargas sociales son de: ${lista_variables[11]}"
texto2 = f"El sueldo neto a cobrar luego del descuento de los aportes es de: ${lista_variables[12]}"
c.drawString(90, 750, texto)
c.drawString(90, 700, texto2)
# Agregar una imagen al PDF
imagen_filename = r"Z:\- LOGOS\CAME\CAME_alta.jpg"  # Reemplaza con el nombre de tu imagen
c.drawImage(imagen_filename, 100, 500, width=200, height=100)
c.save()
print(f"Se ha creado el archivo PDF: {pdf_filename}")
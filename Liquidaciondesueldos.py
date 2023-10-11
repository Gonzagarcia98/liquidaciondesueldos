import reportlab as RL
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import streamlit as st

#TITULO
st.markdown("<h1 style='text-align: center; font-size: 54px; font-family: Verdana, sans-serif;'>Calculadora Sueldos</h1>", unsafe_allow_html=True)
st.write("---")


#IMAGEENES
col1, col2, col3 = st.columns([0.5,3,0.5])
with col1 :
    st.write("")
with col2 : 
    st.image("imgs/logos_came_recortados.png",use_column_width=True)
with col3 :
    st.write("")
st.write("---")

#INPUT INICIAL
Sueldo_bruto = st.text_input('Indique el sueldo bruto', value="$")
Sueldo_bruto = Sueldo_bruto.strip()
Sueldo_bruto = Sueldo_bruto.replace("$", "").replace(".","").replace(",,",",").replace(",",".")

#MANEJO DE ERRORES DEL INPUT
if Sueldo_bruto == "" or Sueldo_bruto == "$" or Sueldo_bruto == " " : 
    aux3 = False 
elif Sueldo_bruto == "0":
    aux3 = False
    st.markdown("<span style='color: red;'>Ingrese un monto válido porfavor.</span>", unsafe_allow_html=True)
else:
    try:
        Sueldo_bruto = float(Sueldo_bruto)
        aux3 = True
    except ValueError:
        aux3 = False        
        st.markdown("<span style='color: red;'>Ingrese un monto válido porfavor.</span>", unsafe_allow_html=True)
st.write("---")

#SELECCIONAMOS EMPLEADO O EMPLEADOR
opcion_seleccionada = st.radio("***Usted es/será***", ["Empleado", "Empleador"], horizontal=True)
if opcion_seleccionada == "Empleado":
    st.write("Seleccionaste Empleado")
elif opcion_seleccionada == "Empleador":
    st.write("Seleccionaste Empleador")
else:
    st.write("No seleccionaste ninguna opción")

#DEFINIMOS VARIABLES Y CALCULOS
#APORTES EMPLEADO
if st.button("Calcular"):
    if aux3 == True:

        Aporte_jubilatorio = (0.11*Sueldo_bruto)
        Obra_social = (0.06*Sueldo_bruto)
        Pami = (0.03*Sueldo_bruto)
        FAECyS = (0.005*Sueldo_bruto)
        Sindicato = (0.02*Sueldo_bruto)
#CALCULAMOS EL NETO LUEGO DE APORTES
        Sueldo_neto = Sueldo_bruto-(Aporte_jubilatorio+Obra_social+Pami+FAECyS+Sindicato)

#CARGAS SOCIALES DEL EMPLEADOR
#DEFINIMOS VARIABLES DEL EMPLEADOR
        Jubilacion = 0.16*Sueldo_bruto
        Obra_social_empleador = 0.03*Sueldo_bruto
        Pami_empleador = 0.019*Sueldo_bruto
        Anses = 0.047*Sueldo_bruto
        Fne = 0.0094*Sueldo_bruto
        Seguro_vida = 0.003*Sueldo_bruto

#CALCULAMOS EL TOTAL DE CARGAS SOCIALES
        Cargas_sociales = Jubilacion+Obra_social_empleador+Pami_empleador+Anses+Fne+Seguro_vida
        Cargas_sociales

#REEEMPLAZAMS LOS . DE LOS MILES
        lista_variables = [Aporte_jubilatorio, Obra_social,Pami,FAECyS,Sindicato,Jubilacion,Obra_social_empleador,Pami_empleador,Anses,Fne,Seguro_vida,Cargas_sociales,Sueldo_neto]
        for i in range (len(lista_variables)) :
            lista_variables[i] = '{:,.2f}'.format(lista_variables[i]).replace(',', ' ')
            lista_variables[i] = lista_variables[i].replace(".",",")
            lista_variables[i] = lista_variables[i].replace(" ",".")
        print(f"El sueldo neto a cobrar luego del descuento de los aportes es de: ${lista_variables[12]}")
        print(f"Los aportes que realiza el empleador en concepto de cargas sociales son de: ${lista_variables[11]}")

#DESCARGAMOS EL PDF
        pdf_filename = "Liquidación de sueldos 2.pdf"
        c = canvas.Canvas(pdf_filename, pagesize=letter)
        texto = f"Los aportes que realiza el empleador en concepto de cargas sociales son de: ${lista_variables[11]}"
        texto2 = f"El sueldo neto a cobrar luego del descuento de los aportes es de: ${lista_variables[12]}"
        c.drawString(90, 750, texto)
        c.drawString(90, 700, texto2)
        # Agregar una imagen al PDF
        imagen_filename = r"imgs/logos_came_recortados.png"  # Reemplaza con el nombre de tu imagen
        c.drawImage(imagen_filename, 100, 500, width=200, height=100)
        c.save()
        print(f"Se ha creado el archivo PDF: {pdf_filename}")
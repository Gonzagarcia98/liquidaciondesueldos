import reportlab as RL
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import streamlit as st
import io
from io import BytesIO

#TITULO
st.markdown("<h1 style='text-align: center; font-size: 54px; font-family: Verdana, sans-serif;'>Calculadora Sueldos</h1>", unsafe_allow_html=True)
st.write("---")

#IMAGENES
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
opcion_seleccionada = st.radio("# **Usted es/será**", ["Empleado", "Empleador"], horizontal=True)
st.write("---")

#DEFINIMOS VARIABLES Y CALCULOS
#APORTES EMPLEADO
colA, colB= st.columns(2)
aux1 = False
aux2 = False
with colA:
    if st.button("Calcular"):
        if aux3 == True:
            if opcion_seleccionada == "Empleado":   
                #APORTES EMPLEADO
                #PRIMER CALCULO - APORTE JUBILATORIO
                Aporte_jubilatorio = (0.11*Sueldo_bruto)
                #SEGUNDO CALCULO - OBRA SOCIAL
                Obra_social = (0.03*Sueldo_bruto)
                #TERCER CALCULO - PAMI
                Pami = (0.03*Sueldo_bruto)
                #CUARTO CALCULO - FAECYS
                FAECyS = (0.005*Sueldo_bruto)
                #QUINTO CALCULO - SINDICATO
                Sindicato = (0.02*Sueldo_bruto)
                #SEXTO CALCULO - SUELDO NETO
                Sueldo_neto = Sueldo_bruto-(Aporte_jubilatorio+Obra_social+Pami+FAECyS+Sindicato)
                #REEEMPLAZAMS LOS . DE LOS MILES EMPLEADO
                lista_variables = [Aporte_jubilatorio, Obra_social, Pami,FAECyS, Sindicato, Sueldo_neto, Sueldo_bruto]
                for i in range (len(lista_variables)) :
                    lista_variables[i] = '{:,.2f}'.format(lista_variables[i]).replace(',', ' ')
                    lista_variables[i] = lista_variables[i].replace(".",",")
                    lista_variables[i] = lista_variables[i].replace(" ",".")
                aux1 = True
        
                pdf_buffer = BytesIO()
                # Generar el PDF
                c = canvas.Canvas(pdf_buffer, pagesize=letter)
                pdf_filename = "Aportes - Empleado.pdf"
                texto2 = f"El sueldo neto a cobrar luego del descuento de los aportes es de: ${lista_variables[5]}"
                c.drawString(90, 700, texto2)
                # Agregar una imagen al PDF
                imagen_filename = r"imgs/logos_came_recortados.png"  # Reemplaza con el nombre de tu imagen
                c.drawImage(imagen_filename, 100, 500, width=200, height=100)
                c.save()
                print(f"Se ha creado el archivo PDF: {pdf_filename}")
                pdf_buffer.seek(0)
                st.download_button("Descargar PDF", pdf_buffer, file_name=pdf_filename)
    
            elif opcion_seleccionada == "Empleador":
            #CARGAS SOCIALES DEL EMPLEADOR
            #SEPTIMO CALCULO - JUBILACIÓN EMPLEADOR
                Jubilacion = (0.16*Sueldo_bruto)
                #OCTAVO CALCULO - OBRA SOCIAL EMPLEADOR
                Obra_social_empleador = (0.06*Sueldo_bruto)
                #NOVENO CALCULO - PAMI EMPLEADOR
                Pami_empleador = (0.019*Sueldo_bruto)
                #DECIMO CALCULO - ANSES
                Anses = (0.047*Sueldo_bruto)
                #DECIMOPRIMER CALCULO - FNE
                Fne = (0.0094*Sueldo_bruto)
                #DECIMOSEGUNDO CALCULO - SEGURO DE VIDA
                Seguro_vida = (0.003*Sueldo_bruto)
                #DECIMOCUARTO CALCULO - TOTAL DE CARGAS SOCIALES
                Cargas_sociales = Jubilacion+Obra_social_empleador+Pami_empleador+Anses+Fne+Seguro_vida

                #REEEMPLAZAMS LOS . DE LOS MILES EMPLEADOR
                lista_variables = [Jubilacion, Obra_social_empleador, Pami_empleador, Anses, Fne, Seguro_vida,Cargas_sociales]
                for i in range (len(lista_variables)) :
                        lista_variables[i] = '{:,.2f}'.format(lista_variables[i]).replace(',', ' ')
                        lista_variables[i] = lista_variables[i].replace(".",",")
                        lista_variables[i] = lista_variables[i].replace(" ",".")
                aux2 = True
                        
                pdf_buffer = BytesIO()
                # Generar el PDF
                c = canvas.Canvas(pdf_buffer, pagesize=letter)
                pdf_filename = "Cargas Sociales - Empleador.pdf"
                texto = f"Los aportes que realiza el empleador en concepto de cargas sociales son de: ${lista_variables[6]}"
                c.drawString(90, 750, texto)
                # Agregar una imagen al PDF
                imagen_filename = r"imgs/logos_came_recortados.png"  # Reemplaza con el nombre de tu imagen
                c.drawImage(imagen_filename, 100, 500, width=200, height=100)
                c.save()
                print(f"Se ha creado el archivo PDF: {pdf_filename}")
                pdf_buffer.seek(0)
                st.download_button("Descargar PDF", pdf_buffer, file_name=pdf_filename)
with colB:
            custom_css = """
        <style>
            .tarjeta {
                text-align: left;
            }
            .subheader {
                font-size: 20px;
                font-weight: bold;
            }
        </style>
        """
        # Agregar el estilo CSS personalizado utilizando st.markdown      
            if aux1 == True :
                st.markdown(custom_css, unsafe_allow_html=True)
                tarjeta = f'<div class="tarjeta" style="font-size: 45px;font-weight: bold; ">${lista_variables[5]}</div>'
                st.markdown('<div class="subheader">El sueldo neto es:</div>', unsafe_allow_html=True)
                st.markdown(tarjeta, unsafe_allow_html=True)
                st.markdown('</div></div>', unsafe_allow_html=True)
                #st.write(f"El precio sugerido es:")
                #st.write(f"# $**{monto_final}**")
            else:
                st.write("")   
                 
            if aux2 == True :
                st.markdown(custom_css, unsafe_allow_html=True)
                tarjeta = f'<div class="tarjeta" style="font-size: 45px;font-weight: bold; ">${lista_variables[6]}</div>'
                st.markdown('<div class="subheader">El total de cargas sociales será:</div>', unsafe_allow_html=True)
                st.markdown(tarjeta, unsafe_allow_html=True)
                st.markdown('</div></div>', unsafe_allow_html=True)
                #st.write(f"El precio sugerido es:")
                #st.write(f"# $**{monto_final}**")
            else:
                st.write("") 
if aux1 == True:      
        st.write("***DETALLE DE DESCUENTOS***")
        st.write(f"**Aporte jubilatorio:** ${lista_variables[0]}")
        st.write(f"**Obra social:** ${lista_variables[1]}")
        st.write(f"**Pami:** ${lista_variables[2]}")
        st.write(F"**Faecys:** ${lista_variables[3]}")
        st.write(f"**Sindicato:** ${lista_variables[4]}")    

if aux2 == True:      
        st.write("***DETALLE DE CARGAS SOCIALES***")
        st.write(f"**Jubilación:** ${lista_variables[0]}")
        st.write(f"**Obra social:** ${lista_variables[1]}")
        st.write(f"**Pami:** ${lista_variables[2]}")
        st.write(F"**Anses:** ${lista_variables[3]}")
        st.write(F"**FNE:** ${lista_variables[4]}")
        st.write(F"**Seguro de vida:** ${lista_variables[5]}") 

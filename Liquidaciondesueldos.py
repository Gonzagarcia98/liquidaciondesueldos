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

#DEFINIMOS VARIABLES Y CALCULOS
#APORTES EMPLEADO
aux1 = False
colA, colB, colAA= st.columns([0.5, 0.3, 1.5])
with colA:
    if st.button("Calcular", use_container_width = True):
        if aux3 == True: 
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
                #CALCULO DEL TOTAL DE APORTES  - SIN NUMERO
                total_aportes = (Aporte_jubilatorio+Obra_social+Pami+FAECyS+Sindicato)
                #SEXTO CALCULO - SUELDO NETO
                Sueldo_neto = Sueldo_bruto-total_aportes
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
                aux1 = True
                #REEEMPLAZAMS LOS . DE LOS MILES EMPLEADOR
                lista_variables = [Jubilacion, Obra_social_empleador, Pami_empleador, Anses, Fne, Seguro_vida,Cargas_sociales, Aporte_jubilatorio, Obra_social, Pami,FAECyS, Sindicato, Sueldo_neto, Sueldo_bruto, total_aportes]
                for i in range (len(lista_variables)) :
                        lista_variables[i] = '{:,.2f}'.format(lista_variables[i]).replace(',', ' ')
                        lista_variables[i] = lista_variables[i].replace(".",",")
                        lista_variables[i] = lista_variables[i].replace(" ",".")
                pdf_buffer = BytesIO()


                # Generar el PDF
                c = canvas.Canvas(pdf_buffer, pagesize=letter)
                pdf_filename = "Cargas Sociales - Empleador.pdf"
                texto = f"Las cargas sociales que paga el empleador por un empleado son de: ${lista_variables[6]}"
                texto = f"Los aportes que realiza el empleado son de: ${lista_variables[14]}"
                c.drawString(90, 750, texto)


                # Agregar una imagen al PDF
                imagen_filename = r"imgs/logos_came_recortados.png"  # Reemplaza con el nombre de tu imagen
                c.drawImage(imagen_filename, 100, 500, width=200, height=100)
                c.save()
                print(f"Se ha creado el archivo PDF: {pdf_filename}")
                pdf_buffer.seek(0)
                st.download_button("Descargar PDF", pdf_buffer, file_name=pdf_filename,use_container_width = True)
with colB:
    st.write("")
with colAA:
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
                tarjeta = f'<div class="tarjeta" style="font-size: 45px;font-weight: bold; ">${lista_variables[12]}</div>'
                st.markdown('<div class="subheader">El sueldo neto es:</div>', unsafe_allow_html=True)
                st.markdown(tarjeta, unsafe_allow_html=True)
                st.markdown('</div></div>', unsafe_allow_html=True)
                st.markdown(custom_css, unsafe_allow_html=True)
                tarjeta = f'<div class="tarjeta" style="font-size: 45px;font-weight: bold; ">${lista_variables[6]}</div>'
                st.markdown('<div class="subheader">El total de cargas sociales es:</div>', unsafe_allow_html=True)
                st.markdown(tarjeta, unsafe_allow_html=True)
                st.markdown('</div></div>', unsafe_allow_html=True)
                #st.write(f"El precio sugerido es:")
                #st.write(f"# $**{monto_final}**")
            else:
                st.write("")
st.write("---")
colC, colD, colE, colF= st.columns([0.3,4,4,0.3])
with colC:
    if aux1 ==True:
        st.write("")
with colD:       
    if aux1 == True:      
        st.write("***DETALLE DE DESCUENTOS***")
        st.write(f"**Aporte jubilatorio (11%):** ${lista_variables[0]}")
        st.write(f"**Obra social (3%):** ${lista_variables[1]}")
        st.write(f"**Pami (3%):** ${lista_variables[2]}")
        st.write(F"**Faecys (0,5%):** ${lista_variables[3]}")
        st.write(f"**Sindicato (2%):** ${lista_variables[4]}") 
with colE:
    if aux1 == True:
        st.write("***DETALLE DE CARGAS SOCIALES***")
        st.write(f"**Jubilación (16%):** ${lista_variables[0]}")
        st.write(f"**Obra social (6%):** ${lista_variables[1]}")
        st.write(f"**Pami (1,9%):** ${lista_variables[2]}")
        st.write(F"**Anses (4,7%):** ${lista_variables[3]}")
        st.write(F"**FNE (0,3%):** ${lista_variables[4]}")
        st.write(F"**Seguro de vida (0,3%):** ${lista_variables[5]}") 
with colF:
    if aux1 == True:      
        st.write("")

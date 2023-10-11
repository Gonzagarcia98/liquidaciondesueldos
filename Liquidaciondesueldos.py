import reportlab as RL
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import streamlit as st
import io
from io import BytesIO
import pytz
import datetime

#TITULO
st.markdown("<h1 style='text-align: center; font-size: 54px; font-family: Verdana, sans-serif;'>Liquidador de sueldos</h1>", unsafe_allow_html=True)
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
                 # Nombre del archivo PDF
        pdf_filename = "Liquidación de sueldo.pdf"

            # Crear un objeto BytesIO para guardar el PDF en memoria
        pdf_buffer = BytesIO()
            # Generar el PDF
        c = canvas.Canvas(pdf_buffer, pagesize=letter)

        # Establecer la zona horaria a Buenos Aires
        zona_horaria = pytz.timezone('America/Argentina/Buenos_Aires')

        # Obtener la fecha y hora actual en la zona horaria especificada
        fecha_hora_actual = datetime.datetime.now(zona_horaria)

        # Obtener la fecha en formato dd/mm/aa
        fecha_actual = fecha_hora_actual.strftime("%d/%m/%y")

        # Obtener la hora en formato hh:mm:ss
        hora_actual = fecha_hora_actual.strftime("%H:%M:%S")

        # Escribimos la fecha actual 
        c.setFont("Helvetica", 10)
        c.drawString(40, 760, f"{fecha_actual} - {hora_actual}")

        # Agregar título
        c.setFont("Helvetica-Bold", 32)
        titulo = "Calculadora Ahora 12"
        titulo_width = c.stringWidth(titulo, "Helvetica-Bold", 32)
        titulo_x = (letter[0] - titulo_width) / 2  # Centrar el título horizontalmente
        c.drawString(titulo_x, 720, titulo)

        # Coordenadas y dimensiones de la imagen
        imagen_path = "imgs/logos_came_con_fondo y recortados2.png"  # Reemplaza 'tu_imagen.png' con la ruta de tu propia imagen
        imagen_width = 300  # Ancho de la imagen
        imagen_height = 50  # Altura de la imagen
        imagen_x = (letter[0] - imagen_width) / 2  # Centrar la imagen horizontalmente
        imagen_y = 660  # Espacio entre el título y la imagen

        c.drawImage(imagen_path, imagen_x, imagen_y, width=imagen_width, height=imagen_height)

        # Coordenadas y dimensiones del rectángulo
        rect_width = 400  # Ancho del rectángulo
        rect_height = 50  # Altura del rectángulo
        rect_x = (letter[0] - rect_width) / 2  # Centrar el rectángulo horizontalmente
        rect_y = 580 # Espacio entre la imagen y el rectángulo

        c.rect(rect_x, rect_y, rect_width, rect_height)

        # Texto que quieres agregar dentro del rectángulo
        c.setFont("Helvetica-Bold", 20)
        texto = f"Precio sugerido: ${lista_variables[1]}"

        # Alinear el texto en el centro del rectángulo
        text_width = c.stringWidth(texto, "Helvetica-Bold", 20)
        text_x = rect_x + (rect_width - text_width) / 2
        text_y = rect_y + (rect_height - 20) / 2  # Alinear verticalmente en el centro

        # Agregar texto dentro del rectángulo
        c.drawString(text_x, text_y, texto)
        
        # ACLARACIÓN 
        c.setFont("Helvetica-Bold", 10)
        c.drawString(90, 555, "ACLARACIÓN")
        c.setFont("Helvetica", 9)
        c.drawString(90, 545, "El usuario reconoce y acepta que los datos generados son a título meramente informativo y orientativo.") 
        c.drawString(90, 535, "La herramienta no apunta a establecer precios finales para ninguna operación sino brindar, de manera detallada,")
        c.drawString(90, 525, "la información que un comercio puede necesitar para definir, por decisión propia,") 
        c.drawString(90, 515, "los precios de los productos y servicios que comercializa a través de las promociones del programa Ahora.")
        c.drawString(90, 505, "Asimismo, CAME no se responsabiliza por la información brindada por el sistema, su actualización o su falta de disponibilidad.")  
        
        # Agrega una línea separadora
        line_x1, line_y1 = 100, 210
        line_x2, line_y2 = 520, 210
        # linea
        c.line(line_x1, line_y1, line_x2, line_y2)

        # TABLA 1
        x1, y1 = 90, 470  # Esquina superior izquierda
        x2, y2 = 400, 230  # Esquina inferior derecha
        
        # Dibuja el cuadrado
        c.rect(x1, y1, x2 - x1, y2 - y1)
        
        # Establece la fuente y agrega tus cadenas de texto
        c.setFont("Helvetica", 12)
        # Coordenada x para las categorías
        category_x = x1 + 10
        # Coordenada x para los valores (contra el margen derecho)
        value_x = x2 - 10
        # Espaciado vertical entre las líneas
        line_spacing = 20
            
        c.setFont("Helvetica-Bold", 14)
        c.drawString(90, 480, "Liquidación de pago")   
        # Agrega las categorías y valores
        c.setFont("Helvetica", 12)    
        categories = [
            "Venta a precio de contado:",
            f"Financiado en {programa_seleccionado}:",
            "Provincia:",
            "AFIP:",
            "Arancel 1,8%:",
            f"Costo Financiero del programa ({tasas_a_STR}):",
            "IVA Arancel (21%):",
            "IVA Costo Financiero (10,50%):",
            "Subtotal",
            "IVA RG 140/98 (3%)",
            "Total Cobrado en la liquidación"  
        ]
        
        values = [
            f"${lista_variables[0]}",
            f"${lista_variables[1]}",
            provincia_seleccionada,
            tipo_inscripcion,
            f"${lista_variables[2]}",
            f"${lista_variables[3]}",
            f"${lista_variables[4]}",
            f"${lista_variables[5]}",
            f"${lista_variables[6]}",
            f"${lista_variables[7]}",
            f"${lista_variables[8]}"    
        ]
        
        # Índices de los valores que deseas en negrita
        bold_indices = [8,10]
        
        for i in range(len(categories)):
            category = categories[i]
            value = values[i]
        
            # Utiliza la fuente en negrita para los valores específicos
            if i in bold_indices:
                c.setFont("Helvetica-Bold", 12)
            else:
                c.setFont("Helvetica", 12)
        
            # Dibuja la categoría y el valor
            c.drawString(category_x, 450 - i * line_spacing, category)
            c.drawString(value_x - c.stringWidth(value, "Helvetica-Bold" if i in bold_indices else "Helvetica", 12), 450 - i * line_spacing, value)

        # TABLA 2


            # TABLA 1
        x1, y1 = 90, 180  # Esquina superior izquierda
        x2, y2 = 400, 10  # Esquina inferior derecha
        
        # Dibuja el cuadrado
        c.rect(x1, y1, x2 - x1, y2 - y1)
        
        # Establece la fuente y agrega tus cadenas de texto
        c.setFont("Helvetica", 12)
        # Coordenada x para las categorías
        category_x = x1 + 10
        # Coordenada x para los valores (contra el margen derecho)
        value_x = x2 - 10
        # Espaciado vertical entre las líneas
        line_spacing = 20
            
        c.setFont("Helvetica-Bold", 14)
        c.drawString(90, 190, f"Cálculo de impuestos")
        # Agrega las categorías y valores
        c.setFont("Helvetica", 12)    
        categories = [
            "Venta neta IVA",
            "IVA Débito",
            "IVA Crédito",
            "Posición IVA",
            "Saldo cobrado",
            "Tasa Municipal (1%)",
            "IIBB",
            "Utilidad Antes de Costos e IIGG"  
        ]
        
        values = [
            f"${lista_variables[9]}",
            f"${lista_variables[10]}",
            f"${lista_variables[11]}",
            f"${lista_variables[12]}",
            f"${lista_variables[13]}",
            f"${lista_variables[14]}",
            f"${lista_variables[15]}", 
            f"${lista_variables[16]}"    
        ]
        
        # Índices de los valores que deseas en negrita
        bold_indices = [3,7]
        
        for i in range(len(categories)):
            category = categories[i]
            value = values[i]
        
            # Utiliza la fuente en negrita para los valores específicos
            if i in bold_indices:
                c.setFont("Helvetica-Bold", 12)
            else:
                c.setFont("Helvetica", 12)
        
            # Dibuja la categoría y el valor
            c.drawString(category_x, 160 - i * line_spacing, category)
            c.drawString(value_x - c.stringWidth(value, "Helvetica-Bold" if i in bold_indices else "Helvetica", 12), 160 - i * line_spacing, value)
            


        # Guardar y cerrar el PDF
        c.save()
        pdf_buffer.seek(0)
        st.download_button("Descargar PDF", pdf_buffer, file_name="Resumen precio sugerido.pdf")
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
colC, colD, colE, colF= st.columns([0.5,4,4,0.3])
with colC:
    if aux1 ==True:
        st.write("")
with colD:       
    if aux1 == True:  
        st.info("***DETALLE DE DESCUENTOS***")
        st.write(f"**Aporte jubilatorio (11%):** ${lista_variables[0]}")
        st.write(f"**Obra social (3%):** ${lista_variables[1]}")
        st.write(f"**Pami (3%):** ${lista_variables[2]}")
        st.write(F"**Faecys (0,5%):** ${lista_variables[3]}")
        st.write(f"**Sindicato (2%):** ${lista_variables[4]}") 
with colE:
    if aux1 == True:
        st.info("***DETALLE DE APORTES***")
        st.write(f"**Jubilación (16%):** ${lista_variables[0]}")
        st.write(f"**Obra social (6%):** ${lista_variables[1]}")
        st.write(f"**Pami (1,9%):** ${lista_variables[2]}")
        st.write(F"**Anses (4,7%):** ${lista_variables[3]}")
        st.write(F"**FNE (0,3%):** ${lista_variables[4]}")
        st.write(F"**Seguro de vida (0,3%):** ${lista_variables[5]}") 
with colF:
    if aux1 == True:      
        st.write("")

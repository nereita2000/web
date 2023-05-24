from fastapi import FastAPI
from fastapi import Request
import mysql.connector
import smtplib
import configparser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = FastAPI()


@app.post("/guardar")
async def guardar(request: Request):
    # Obtener los datos del formulario
    form_data = await request.form()
    nombre = form_data["nombre"]
    email = form_data["email"]
    telefono = form_data["telefono"]
    fecha = form_data["fecha"]
    hora = form_data["hora"]
    personas = form_data["personas"]
    campus = form_data["campus"]
    
    #Leemos configuracion

    config = configparser.ConfigParser()

    config.read('/code/app.env')



    #Tomamos los valores del fichero de variables
    nombre2 = config.get('DB', 'DBNAME')
    contra = config.get('DB', 'PWDROOTDB')
    rt = config.get('DB', 'ROOTDB')
    usuario = config.get('DB','USERDB')
    mail = config.get('MAIL','ip')

    # Conexión a la base de datos
    conn = mysql.connector.connect(
        host="database",  # generalmente es 'localhost'
        database=nombre2,
        user=usuario,
        password=rt
    )
    cursor = conn.cursor()

    # Insertar los datos en la base de datos
    query = "INSERT INTO reservas (nombre, correo, telefono, fecha_reserva, hora_reserva, cantidad_personas, campus_reserva) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (nombre,email,telefono,fecha,hora,personas,campus))

    # Guardar los cambios y cerrar la conexión
    conn.commit()
    cursor.close()
    conn.close()
    #Enviamos correo de confirmación
    # Configuración del servidor SMTP y del correo electrónico
    smtp_server = mail
    smtp_port = 1025
    origen = 'restaurante@urjc.es'
    destinatario = email
    asunto = 'Reserva'

    # Creación del mensaje
    mensaje = MIMEMultipart()
    mensaje['From'] = origen
    mensaje['To'] = destinatario
    mensaje['Subject'] = asunto

    # Agregar el cuerpo del mensaje
    cuerpo_mensaje = 'Estimado usuario,\n\nSu reserva ha sido confirmada.'
    mensaje.attach(MIMEText(cuerpo_mensaje, 'plain'))

    # Envío del correo electrónico
    with smtplib.SMTP(smtp_server, smtp_port) as servidor:
        servidor.sendmail(origen, destinatario, mensaje.as_string())

    print('El correo ha sido enviado correctamente.')



    return {"message": "Datos guardados correctamente"}

@app.post("/contactar")
async def guardar(request: Request):
    # Obtener los datos del formulario
    form_data = await request.form()
    nombre = form_data["nombre"]
    email = form_data["email"]
    mensaje2 = form_data["mensaje"]

    
    #Leemos configuracion

    config = configparser.ConfigParser()

    config.read('/code/app.env')

    mail = config.get('MAIL','ip')
    #Enviamos correo de confirmación
    # Configuración del servidor SMTP y del correo electrónico
    smtp_server = mail
    smtp_port = 1025
    origen = email
    destinatario = 'restaurante@urjc.es'
    asunto = 'Contactar'

    # Creación del mensaje
    mensaje = MIMEMultipart()
    mensaje['From'] = origen
    mensaje['To'] = destinatario
    mensaje['Subject'] = asunto

    # Agregar el cuerpo del mensaje
    cuerpo_mensaje = 'Solicita contacto '+ nombre +", \n\n" + mensaje2
    mensaje.attach(MIMEText(cuerpo_mensaje, 'plain'))

    # Envío del correo electrónico
    with smtplib.SMTP(smtp_server, smtp_port) as servidor:
        servidor.sendmail(origen, destinatario, mensaje.as_string())

    print('El correo ha sido enviado correctamente.')


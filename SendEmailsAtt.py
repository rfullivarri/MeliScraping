from ast import Import
from fileinput import filename
import smtplib,ssl
import email
from os.path import basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase



destinatario = 'yourmail@gmail.com'
asunto = 'Prueba con adjunto'
cuerpo = 'si anda esto es una belleza'
archivo = "C:\\Users\\ramferna\\ev\Ramiro Fernandez de Ullivarri\\31. Scrapping\MELIScrapingDemacbook pro m1.xlsx" 


def SendEmailsAtt(destinatario,asunto,cuerpo,archivo):
 #INFO BASICA DEL MAIL REMITENTE  
 servidor= 'smtp.gmail.com'
 puerto= 465
 contexto= ssl.create_default_context()
 email_sender = 'rfullivarri22@gmail.com'
 password = 'yourpassword'
 
 #INFO DE DESTINATARIO, REMITENTE, ASUNTO
 msg = MIMEMultipart()
 msg['From'] = email_sender
 msg['To'] =  destinatario
 msg['Subject'] = asunto

 #CUERPO DEL MAIL + ARCHIVO ADJUNTO
 msg.attach(MIMEText(cuerpo, 'plain'))
 filename= archivo

 #ABRIR EL ARCHIVO EN FORMATO BINARIO
 with open(filename, 'rb') as adjunto:
    part = MIMEBase('application', 'octet_stream')
    part.set_payload(adjunto.read())

 #CODIFICAR EL ASCII PARA PODER ENVIARLO
 encoders.encode_base64(part)
 part.add_header('Content-Disposition', f'attachment;filename={filename}',)
 
 #AÑADIMOS EL MENSAJE Y LO CONVERTIMOS EN CADENA (string)
 msg.attach(part)
 texto= msg.as_string()

 with smtplib.SMTP_SSL(servidor,puerto, context= contexto) as s:
   s.login(email_sender, password)
   s.sendmail(email_sender,destinatario,texto)

#SendEmailsAtt(destinatario,asunto,cuerpo,archivo)

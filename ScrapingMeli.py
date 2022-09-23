from distutils.command.build_ext import build_ext
from turtle import title
from typing import List
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
from SendEmailsAtt import SendEmailsAtt



dfbusqueda=pd.read_excel(r"C:\Users\ramferna\Pictures\ScrappingMeli.xlsx", sheet_name="Hoja1")

Busqueda= dfbusqueda.iat[0,1]
destinatario2= dfbusqueda.iloc[0,2]

def Scraping_Meli():
 Options= webdriver.EdgeOptions()
 Options.add_argument("--start-maximized")
   
 Driver= webdriver.Edge(r"C:\Python\venv\webdriver\msedgedriver.exe" , options=Options)

 Driver.get("https://www.mercadolibre.com.ar/")
 Driver.maximize_window()


 WebDriverWait(Driver, 5)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button.cookie-consent-banner-opt-out__action cookie-consent-banner-opt-out__action--primary cookie-consent-banner-opt-out__action--key-accept".replace(' ', '.'))))\
    .click()
 

 WebDriverWait(Driver, 5)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input#cb1-edit.nav-search-input")))\
    .send_keys(Busqueda) 


 WebDriverWait(Driver, 5)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR,"div.nav-icon-search")))\
    .click()

 WebDriverWait(Driver, 5)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button.onboarding-cp-button.andes-button.andes-button--filled.andes-button--small")))\
    .click()

 time.sleep(2)



 #BUSQUEDAS DE INFO
 Precio= Driver.find_elements(By.XPATH, "//ol[@class='ui-search-layout ui-search-layout--grid']//li[@class='ui-search-layout__item']//a[@class='ui-search-result__content ui-search-link']//div[@class='ui-search-result__content-wrapper shops-custom-secondary-font']//div[@class='ui-search-price__second-line']//span[@class='price-tag-fraction']")
 Moneda= Driver.find_elements(By.XPATH, "//ol[@class='ui-search-layout ui-search-layout--grid']//div[@class='ui-search-price__second-line']//span[@class='price-tag-symbol']")
 Titulo= Driver.find_elements(By.XPATH,"//ol[@class='ui-search-layout ui-search-layout--grid']//li[@class='ui-search-layout__item']//div[@class='ui-search-result__content-wrapper shops-custom-secondary-font']//h2[@class='ui-search-item__title ui-search-item__group__element shops-custom-secondary-font']")
 Links=  Driver.find_elements(By.XPATH,"//li[@class='ui-search-layout__item']//div[@class='ui-search-result__image shops__picturesStyles']//a[1]")

 #GENERAR LISTAS DE LA INFO ALMACENADA
 Precio= [float(price.text.replace(".","")) for price in Precio ]                              #LIST Comprehension (Un for resumido en una sola linea)
 Moneda= [moneda.text for moneda in Moneda ]
 Titulo= [title.text for title in Titulo ]
 Links= [link.get_attribute('href') for link in Links]


 #SI NO ENCUENTRA INFO EN LA PRIMERA INSTANCIA CONTINUA CON EL CONDICIONAL
 if((len(Precio)>0)):
    Precio
 else:
   Precio= Driver.find_elements(By.XPATH, "//ol[@class='ui-search-layout ui-search-layout--stack']//div[@class='ui-search-price__second-line']//span[@class='price-tag-fraction']")
   Precio= [ float(price.text.replace(".","")) for price in Precio ]                         #LIST Comprehension (Un for resumido en una sola linea)


 if((len(Moneda)>0)):
    Moneda
 else:
    Moneda= Driver.find_elements(By.XPATH, "//ol[@class='ui-search-layout ui-search-layout--stack']//div[@class='ui-search-price__second-line']//span[@class='price-tag-symbol']")
    Moneda= [ moneda.text for moneda in Moneda ]                     #LIST Comprehension (Un for resumido en una sola linea)


 if((len(Titulo)>0)):
    Titulo
 else:
    Titulo= Driver.find_elements(By.XPATH,"//ol[@class='ui-search-layout ui-search-layout--stack']//div[@class='ui-search-result__wrapper']//div[@class='ui-search-item__group ui-search-item__group--title shops__items-group']//a[@class='ui-search-item__group__element shops-custom-secondary-font ui-search-link']//h2[@class='ui-search-item__title']")
    Titulo= [title.text for title in Titulo ]                       #LIST Comprehension (Un for resumido en una sola linea)

 print(len(Moneda), len(Precio), len(Links), len(Titulo))


 # #DICCIONARIO DE PRODUCTOS (PREPARAMOS LA DATA PARA GUARDARLA)
 DataScraping= {
    "Nombre_Producto":Titulo,
    "Moneda":Moneda,                                 #Es un DICCIONARIO donde le decimos que queres q contenga y con que nombre
    "Precio":Precio,
    "Links":Links
 }

 #GUARDAR DATAFRAME
 df1= pd.DataFrame(DataScraping)

 #PROCESANDO LA DATA CON PANDAS Y NUMPY

 #df1["Precio"] = int(df1['Precio'])
 df1['En_Dolares']= df1['Precio']/280
 df1['PromP']= df1['Precio'].mean()
 df1['Variacion']= (df1['Precio']/df1['PromP'])-1
 df1= df1.round({'En_Dolares':2, 'PromP':2,'Variacion':2})
 df1= df1.sort_values(by=['Variacion','Precio'],ascending=[1,0])
 df2=df1[['Nombre_Producto','Moneda','Precio','En_Dolares','PromP','Variacion','Links']] 
 
 ##df1= df1.to_excel("MELIScrapingDe"+Busqueda+".xlsx")
 df2= df2.to_excel(r"C:\Users\ramferna\OneDrive - Anheuser-Busch InBev\Ramiro Fernandez de Ullivarri\31. Scrapping"+"\\"+ "Meli Scraping De "+Busqueda+".xlsx")
 
 df3= r"C:\Users\ramferna\OneDrive - Anheuser-Busch InBev\Ramiro Fernandez de Ullivarri\31. Scrapping"+"\\"+ "Meli Scraping De "+Busqueda+".xlsx"

 #Enviar por mail

 asunto2= "Analisis de Precios ML de " + Busqueda
 cuerpo2= """Buenas! como estas? 
    Te Adjunto el Analisis de Precios del Producto que solicisitaste!
    Esperamos que te sirva

    Cualquier cosa no dudes en consultarnos
    Saludos!"""
 SendEmailsAtt(destinatario2,asunto2,cuerpo2,df3)
 
 Driver.quit()


Scraping_Meli()




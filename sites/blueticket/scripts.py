import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

from utils.salvar_print import salvar_print

# Configuração do navegador (modo headless é opcional)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920,1080")
service = Service("C:/chromedriver/chromedriver.exe")  # ajuste conforme necessário

driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    driver.get("https://www.blueticket.com.br/search?q=")

    # Espera até que cards de evento estejam presentes
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "event-card"))
    )

    # Coleta os títulos dos eventos
    event_titles = driver.find_elements(By.CLASS_NAME, "event-title")

    print("\nTítulos dos eventos encontrados:")
    for title in event_titles[:10]:  # limita aos 10 primeiros
        print("-", title.text)


    # 👉 Você pode salvar um print a qualquer momento chamando:
    salvar_print(driver, nome_base="pagina_blueticket")

except Exception as e:
    print("⚠️ Ocorreu um erro:", str(e))
    salvar_print(driver, nome_base="erro")

finally:
    driver.quit()

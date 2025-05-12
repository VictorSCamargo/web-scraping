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
service = Service("C:/chromedriver/chromedriver.exe")  # ajuste conforme necessário

driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    driver.get("https://www.blueticket.com.br")

    # Espera até que algum conteúdo principal seja carregado (ex: lista de eventos)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "h2"))
    )

    # Pega o título da aba (nome do site)
    print("Título da página:", driver.title)

    # Captura alguns textos (ex: títulos, seções, etc.)
    h1_elements = driver.find_elements(By.TAG_NAME, "h1")
    print("\nTextos em <h1>:")
    for h1 in h1_elements:
        print("-", h1.text)

    p_elements = driver.find_elements(By.TAG_NAME, "p")
    print("\nPrimeiros <p>:")
    for p in p_elements[:5]:
        print("-", p.text)

    # 👉 Você pode salvar um print a qualquer momento chamando:
    salvar_print(driver, nome_base="pagina_blueticket")

except Exception as e:
    print("⚠️ Ocorreu um erro:", str(e))
    salvar_print(driver, nome_base="erro")

finally:
    driver.quit()

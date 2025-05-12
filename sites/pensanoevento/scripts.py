import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from utils.salvar_print import salvar_print

# Configuração do ChromeDriver
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920,1080")
service = Service("./chromedriver")

driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    driver.get("https://www.pensanoevento.com.br/")

    # Aguarda o carregamento de eventos
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".card-text"))
    )

    event_cards = driver.find_elements(By.CLASS_NAME, "card-text")

    for card in event_cards:
        try:
            # Extrai o título do evento (link dentro do <a>)
            event_title = card.find_element(By.TAG_NAME, "a").text
            # Extrai o link do evento (href do <a>)
            event_link = card.find_element(By.TAG_NAME, "a").get_attribute("href")
            # Extrai o local do evento (informação dentro do <span>)
            event_location = card.find_element(By.TAG_NAME, "span").text

            # Exibe as informações do evento
            print(f"Evento: {event_title}")
            print(f"Link: {event_link}")
            print(f"Local: {event_location}")
            print("-" * 40)
        except Exception as e:
            print("Erro ao extrair informações de um evento:", str(e))

except Exception as e:
    print("⚠️ Ocorreu um erro:", str(e))
    salvar_print(driver, nome_base="erro")

finally:
    driver.quit()

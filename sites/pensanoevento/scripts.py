import os
import sys
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from utils.salvar_print import salvar_print

# Configuração do ChromeDriver
chrome_options = Options()
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service("./chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)

eventos_extraidos = []

try:
    driver.get("https://www.pensanoevento.com.br/eventos/")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    WebDriverWait(driver, 10).until(
        ec.presence_of_all_elements_located((By.CSS_SELECTOR, ".card-text"))
    )

    event_cards = driver.find_elements(By.CLASS_NAME, "card-text")

    quantidadeEventosExtraidos = 3

    for i, card in enumerate(event_cards[:quantidadeEventosExtraidos]):
        try:
            event_title = card.find_element(By.TAG_NAME, "a").text
            event_link = card.find_element(By.TAG_NAME, "a").get_attribute("href")
            event_location = card.find_element(By.TAG_NAME, "span").text

            print(f"Evento: {event_title}")
            print(f"Link: {event_link}")
            print(f"Local: {event_location}")
            print("-" * 40)

            eventos_extraidos.append({
                "titulo": event_title,
                "link": event_link,
                "local": event_location
            })

            time.sleep(1)
        except Exception as e:
            print("Erro ao extrair informações de um evento:", str(e))

    # Cria o diretório de output se não existir
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)

    # Caminho completo do arquivo de saída
    output_path = os.path.join(output_dir, "eventos.json")

    # Salvar os dados extraídos em JSON
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(eventos_extraidos, f, ensure_ascii=False, indent=4)
        print(f"✅ Dados salvos em '{output_path}'")

except Exception as e:
    print("⚠️ Ocorreu um erro:", str(e))
    salvar_print(driver, nome_base="erro")

finally:
    driver.quit()

import os
import sys
import json
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

    # Coleta os primeiros 10 cards de evento
    event_cards = driver.find_elements(By.CLASS_NAME, "event-card")[:2]

    print("\nEventos encontrados:")
    print(event_cards)
    events_data = []
    
    for card in event_cards:
        # Extrai o título
        try:
            title = card.find_element(By.CLASS_NAME, "event-title").text
        except:
            title = "Título não disponível"
        
        # Extrai o link (href)
        try:
            link = card.get_attribute("href")
        except:
            link = "Link não disponível"
        
        print(f"- {title} | {link}")
        events_data.append({
            "title": title,
            "url": link
        })

    output_name = 'eventos_blueticket.json'

    # Obtém o diretório onde o script está localizado
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Cria a pasta 'output' se não existir
    os.makedirs(os.path.join(script_dir, 'output'), exist_ok=True)
    json_path = os.path.join(script_dir, 'output', output_name)

    # Salva os dados em um arquivo JSON
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(events_data, f, ensure_ascii=False, indent=4)
    
    print(f"\nDados salvos com sucesso em: {json_path}")

    # Salva um print da página
    salvar_print(driver, nome_base="pagina_blueticket")

except Exception as e:
    print("⚠️ Ocorreu um erro:", str(e))
    salvar_print(driver, nome_base="erro")

finally:
    driver.quit()
import os
import json
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.salvar_print import salvar_print
from utils.safe_get_text import safe_get_text

# Configuração do navegador
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920,1080")
service = Service('../../chromedriver/chromedriver.exe')
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 10)
cards_to_extract_before_saving = 2

def get_event_links(numOfEvents = None):
    """Coleta todos os links de eventos na página de busca"""
    driver.get("https://www.blueticket.com.br/search?q=")
    cards = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "event-card")))
    print(len(cards))
    
    maxCards = numOfEvents if (numOfEvents and numOfEvents < len(cards) ) else len(cards) 
    return [card.get_attribute("href") for card in cards[:maxCards]]

def extract_event_details(url):
    """Extrai detalhes de uma página de evento"""
    driver.get(url)
    details = {
        "url": url,
        "name": "",
        "date": "",
        "local-subtitle": "",
        "local-description": "",
        "subinfos": [], # Detalhes extras resumidos ao entrar no evento
        "description_cropped": "", # Descrição longa, que será armazenado apenas um pedaço dela
        "classification": "", # Classificação etária ou similar
        "parcelamento": "",
        "nome_organizador": "",
    }
    
    try:
        details["name"] = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "event-name"))).text
    except Exception as e:
        print(f"Erro ao extrair name: {str(e)}")

    # Uma vez encontrado a variável nome, assume-se que o resto já carregou e para de usar wait

    details["date"] = safe_get_text(driver, "event-date")
    details["local-subtitle"] = safe_get_text(driver, "local-subtitle")
    details["local-description"] = safe_get_text(driver, "local-description")

    try:
        subinfos_elements = driver.find_elements(By.CLASS_NAME, "event-subinfos")
        details["subinfos"] = [elem.text.strip() for elem in subinfos_elements if elem.text.strip()]
    except NoSuchElementException:
        details["subinfos"] = []
        print("Nenhuma subinformação encontrada - continuando normalmente")
    except Exception as e:
        details["subinfos"] = []
        print(f"Erro inesperado ao buscar subinformações: {str(e)}")
    
    # Extrai conteúdo da div noMarginBottom (primeiros 255 caracteres do texto)
    try:
        no_margin_div = driver.find_element(By.CLASS_NAME, "noMarginBottom")
        details["description_cropped"] = no_margin_div.text.strip()[:255]
    except NoSuchElementException:
        details["description_cropped"] = ""
        print("Div noMarginBottom não encontrada - campo opcional")
    except Exception as e:
        details["description_cropped"] = ""
        print(f"Erro inesperado ao extrair descrição: {str(e)}")
    
    # Extrai classificação
    try:
        # Encontra todos os elementos que contêm "Classificação"
        elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Classificação')]")
        if elements:
            # Pega o primeiro elemento encontrado e depois seu próximo irmão div
            classification_label = elements[0]
            next_div = classification_label.find_element(By.XPATH, "./following-sibling::div[1]")
            details["classification"] = next_div.text.strip()
    except Exception as e:
        details["classification"] = ""
        print(f"Erro ao extrair classificação: {str(e)}")
    
    # Extrai informações de parcelamento
    try:
        parcelamento_div = driver.find_element(
            By.XPATH,
            "//div[contains(text(), 'Formas de Pagamento')]/following-sibling::div[2]"
        )
        details["parcelamento"] = parcelamento_div.text.strip()
    except NoSuchElementException:
        details["parcelamento"] = ""
        print("Informações de parcelamento não encontradas - campo opcional")
    except Exception as e:
        details["parcelamento"] = ""
        print(f"Erro inesperado ao extrair parcelamento: {str(e)}")

    # Extrai nome do organizador
    try:
        # Busca direta pelo último span com o estilo específico em uma única query
        organizer_span = driver.find_element(
            By.XPATH,
            "(//span[contains(@style, 'font-size: 20px')])[last()]"
        )
        details["nome_organizador"] = organizer_span.text.strip()
    except NoSuchElementException:
        details["nome_organizador"] = ""
        print("Nome do organizador não encontrado - campo opcional")

    except Exception as e:
        details["nome_organizador"] = ""
        print(f"Erro inesperado ao extrair nome do organizador: {str(e)}")

    return details

def main():
    event_links = get_event_links()
    events_data = []
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output", "blueticket.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    for idx, link in enumerate(event_links):
        try:
            print(f"Processando: {link}")
            event = extract_event_details(link)
            events_data.append(event)
        except Exception as e:
            print(f"Erro no evento {link}: {str(e)}")
            salvar_print(driver, nome_base="erro")

            # Tentamos encontrar e clicar no botão "Rejeitar" para fechar o popup caso tenha sido ele o culpado
            reject_button = WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable((By.ID, "adopt-reject-all-button"))
            )
            if reject_button:
                reject_button.click()
                print("Popup de privacidade fechado (via ID)")
            continue

        # Salva a cada X eventos processados com sucesso
        if len(events_data) % cards_to_extract_before_saving == 0:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(events_data, f, ensure_ascii=False, indent=2)
            print(f"{len(events_data)} eventos salvos até agora.")

    # Salva o restante (caso o total não seja múltiplo)
    if len(events_data) % cards_to_extract_before_saving != 0:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(events_data, f, ensure_ascii=False, indent=2)
        print(f"{len(events_data)} eventos salvos no final.")

    print(f"Dados finais salvos em {output_path}")

if __name__ == "__main__":
    try:
        main()
    finally:
        driver.quit()
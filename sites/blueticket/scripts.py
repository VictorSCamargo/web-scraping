import os
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.salvar_print import salvar_print

# Configuração do navegador
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920,1080")
service = Service("C:/chromedriver/chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 10)
cards_to_extract_before_saving = 2

def get_event_links(numOfEvents=1):
    """Coleta todos os links de eventos na página de busca"""
    driver.get("https://www.blueticket.com.br/search?q=")
    cards = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "event-card")))
    print(len(cards))
    return [card.get_attribute("href") for card in cards[:numOfEvents]]  # Limita a 10 eventos

def extract_event_details(url):
    """Extrai detalhes de uma página de evento"""
    driver.get(url)
    details = {
        "url": url,
        "name": wait.until(EC.presence_of_element_located((By.CLASS_NAME, "event-name"))).text,
        "date": wait.until(EC.presence_of_element_located((By.CLASS_NAME, "event-date"))).text,
        "local-subtitle": wait.until(EC.presence_of_element_located((By.CLASS_NAME, "local-subtitle"))).text, # Nome do local
        "local-description": wait.until(EC.presence_of_element_located((By.CLASS_NAME, "local-description"))).text, # Detalhes do endereço do local
        "subinfos": [], # Detalhes extras resumidos ao entrar no evento
        "description_cropped": "", # Descrição longa, que será armazenado apenas um pedaço dela
        "classification": "", # Classificação etária ou similar
        "parcelamento": "",
        "nome_organizador": "",
    }

    # Extrai subinformações (com fallback para texto direto)
    for subinfo in wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "event-subinfos"))):
        texto_completo = subinfo.text.strip()
        if texto_completo:
            details["subinfos"].append(texto_completo)
    
    # Extrai conteúdo da div noMarginBottom (primeiros 255 caracteres do texto)
    try:
        no_margin_div = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "noMarginBottom")))
        full_text = no_margin_div.text.strip()
        details["description_cropped"] = full_text[:255]
    except:
        details["description_cropped"] = ""
        print(f"Erro ao extrair descrição: {str(e)}")
    
    # Extrai classificação (texto após "Classificação")
    try:
        # Encontra todos os elementos que contêm "Classificação"
        elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Classificação')]")
        if elements:
            # Pega o primeiro elemento encontrado e depois seu próximo irmão div
            classification_label = elements[0]
            next_div = classification_label.find_element(By.XPATH, "./following-sibling::div[1]")
            details["classification"] = next_div.text.strip()
    except:
        details["classification"] = ""
        print(f"Erro ao extrair classificação: {str(e)}")
    
    # Extrai informações de parcelamento (nova abordagem simplificada)
    try:
        # Localiza a div com "Formas de Pagamento" e pega a segunda div seguinte
        pagamento_div = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//div[contains(text(), 'Formas de Pagamento')]")
        ))
        
        # Pega a segunda div irmã seguinte
        parcelamento_div = pagamento_div.find_element(By.XPATH, "./following-sibling::div[2]")
        details["parcelamento"] = parcelamento_div.text.strip()
        
    except Exception as e:
        details["parcelamento"] = ""
        print(f"Erro ao extrair parcelamento: {str(e)}")

    try:
        # Procura TODOS os spans com o style específico
        spans = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "//span[contains(@style, 'font-size: 20px')]")
        ))
        
        # Pega o ÚLTIMO span da lista
        if spans:
            details["nome_organizador"] = spans[-1].text.strip()
            
    except Exception as e:
        print(f"Erro ao buscar organizador: {str(e)}")
        details["nome_organizador"] = ""

    return details

def main():
    event_links = get_event_links(1)
    events_data = []
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output", "eventos.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    for idx, link in enumerate(event_links):
        try:
            print(f"Processando: {link}")
            event = extract_event_details(link)
            events_data.append(event)
        except Exception as e:
            print(f"Erro no evento {link}: {str(e)}")
            salvar_print(driver, nome_base="erro")
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
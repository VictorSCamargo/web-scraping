import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException

CHROMEDRIVER_PATH = r'C:\Program Files\chromedriver-win64\chromedriver.exe'

def carregar_mais_eventos(driver, vezes=3):
    for _ in range(vezes):
        try:
            botao = driver.find_element(By.XPATH, "//button[contains(text(), 'Mostrar mais resultados')]")
            driver.execute_script("arguments[0].scrollIntoView(true);", botao)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", botao)
            time.sleep(3)
        except NoSuchElementException:
            print("Não há mais eventos para carregar.")
            break

def coletar_links_eventos(driver):
    cards = driver.find_elements(By.CSS_SELECTOR, 'a.sympla-card')
    return [card.get_attribute('href') for card in cards]

def extrair_titulo(driver):
    try:
        return driver.find_element(By.CSS_SELECTOR, '#event-page-top h1').text.strip()
    except:
        return "Título não encontrado"

def extrair_data(driver):
    try:
        return driver.find_element(By.CSS_SELECTOR, '#event-page-top p').text.strip()
    except:
        return "Data não encontrada"

def extrair_descricao(driver):
    h3s = driver.find_elements(By.TAG_NAME, "h3")
    for h3 in h3s:
        try:
            if "descrição do evento" in h3.text.strip().lower():
                div = h3.find_element(By.XPATH, "following-sibling::div[1]")
                return div.text.strip()
        except:
            continue
    return "Descrição não encontrada"

def extrair_local(driver):
    h3s = driver.find_elements(By.TAG_NAME, "h3")
    for h3 in h3s:
        try:
            if "local" in h3.text.strip().lower():
                div = h3.find_element(By.XPATH, "following-sibling::div[1]")
                return div.text.strip()
        except:
            continue
    return "Local não encontrado"

def salvar_em_json(dados, caminho="eventos_sympla.json"):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    print(f"\n✅ Dados salvos em: {caminho}")

def main():
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)

    driver.get("https://www.sympla.com.br/eventos")
    time.sleep(5)

    carregar_mais_eventos(driver, vezes=3)
    links = coletar_links_eventos(driver)
    print(f"🔗 Total de links encontrados: {len(links)}")

    dados_eventos = []

    for link in links[:-1]:
        driver.get(link)
        time.sleep(3)

        evento = {
            "link": link,
            "titulo": extrair_titulo(driver),
            "data": extrair_data(driver),
            # "descricao": extrair_descricao(driver),
            "local": extrair_local(driver)
        }

        dados_eventos.append(evento)
        print(f"📌 Evento coletado: {evento['titulo']}")

    salvar_em_json(dados_eventos)
    driver.quit()

if __name__ == "__main__":
    main()

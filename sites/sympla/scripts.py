import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException

CHROMEDRIVER_PATH = '../../chromedriver/chromedriver.exe'

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
        try:
            return driver.find_element(By.CSS_SELECTOR, 'h1.event-name span').text.strip()
        except:
            return "Título não encontrado"

def extrair_data(driver):
    try:
        return driver.find_element(By.CSS_SELECTOR, '#event-page-top p').text.strip()
    except:
        try:
            return driver.find_element(By.CSS_SELECTOR, 'p.sta-event-week-date-text').text.strip()
        except:
            return "Data não encontrada"

def extrair_descricao(driver):
    # Convencional
    h3s = driver.find_elements(By.TAG_NAME, "h3")
    for h3 in h3s:
        try:
            if "descrição do evento" in h3.text.strip().lower():
                div = h3.find_element(By.XPATH, "following-sibling::div[1]")
                return div.text.strip()
        except:
            continue

    # Fallback: clicar no botão e pegar conteúdo revelado
    try:
        # Clica no botão do chevron
        botao = driver.find_element(By.CSS_SELECTOR, '.description__action')
        icone = botao.find_element(By.TAG_NAME, 'sb-icon')
        driver.execute_script("arguments[0].click();", icone)
        time.sleep(3)

        # Depois de expandido, procurar conteúdo
        descricoes = driver.find_elements(By.CSS_SELECTOR, '.release.sta-event-description-content-text')
        for d in descricoes:
            texto = d.text.strip()
            if texto:
                return texto
    except:
        pass

    return "Descrição não encontrada"

def extrair_politicas_evento(driver):
    """Extrai uma lista de textos <p> da seção 'Política do evento'."""
    politicas = []
    try:
        h3_elements = driver.find_elements(By.TAG_NAME, "h3")
        for h3 in h3_elements:
            if "política do evento" in h3.text.strip().lower():
                # Pega as divs irmãs (até 2 subsequentes)
                divs = h3.find_elements(By.XPATH, "following-sibling::div")
                for div in divs[:2]:  # Considera só as duas principais subseções
                    try:
                        ps = div.find_elements(By.TAG_NAME, "p")
                        for p in ps:
                            texto = p.text.strip()
                            if texto:
                                politicas.append(texto)
                    except:
                        continue
                break
    except:
        pass

    return politicas if politicas else ["Não encontrado"]

def extrair_produtor(driver):
    """Extrai o nome do produtor a partir da seção 'Sobre o produtor'."""
    try:
        h3_elements = driver.find_elements(By.TAG_NAME, "h3")
        for h3 in h3_elements:
            if "sobre o produtor" in h3.text.strip().lower():
                # Pega o primeiro <div> irmão ou descendente
                div = h3.find_element(By.XPATH, "following::*[1]")
                ps = div.find_elements(By.TAG_NAME, "p")
                for p in ps:
                    texto = p.text.strip()
                    if texto:
                        return texto
    except:
        pass

    return "Não encontrado"

def extrair_parcelamento(driver):
    """Extrai a informação de parcelamento a partir de um <span> com 'parcele'."""
    try:
        spans = driver.find_elements(By.TAG_NAME, "span")
        for span in spans:
            texto = span.text.strip().lower()
            if "parcele" in texto:
                return span.text.strip()
    except:
        pass
    return "Não encontrado"

def extrair_local(driver):
    # Método convencional
    h3s = driver.find_elements(By.TAG_NAME, "h3")
    for h3 in h3s:
        try:
            if "local" in h3.text.strip().lower():
                local_section = h3.find_element(By.XPATH, "following-sibling::*[1]")
                local_subtitle = None
                local_description = []

                try:
                    h4 = local_section.find_element(By.TAG_NAME, "h4")
                    local_subtitle = h4.text.strip()
                except:
                    pass

                try:
                    ps = local_section.find_elements(By.TAG_NAME, "p")
                    local_description = [p.text.strip() for p in ps if p.text.strip()]
                except:
                    pass

                return {
                    "local_subtitle": local_subtitle or "Não encontrado",
                    "local_description": "\n".join(local_description) if local_description else "Não encontrado"
                }
        except:
            continue

    # Fallback alternativo
    try:
        address_div = driver.find_element(By.CLASS_NAME, "address")
        spans = address_div.find_elements(By.CLASS_NAME, "sta-event-venue-address-text")
        if len(spans) >= 2:
            return {
                "local_subtitle": spans[0].text.strip(),
                "local_description": spans[1].text.strip()
            }
    except:
        pass

    return {
        "local_subtitle": "Não encontrado",
        "local_description": "Não encontrado"
    }

def salvar_em_json(dados, caminho="eventos_sympla_backup.json"):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    print(f"\n✅ Dados salvos em: {caminho}")

def main():
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)

    driver.get("https://www.sympla.com.br/eventos")
    time.sleep(5)

    carregar_mais_eventos(driver, vezes=20)
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
            "descricao": extrair_descricao(driver),
            "politicas_evento": extrair_politicas_evento(driver),
            "nome_organizador": extrair_produtor(driver),
            "parcelamento": extrair_parcelamento(driver),
            **extrair_local(driver)
        }

        if evento['titulo'] != "Título não encontrado":
            dados_eventos.append(evento)
            print(f"📌 Evento coletado: {evento['titulo']}")

    salvar_em_json(dados_eventos)
    driver.quit()

if __name__ == "__main__":
    main()


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

chrome_options = Options()
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service("./chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)

eventos_extraidos = []

def scroll_until_no_more_new_events(driver, timeout=2, max_attempts=20):
    last_count = 0
    same_count_retries = 0

    for _ in range(max_attempts):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(timeout)

        event_cards = driver.find_elements(By.CLASS_NAME, "card-body")
        current_count = len(event_cards)

        print(f"Eventos carregados: {current_count}")

        if current_count == last_count:
            same_count_retries += 1
        else:
            same_count_retries = 0

        if same_count_retries >= 3:
            break

        last_count = current_count

def extract_event_link():
    event_cards = driver.find_elements(By.CLASS_NAME, "card-body")
    events_links = []
    quantidade_eventos_extraidos = len(event_cards)

    for i, card in enumerate(event_cards[:quantidade_eventos_extraidos]):
        try:
            event_link = card.find_element(By.TAG_NAME, "a").get_attribute("href")
            print(event_link)
            events_links.append(event_link)
            time.sleep(1)
        except Exception as e:
            print("Erro ao extrair links dos eventos:", str(e))
    return events_links

def extract_event_details(links):
    for link in links:
        try:
            driver.get(link)
            WebDriverWait(driver, 10).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, "body"))
            )
            time.sleep(2)

            event = {
                "url": link,
                "name": None,
                "date": None,
                "place_name": None,
                "address": None,
                "subinfos": [],
                "description_cropped": None,
                "classification": None,
                "parcelamento": None,
                "nome_organizador": None,
            }

            try:
                titulo = driver.find_element(By.TAG_NAME, "h1").text.strip()
                event["name"] = titulo
            except:
                pass

            lis = driver.find_elements(By.CSS_SELECTOR, "div.card-body ul.list li")
            for li in lis:
                texto = li.text.strip()

                if "Nome do Evento:" in texto:
                    event["name"] = texto.replace("Nome do Evento:", "").strip()
                elif "Data:" in texto:
                    event["date"] = texto.replace("Data:", "").strip()
                elif "Horário de Abertura:" in texto or "Horário de término:" in texto:
                    event["subinfos"].append(texto)
                elif "Classificação:" in texto:
                    event["classification"] = texto.replace("Classificação:", "").strip()
                elif "Instagram:" in texto:
                    try:
                        ig = li.find_element(By.TAG_NAME, "a").text.strip()
                        event["subinfos"].append(f"Instagram: {ig}")
                    except:
                        pass

            try:
                card_bodies = driver.find_elements(By.CSS_SELECTOR, "div.card-body")
                for card in card_bodies:
                    try:
                        title = card.find_element(By.CSS_SELECTOR, "h5.card-title").text.strip()
                        if title.lower() == "localização":
                            try:
                                place_name = card.find_element(By.CSS_SELECTOR, "h6.card-subtitle").text.strip()
                                event["place_name"] = place_name
                            except:
                                pass
                            try:
                                address = card.find_element(By.CSS_SELECTOR, "p.card-text").text.strip()
                                event["address"] = address
                            except:
                                pass
                            break
                    except:
                        continue
            except Exception as e:
                print(f"Erro ao extrair localização: {e}")

            try:
                description = driver.find_element(By.CSS_SELECTOR, "div.description").text.strip()
                event["description_cropped"] = description[:200] + "..." if len(description) > 200 else description
            except:
                pass

            eventos_extraidos.append(event)
            print(f"Evento extraído: {event['name']}")
            time.sleep(1)

        except Exception as e:
            print(f"Erro ao extrair detalhes do evento {link}: {e}")

try:
    driver.get("https://www.pensanoevento.com.br/eventos/")

    scroll_until_no_more_new_events(driver, timeout=2, max_attempts=20)

    WebDriverWait(driver, 10).until(
        ec.presence_of_all_elements_located((By.CSS_SELECTOR, ".card-text"))
    )

    events_links = extract_event_link()
    extract_event_details(events_links)

    print(events_links)
    print(eventos_extraidos)

    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "pensanoevento.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(eventos_extraidos, f, ensure_ascii=False, indent=4)
        print(f"Dados salvos em '{output_path}'")

except Exception as e:
    print("Ocorreu um erro:", str(e))
    salvar_print(driver, nome_base="erro")

finally:
    driver.quit()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
import time

# Carrega o chromedriver
CHROMEDRIVER_PATH = r'C:\Program Files\chromedriver-win64\chromedriver.exe'

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)

driver.get("https://www.sympla.com.br/eventos")
time.sleep(5)

# Clica no botão para carregar mais eventos 10 vezes
for _ in range(10):
    try:
        botao_mais = driver.find_element(By.XPATH, "//button[contains(text(), 'Carregar mais eventos')]")
        driver.execute_script("arguments[0].scrollIntoView(true);", botao_mais)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", botao_mais)
        time.sleep(3)
    except NoSuchElementException:
        print("Botão não encontrado ou não há mais eventos.")
        break

# Coleta os eventos
eventos = driver.find_elements(By.CSS_SELECTOR, 'a.sympla-card')
print(f"Total de eventos encontrados: {len(eventos)}")

for evento in eventos:
    titulo = evento.text.strip()
    link = evento.get_attribute('href')
    print(f"{titulo} - {link}")

driver.quit()

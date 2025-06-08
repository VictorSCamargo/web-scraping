from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


# Pensado para ser usado no Blueticket
def safe_get_text(driver, class_name):
    try:
        element = driver.find_element(By.CLASS_NAME, class_name)
        return element.text.strip()
    except NoSuchElementException:
        print(f"{class_name} não encontrado - campo opcional")
        return ""
    except Exception as e:
        print(f"Erro ao extrair {class_name}: {str(e)}")
        return ""

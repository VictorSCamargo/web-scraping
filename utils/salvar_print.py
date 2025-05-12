from datetime import datetime
import os

# Função utilitária para tirar print
def salvar_print(driver, nome_base="screenshot"):
    pasta = "prints"
    os.makedirs(pasta, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    caminho = os.path.join(pasta, f"{nome_base}_{timestamp}.png")
    driver.save_screenshot(caminho)
    print(f"📸 Print salvo em: {caminho}")

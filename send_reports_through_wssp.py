import os
import time
from pathlib import Path
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def get_attatchments(project_address):
    attachment_folder = Path(project_address)
    graphics_address = {}

    for attch in attachment_folder.glob('*.png'):
        graphics_address[attch.name] = os.path.join(project_address, attch.name)

    return graphics_address

def send_mssg_to_chat(options, page_url, group_name, graphics):

    print('\n.-----------------------------------------------------------------------.')

    try:
        driver = webdriver.Chrome(options=options)        
        print(f'[*] Abriendo Grupo de WSSP ({group_name})')

        driver.get(page_url)
        print("[*] Esperando que WhatsApp Web cargue completamente...")

        # ✅ Esperar a que aparezca el buscador (indicador de carga completa)
        WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true'][@data-tab='3']"))
        )
        print("[✓] WhatsApp Web cargado.")

        # Buscar grupo
        search_box = driver.find_element(By.XPATH, "//div[@contenteditable='true'][@data-tab='3']")
        search_box.click()
        time.sleep(1)
        search_box.send_keys(group_name)
        time.sleep(3)

        # Esperar y hacer clic en el grupo
        clip_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//span[@title='{group_name}']"))
        )
        clip_button.click()
        print(f"\n[✓] Click realizado en el grupo: '{group_name}'")
        time.sleep(3)

        for graph_name, graph_address in graphics.items():
            # Esperar hasta que el ícono del clip esté presente y visible
            attach_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and @aria-label='Adjuntar']"))
            )
            # attach_button = WebDriverWait(driver, 10).until(
            #     EC.element_to_be_clickable((By.XPATH, "//button[@title='Adjuntar' and @type='button']"))
            # )
            attach_button.click()
            print(f"\n[✓] Click realizado en el botón de 'Adjuntar'")
            time.sleep(2)

            # Esperar el input para cargar imagen
            image_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@accept='image/*,video/mp4,video/3gpp,video/quicktime']"))
            )
            print(f'[*] Cargando imagen ({graph_name}) ...')
            image_input.send_keys(graph_address)
            time.sleep(3)

            # Esperar y escribir texto junto a la imagen
            # caption_box = WebDriverWait(driver, 10).until(
            #     EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true' and @aria-label='Añade un comentario']"))
            # )
            caption_box = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true' and @aria-label='Escribe un mensaje']"))
            )
            print(f'[*] Escribiendo mensaje ...')
            time.sleep(1)
            caption_box.send_keys(graph_name.split('_')[1])

            # Enviar
            send_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and @aria-label='Enviar']"))
            )
            send_button.click()
            time.sleep(3)

    finally:
        print(f'\n✅ Reportes enviados correctamente')
        driver.quit()

    print("'-----------------------------------------------------------------------'\n")

# Captura de gráficos de Power BI por página
def main(project_address, WSSP_CONFIF):
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--user-data-dir=C:\\Users\\AYACDA23\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 6")

    graphics = get_attatchments(project_address)

    page_url = WSSP_CONFIF['page_url']
    for group_name in WSSP_CONFIF['group_names']:
        send_mssg_to_chat(options, page_url, group_name, graphics)
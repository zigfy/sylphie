import os
import time
import json
import logging
import smtplib
import requests
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.vscode', '.env'))
vtex_api_key = os.getenv('VTEX_API_KEY')
vtex_api_token = os.getenv('VTEX_API_TOKEN')
price_endpoint = os.getenv('PRICE_ENDPOINT')
gmail_address = os.getenv('GMAIL_ADDRESS')
gmail_password = os.getenv('GMAIL_PASSWORD')

logging.basicConfig(level=logging.INFO)

def vtex_get_prices(skus: list):
    json_path = os.path.join(os.path.dirname(__file__), '..', 'planilhas/vtex', 'vtex_response.json')
    headers = {
        'Accept': "application/json",
        'Content-Type': "application/json",
        'X-VTEX-API-AppKey': f"{vtex_api_key}",
        'X-VTEX-API-AppToken': f"{vtex_api_token}"
    }
    res = []
    
    for i, sku in enumerate(skus):
        if sku:
            sku = sku.replace("None", "").strip()
            if not sku:
                logging.warning(f"SKU inválido após remoção: Original - {skus[i]}")
                continue
            
            if i > 0 and i % 30 == 0:
                time.sleep(1)
                
            try:
                req = requests.get(url=f'{price_endpoint}{sku}', headers=headers, timeout=5)
                req.raise_for_status()
                res.append([req.json()])
            except requests.exceptions.RequestException as e:
                logging.error(f"Erro ao solicitar o SKU {sku}: {e}")
                continue
            except requests.RequestException:
                print(f"erro no request, sku: {sku}. continuando...")
                continue
            except:
                print(f'erro não identificado no request. sku: {sku}...')
                continue
        else:
            logging.warning(f"SKU inválido encontrado: {sku}")
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    
    return json_path


def vtex_diffusion_mail():
    gmail_service = smtplib.SMTP('smtp.gmail.com', 587)
    gmail_service.starttls()
    gmail_service.login(user=gmail_address, password=gmail_password)

    msg = f'''\n From: {gmail_address}
    Subject: Test
    This is a test.
    Line two. /n
    Line three...
    /r Test.
'''
    gmail_service.sendmail(from_addr=gmail_address, to_addrs=gmail_address, msg=msg)
    gmail_service.quit()
    return "runned."


def download_file(uri, dir):
    options = webdriver.ChromeOptions()
    #options.add_argument("--start-maximized")
    #options.add_argument("--headless")
    options.add_experimental_option("detach", True)
    options.add_argument(fr"user-data-dir=C:\Users\cristiano.silva\AppData\Local\Google\Chrome\User Data\Default")
    working_dir = {'download.default_directory' : fr'{dir}'}
    options.add_experimental_option('prefs', working_dir)
    driver = webdriver.Chrome(options=options, keep_alive=False)
    driver.get(f'{uri}')
    default_dir = {'download.default_directory': fr'C:\Users\cristiano.silva\Downloads'}
    options.add_experimental_option('prefs', default_dir)
    time.sleep(15)
    driver.quit()
    return True

def download_products_file(uri, dir):
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")
    options.add_experimental_option("detach", True)
    options.add_argument(fr"user-data-dir=C:\Users\cristiano.silva\AppData\Local\Google\Chrome\User Data\Default")
    working_dir = {'download.default_directory' : fr'{dir}'}
    options.add_experimental_option('prefs', working_dir)
    driver = webdriver.Chrome(options=options, keep_alive=False)
    driver.get(f'{uri}')
    default_dir = {'download.default_directory': fr'C:\Users\cristiano.silva\Downloads'}
    options.add_experimental_option('prefs', default_dir)
    wait = WebDriverWait(driver, 10)

    if driver.current_url == fr'https://portalsmart.gruporihappy.com.br/login?redirectTo=%2Fdashboard':
        email_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/core-root/div/div/c-login/div[2]/form[1]/div[2]/c-input[1]/div/div/div/input')))
        email_input.send_keys("cristiano.silva@gruporihappy.com.br")
        password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/core-root/div/div/c-login/div[2]/form[1]/div[2]/c-input[2]/div/div/div/input')))
        password_input.send_keys(gmail_password)
        driver.find_element(By.XPATH, '/html/body/core-root/div/div/c-login/div[2]/form[1]/div[5]/button').click()
    WebDriverWait(driver, 10).until(EC.url_to_be('https://portalsmart.gruporihappy.com.br/dashboard'))
    button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn -outline -primary uppercase waves-effect import__btn-download ng-star-inserted')))
    button.click()
    time.sleep(8)
    driver.quit()
    return True

import os.path
import time
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, ElementNotSelectableException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SAMPLE_SPREADSHEET_ID = "1-JfiG1L7bkifer_LwpaOODEGem0YOfhk_sL6ze6NIwc"
SAMPLE_RANGE_NAME = "Página1!A:A"

def main():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
            creds = flow.run_local_server(port=0)
    
    with open("token.json", "w") as token:
        token.write(creds.to_json())
    
    return creds

def start_driver():
    chrome_options = Options()
    arguments = [
        '--lang=pt_BR', 
        '--window-size=1366x768', 
        '--incognito',
        '--headless'
    ]
    for argument in arguments:
        chrome_options.add_argument(argument)
    
    chrome_options.add_experimental_option('prefs', {
        'download.prompt_for_download': False,
        'profile.default_content_setting_values.notifications': 2,
        'profile.default_content_setting_values.automatic_downloads': 1
    })

    driver = webdriver.Chrome(options=chrome_options)

    wait = WebDriverWait(
        driver,
        20,
        poll_frequency=1,
        ignored_exceptions=[NoSuchElementException, ElementNotVisibleException, ElementNotSelectableException]
    )
    return driver, wait

def check_for_banned_terms(banned_terms_list, product_name):
    return any(term in product_name for term in banned_terms_list)

def check_for_all_product_terms(product_terms_list, product_name):
    return all(term in product_name for term in product_terms_list)

def check_for_taxes_fees(price):
    fees_terms = ['taxas', 'impostos']
    return any(term in price.lower() for term in fees_terms)

def check_trusted_domain(link):
    untrusted_domains = ['shopee', 'aliexpress', 'alibaba', 'temu']
    return not any(domain in link for domain in untrusted_domains)

def google_shopping_search(driver, product_name):
    driver.get("https://shopping.google.com.br/")
    
    banned_terms = ['usado', 'used', 'kit', 'controle remoto', 'hélices', 'airdrop', 'maleta']
    product_name = product_name.lower()
    banned_terms_list = banned_terms
    product_terms_list = product_name.split(" ")

    # Explicit wait up to 10 seconds for the element to be present
    search_box = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'yyJm8b')))

    search_box.send_keys(product_name, Keys.ENTER)

    results_list = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'i0X6df')))
      
    offers_list = [] 
    
    for result in results_list:
        name = result.find_element(By.CLASS_NAME, 'tAxDx').text.lower()

        has_banned_terms = check_for_banned_terms(banned_terms_list, name)
        has_all_product_terms = check_for_all_product_terms(product_terms_list, name)

        if not has_banned_terms and has_all_product_terms:
            try:
                price_element = result.find_element(By.CLASS_NAME, 'a8Pemb')
                price_text = price_element.text

                if check_for_taxes_fees(price_text):
                    continue  # Ignore results that mention taxes or fees

                price = float(price_text.replace("R$", "").replace(" ", "").replace(".", "").replace(",", "."))
                reference_element = result.find_element(By.CLASS_NAME, 'bONr3b')
                parent_element = reference_element.find_element(By.XPATH, '..')
                link = parent_element.get_attribute('href')

                if check_trusted_domain(link):
                    offers_list.append((price, link))
            
            except Exception as e:
                continue

    return offers_list

def get_products(creds):
    try:
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
        products = result.get('values', [])
        products = products[1:] if products else []  # Remove header
                
        if not products:
            print("No data found.")
            return []
        
        return products

    except HttpError as err:
        print(err)
        return []

def search_prices_and_update_spreadsheet(products, creds):
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()
    
    for i, product in enumerate(products):
        product_name = product[0]
        google_shopping_offers_list = google_shopping_search(driver, product_name)

        product_row = [product_name]  # Keep product name in the first column, but don't alter it
        if google_shopping_offers_list:
            for offer in google_shopping_offers_list[:10]:
                product_row.extend([offer[0], offer[1]])  # Add price and link to the product

            # Add current date and time in column V
            current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            range_update = f"Página1!V{i + 2}"  # i + 2 to skip header and start at the correct row
            sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_update,
                                  valueInputOption="RAW", body={"values": [[current_datetime]]}).execute()
    
        if product_row:
            # Update starting from column B
            range_update = f"Página1!B{i + 2}"  # Update starting from column B
            sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_update,
                                  valueInputOption="RAW", body={"values": [product_row[1:]]}).execute()

def start():
    creds = main()  
    products = get_products(creds)
    if products:
        search_prices_and_update_spreadsheet(products, creds)

if __name__ == "__main__":
    driver, wait = start_driver()
    try:
        start()
    finally:
        driver.quit()

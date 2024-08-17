import os
import time
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager

def create_driver_selenium():
    options = get_chrome_browser_options()  # Usa il metodo corretto per ottenere le opzioni
    service = ChromeService(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def HTML_to_PDF(FilePath):
    # Validazione e preparazione del percorso del file
    if not os.path.isfile(FilePath):
        raise FileNotFoundError(f"The specified file does not exist: {FilePath}")
    FilePath = f"file:///{os.path.abspath(FilePath).replace(os.sep, '/')}"
    driver = create_driver_selenium()
    try:
        driver.get(FilePath)
        time.sleep(3)
        start_time = time.time()
        pdf_base64 = driver.execute_cdp_cmd("Page.printToPDF", {
            "printBackground": True,         # Include lo sfondo nella stampa
            "landscape": False,              # Stampa in verticale (False per ritratto)
            "paperWidth": 8.27,              # Larghezza del foglio in pollici (A4)
            "paperHeight": 11.69,            # Altezza del foglio in pollici (A4)
            "marginTop": 0.8,                # Margine superiore in pollici (circa 2 cm)
            "marginBottom": 0.8,             # Margine inferiore in pollici (circa 2 cm)
            "marginLeft": 0.8,               # Margine sinistro in pollici (circa 2 cm)
            "marginRight": 0.8,              # Margine destro in pollici (circa 2 cm)
            "displayHeaderFooter": False,   # Non visualizzare intestazioni e piè di pagina
            "preferCSSPageSize": True,       # Preferire le dimensioni della pagina CSS
            "generateDocumentOutline": False, # Non generare un sommario del documento
            "generateTaggedPDF": False,      # Non generare PDF taggato
            "transferMode": "ReturnAsBase64" # Restituire il PDF come stringa base64
        })
        if time.time() - start_time > 120:
            raise TimeoutError("PDF generation exceeded the specified timeout limit.")
        return pdf_base64['data']
    except WebDriverException as e:
        raise RuntimeError(f"WebDriver exception occurred: {e}")
    finally:
        driver.quit()

def get_chrome_browser_options():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-extensions")
    options.add_argument('--disable-gpu')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("window-size=1200x800")
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("--incognito")
    options.add_argument('--log-level=3')
    options.add_argument("--silent") 
    return options

def printred(text):
    RED = "\033[91m"
    RESET = "\033[0m"
    print(f"{RED}{text}{RESET}")

def printyellow(text):
    YELLOW = "\033[93m"
    RESET = "\033[0m"
    print(f"{YELLOW}{text}{RESET}")
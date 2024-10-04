import os
import time
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from loguru import logger
import sys

logger.remove()
logger.add(sys.stdout, level="DEBUG")

def create_driver_selenium():
    logger.debug("Creating Selenium WebDriver with Chrome options.")
    options = get_chrome_browser_options()
    logger.debug(f"Options configured: {options.arguments}")

    logger.debug("Installing ChromeDriver using webdriver_manager...")
    chrome_install = ChromeDriverManager().install()
    folder = os.path.dirname(chrome_install)
    chromedriver_path = os.path.join(folder, "chromedriver.exe")
    logger.debug(f"ChromeDriver installed at path: {chromedriver_path}")

    service = ChromeService(executable_path=chromedriver_path)
    logger.debug("Starting Chrome WebDriver.")
    return webdriver.Chrome(service=service, options=options)

def HTML_to_PDF(FilePath):

    if not os.path.isfile(FilePath):
        logger.error(f"File not found: {FilePath}")
        raise FileNotFoundError(f"The specified file does not exist: {FilePath}")
    logger.info(f"Converting HTML file to PDF: {FilePath}")

    FilePath = f"file:///{os.path.abspath(FilePath).replace(os.sep, '/')}"

    driver = create_driver_selenium()

    try:
        logger.debug(f"Opening file in the browser: {FilePath}")
        driver.get(FilePath)
        time.sleep(2)
        logger.debug("Executing Page.printToPDF command.")
        pdf_base64 = driver.execute_cdp_cmd("Page.printToPDF", {
            "printBackground": True,         # Include lo sfondo nella stampa
            "landscape": False,              # Stampa in verticale (False per ritratto)
            "paperWidth": 8.27,              # Larghezza del foglio in pollici (A4)
            "paperHeight": 11.69,            # Altezza del foglio in pollici (A4)
            "marginTop": 0.8,                # Margine superiore in pollici (circa 2 cm)
            "marginBottom": 0.8,             # Margine inferiore in pollici (circa 2 cm)
            "marginLeft": 0.5,               # Margine sinistro in pollici (circa 2 cm)
            "marginRight": 0.5,              # Margine destro in pollici (circa 2 cm)
            "displayHeaderFooter": False,   # Non visualizzare intestazioni e piè di pagina
            "preferCSSPageSize": True,       # Preferire le dimensioni della pagina CSS
            "generateDocumentOutline": False, # Non generare un sommario del documento
            "generateTaggedPDF": False,      # Non generare PDF taggato
            "transferMode": "ReturnAsBase64" # Restituire il PDF come stringa base64
        })
        logger.info("PDF generation successful.")
        return pdf_base64['data']
    except WebDriverException as e:
        logger.error(f"WebDriver exception occurred: {e}")
        raise RuntimeError(f"WebDriver exception occurred: {e}")
    finally:
        logger.debug("Closing the browser.")
        driver.quit()

def get_chrome_browser_options():
    logger.debug("Configuring Chrome browser options.")
    options = webdriver.ChromeOptions()
    options.headless = True

    options_list = [
        "--no-sandbox",
        "--headless=new",
        "--disable-dev-shm-usage",
        "--ignore-certificate-errors",
        "--disable-extensions",
        "--disable-gpu",
        "--disable-background-timer-throttling",
        "--disable-backgrounding-occluded-windows",
        "--disable-translate",
        "--disable-popup-blocking",
        "--no-first-run",
        "--no-default-browser-check",
        "--single-process",
        "--disable-logging",
        "--disable-autofill",
        "--disable-plugins",
        "--disable-animations",
        "--disable-cache",
    ]
    for opt in options_list:
        logger.debug(f"Adding option: {opt}")
        options.add_argument(opt)

    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    return options

def printred(text):
    RED = "\033[91m"
    RESET = "\033[0m"
    print(f"{RED}{text}{RESET}")

def printyellow(text):
    YELLOW = "\033[93m"
    RESET = "\033[0m"
    print(f"{YELLOW}{text}{RESET}")

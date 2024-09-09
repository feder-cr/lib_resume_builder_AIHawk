import os
import time
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def create_driver_selenium():
    options = get_chrome_browser_options()
    service = ChromeService(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def HTML_to_PDF(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The specified file does not exist: {file_path}")

    file_url = f"file:///{os.path.abspath(file_path).replace(os.sep, '/')}"
    driver = create_driver_selenium()

    try:
        driver.get(file_url)
        time.sleep(2)  # Wait for the page to load
        pdf_base64 = driver.execute_cdp_cmd("Page.printToPDF", {
            "printBackground": True,
            "landscape": False,
            "paperWidth": 8.27,
            "paperHeight": 11.69,
            "marginTop": 0.8,
            "marginBottom": 0.8,
            "marginLeft": 0.8,
            "marginRight": 0.8,
            "displayHeaderFooter": False,
            "preferCSSPageSize": True,
            "generateDocumentOutline": False,
            "generateTaggedPDF": False,
            "transferMode": "ReturnAsBase64"
        })
        return pdf_base64['data']
    except WebDriverException as e:
        raise RuntimeError(f"WebDriver exception occurred: {e}")
    finally:
        driver.quit()


def get_chrome_browser_options():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("window-size=1200x800")
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-backgrounding-occluded-windows")
    options.add_argument("--disable-translate")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--single-process")
    options.add_argument("--disable-logging")
    options.add_argument("--disable-autofill")
    options.add_argument("--disable-plugins")
    options.add_argument("--disable-animations")
    options.add_argument("--disable-cache")
    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])

    return options


def print_colored(text, color):
    colors = {
        "red": "\033[91m",
        "yellow": "\033[93m"
    }
    RESET = "\033[0m"
    print(f"{colors.get(color, '')}{text}{RESET}")


def print_red(text):
    print_colored(text, "red")


def print_yellow(text):
    print_colored(text, "yellow")
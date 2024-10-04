import base64
import os
from pathlib import Path
import tempfile
import inquirer
from lib_resume_builder_AIHawk.config import global_config
from lib_resume_builder_AIHawk.utils import HTML_to_PDF
import webbrowser
from loguru import logger
import time
import sys

logger.remove()
logger.add(sys.stdout, level="DEBUG")

class FacadeManager:
    def __init__(self, api_key, style_manager, resume_generator, resume_object, log_path):
        # Ottieni il percorso assoluto della directory della libreria
        lib_directory = Path(__file__).resolve().parent
        global_config.STRINGS_MODULE_RESUME_PATH = lib_directory / "resume_prompt/strings_feder-cr.py"
        global_config.STRINGS_MODULE_RESUME_JOB_DESCRIPTION_PATH = lib_directory / "resume_job_description_prompt/strings_feder-cr.py"
        global_config.STRINGS_MODULE_NAME = "strings_feder_cr"
        global_config.STYLES_DIRECTORY = lib_directory / "resume_style"
        global_config.LOG_OUTPUT_FILE_PATH = log_path
        global_config.API_KEY = api_key
        if config is not None:
            global_config.LLM_MODEL = config['llm_model']
            global_config.LLM_MODEL_TYPE = config['llm_model_type']
            global_config.LLM_API_URL = config['llm_api_url']
        else:
            global_config.LLM_MODEL = 'gpt-4o'
            global_config.LLM_MODEL_TYPE = 'openai'
            global_config.LLM_API_URL = 'https://api.openai.com/v1/'
        self.style_manager = style_manager
        self.style_manager.set_styles_directory(global_config.STYLES_DIRECTORY)
        self.resume_generator = resume_generator
        self.resume_generator.set_resume_object(resume_object)
        self.selected_style = None  # Proprietà per memorizzare lo stile selezionato

    def prompt_user(self, choices: list[str], message: str) -> str:
        questions = [
            inquirer.List('selection', message=message, choices=choices),
        ]
        return inquirer.prompt(questions)['selection']

    def prompt_for_url(self, message: str) -> str:
        questions = [
            inquirer.Text('url', message=message),
        ]
        return inquirer.prompt(questions)['url']

    def prompt_for_text(self, message: str) -> str:
        questions = [
            inquirer.Text('text', message=message),
        ]
        return inquirer.prompt(questions)['text']

    def choose_style(self, test_flag=False):
        styles = self.style_manager.get_styles()
        if not styles:
            print("No styles available")
            return None

        final_style_choice = "Create your resume style in CSS"
        formatted_choices = self.style_manager.format_choices(styles)
        formatted_choices.append(final_style_choice)

        if test_flag:
            # Automatically select the first available style during tests
            selected_choice = formatted_choices[0]
        else:
            selected_choice = self.prompt_user(formatted_choices, "Which style would you like to adopt?")


        if selected_choice == final_style_choice:
            tutorial_url = "https://github.com/feder-cr/lib_resume_builder_AIHawk/blob/main/how_to_contribute/web_designer.md"
            print("\nOpening tutorial in your browser...")
            webbrowser.open(tutorial_url)
            exit()
        else:
            self.selected_style = selected_choice.split(' (')[0]
            print(f"Style selected: {self.selected_style}")
            return self.selected_style

    def prompt_user_with_input(self, choices: list[str]) -> str:

        print("Available styles:")
        for idx, choice in enumerate(choices, 1):
            print(f"{idx}. {choice}")

        try:
            selected_choice = int(input("Enter the number of the style you would like to adopt: "))
            if selected_choice < 1 or selected_choice > len(choices):
                raise ValueError("Invalid selection.")
        except ValueError as e:
            print(f"Error: {e}. Please enter a valid number.")
            return self.prompt_user_with_input(choices)

        return choices[selected_choice - 1]

    def pdf_base64(self, job_description_url=None, job_description_text=None):
        logger.debug("Starting PDF generation process.")
        start_time = time.time()

        # Проверка входных параметров
        if job_description_url is not None and job_description_text is not None:
            logger.error("Both 'job_description_url' and 'job_description_text' provided. Raising ValueError.")
            raise ValueError("Esattamente uno tra 'job_description_url' o 'job_description_text' deve essere fornito.")
        
        if self.selected_style is None:
            logger.error("Selected style is None. Raising ValueError.")
            raise ValueError("Devi scegliere uno stile prima di generare il PDF.")
        
        logger.debug("Fetching style path.")
        style_path = self.style_manager.get_style_path(self.selected_style)
        logger.debug(f"Style path obtained: {style_path}")

        # Создание временного HTML-файла
        logger.debug("Creating temporary HTML file.")
        with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.html', encoding='utf-8') as temp_html_file:
            temp_html_path = temp_html_file.name
            logger.debug(f"Temporary HTML file created at path: {temp_html_path}")

            # Генерация резюме
            if job_description_url is None and job_description_text is None:
                logger.debug("Generating resume without job description.")
                self.resume_generator.create_resume(style_path, temp_html_path)
            elif job_description_url is not None and job_description_text is None:
                logger.debug(f"Generating resume using job description URL: {job_description_url}")
                self.resume_generator.create_resume_job_description_url(style_path, job_description_url, temp_html_path)
            elif job_description_url is None and job_description_text is not None:
                logger.debug("Generating resume using job description text.")
                self.resume_generator.create_resume_job_description_text(style_path, job_description_text, temp_html_path)
            else:
                logger.error("Invalid input combination, returning None.")
                return None

        # Вызов функции HTML_to_PDF и логирование времени
        logger.debug(f"Starting HTML to PDF conversion for file: {temp_html_path}")
        pdf_conversion_start = time.time()
        pdf_base64 = HTML_to_PDF(temp_html_path)
        logger.debug(f"HTML to PDF conversion completed in {time.time() - pdf_conversion_start:.2f} seconds.")

        # Удаление временного файла
        logger.debug(f"Removing temporary file: {temp_html_path}")
        os.remove(temp_html_path)

        total_time = time.time() - start_time
        logger.debug(f"Total PDF generation process completed in {total_time:.2f} seconds.")
        return pdf_base64

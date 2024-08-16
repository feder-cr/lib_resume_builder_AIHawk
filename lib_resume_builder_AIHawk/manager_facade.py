import base64
import os
from pathlib import Path
import inquirer
import requests
import json
from lib_resume_builder_AIHawk.config import global_config
from lib_resume_builder_AIHawk.utils import HTML_to_PDF


class FacadeManager:
    def __init__(self, api_key, style_manager, resume_generator, resume_object, log_path):
        global_config.STRINGS_MODULE_RESUME_PATH=Path("resume_prompt/strings_feder-cr.py").resolve(),
        global_config.STRINGS_MODULE_RESUME_JOB_DESCRIPTION_PATH=Path("resume_job_description_prompt/strings_feder-cr.py").resolve(),
        global_config.STRINGS_MODULE_NAME="strings_feder_cr",
        global_config.STYLES_DIRECTORY=Path("resume_style").resolve(),
        global_config.OUTPUT_FILE_PATH=Path("temp_resume.html").resolve(),
        global_config.LOG_OUTPUT_FILE_PATH=log_path,
        global_config.API_KEY=api_key
        self.style_manager = style_manager
        self.style_manager.set_styles_directory(global_config.STYLES_DIRECTORY)
        self.resume_generator = resume_generator
        self.resume_generator.set_config(global_config)
        self.resume_generator.set_resume_object(resume_object)
        self.job_description_url = None

    def set_job_description_url(self, url):
        self.job_description_url = url

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

    def pdf_base64(self):
        while True:
            action = self.prompt_user(['Create Resume', 'Create Resume based on Job Description', 'Exit'], "What would you like to do?")
            if action == 'Exit':
                print("Exiting...")
                break
            styles = self.style_manager.get_styles()
            if not styles:
                print("No styles available")
                continue
            formatted_choices = self.style_manager.format_choices(styles)
            selected_choice = self.prompt_user(formatted_choices, "Which style would you like to adopt?")
            selected_style = selected_choice.split(' (')[0]
            style_path = self.style_manager.get_style_path(selected_style)
            if action == 'Create Resume':
                self.resume_generator.create_resume(style_path)
            elif action == 'Create Resume based on Job Description':
                url_job_description = self.prompt_for_url("Please enter the URL of the job description:")
                self.resume_generator.create_resume_job_description(style_path, url_job_description)
            pdf_base64 = base64.b64decode(HTML_to_PDF(global_config.OUTPUT_FILE_PATH))
            if os.path.exists(global_config.OUTPUT_FILE_PATH):
                os.remove(global_config.OUTPUT_FILE_PATH)
        return pdf_base64

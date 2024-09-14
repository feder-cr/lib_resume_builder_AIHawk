from typing import Any
from string import Template
from typing import Any
from lib_resume_builder_AIHawk.gpt_resume import LLMResumer
from lib_resume_builder_AIHawk.gpt_resume_job_description import LLMResumeJobDescription
from lib_resume_builder_AIHawk.module_loader import load_module
from lib_resume_builder_AIHawk.config import global_config
import yaml
from pdfminer.high_level import extract_text
from jsonschema import validate, ValidationError


class ResumeGenerator:
    def __init__(self):
        self.resume_object = None
    
    def set_resume_object(self, resume_object):
         self.resume_object = resume_object

    def _create_resume(self, gpt_answerer: Any, style_path, temp_html_path):
        gpt_answerer.set_resume(self.resume_object)
        template = Template(global_config.html_template)
        message = template.substitute(markdown=gpt_answerer.generate_html_resume(), style_path=style_path)
        with open(temp_html_path, 'w', encoding='utf-8') as temp_file:
            temp_file.write(message)

    def create_resume(self, style_path, temp_html_file):
        strings = load_module(global_config.STRINGS_MODULE_RESUME_PATH, global_config.STRINGS_MODULE_NAME)
        gpt_answerer = LLMResumer(strings)
        self._create_resume(gpt_answerer, style_path, temp_html_file)

    def create_resume_job_description_url(self, style_path: str, url_job_description: str, temp_html_path):
        strings = load_module(global_config.STRINGS_MODULE_RESUME_JOB_DESCRIPTION_PATH, global_config.STRINGS_MODULE_NAME)
        gpt_answerer = LLMResumeJobDescription( strings)
        gpt_answerer.set_job_description_from_url(url_job_description)
        self._create_resume(gpt_answerer, style_path, temp_html_path)

    def create_resume_job_description_text(self, style_path: str, job_description_text: str, temp_html_path):
        strings = load_module(global_config.STRINGS_MODULE_RESUME_JOB_DESCRIPTION_PATH, global_config.STRINGS_MODULE_NAME)
        gpt_answerer = LLMResumeJobDescription(strings)
        gpt_answerer.set_job_description_from_text(job_description_text)
        self._create_resume(gpt_answerer, style_path, temp_html_path)
    
    def pdf_to_yaml(self, input_file: str, output_yaml: str, schema_path: str):
        def load_yaml(file_path: str) -> dict:
            with open(file_path, 'r') as file:
                return yaml.safe_load(file)

        def validate_yaml(yaml_content: str, schema: dict) -> dict:
            try:
                yaml_dict = yaml.safe_load(yaml_content)
                validate(instance=yaml_dict, schema=schema)
                return {"valid": True, "errors": None}
            except ValidationError as e:
                return {"valid": False, "errors": str(e)}

        def save_yaml(data: str, output_file: str):
            with open(output_file, 'w') as file:
                file.write(data)

        # Carica lo schema YAML
        schema = load_yaml(schema_path)

        # Determina se l'input è un PDF o un file di testo
        if input_file.lower().endswith('.pdf'):
            resume_text = extract_text(input_file)  # Converte il PDF in testo
        else:
            with open(input_file, 'r') as file:
                resume_text = file.read()  # Carica il file TXT

        # Qui possiamo richiamare un processo GPT tramite gpt_answerer, o lasciare una struttura per inserirlo in futuro.
        gpt_answerer = LLMResumer(None)  # Passare gli argomenti necessari in futuro
        gpt_answerer.set_resume(resume_text)  # Usa il testo del resume

        # Simuliamo il processo GPT per generare YAML. Questo va integrato nel gpt_answerer
        generated_yaml = gpt_answerer.generate_yaml()  # Il metodo specifico di LLMResumer

        # Validazione del YAML generato
        validation_result = validate_yaml(generated_yaml, schema)
        if validation_result["valid"]:
            print(f"YAML valido, salvato in: {output_yaml}")
            save_yaml(generated_yaml, output_yaml)
        else:
            print(f"Errore nella validazione del YAML: {validation_result['errors']}")

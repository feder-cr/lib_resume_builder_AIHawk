import os
import textwrap

import logging
from typing import Dict
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from concurrent.futures import ThreadPoolExecutor, as_completed

from lib_resume_builder_AIHawk.gpt import LLMLoggerGpt, GPT, AIAdapter

load_dotenv()

log_folder = 'log'
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

# Configure the log file
log_file = os.path.join(log_folder, 'app.log')

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8')
    ]
)

logger = logging.getLogger(__name__)


class LLMLogger(LLMLoggerGpt):
    pass
class LoggerChatModel(GPT):
    pass



class LLMResumer:
    def __init__(self,strings):
        self.job_description = None
        self.strings = strings
        self.resume = None
        self.ai_adapter = AIAdapter()
        self.llm_cheap = LoggerChatModel(self.ai_adapter)

    @staticmethod
    def _preprocess_template_string(template: str) -> str:
        return textwrap.dedent(template)

    def set_resume(self, resume):
        self.resume = resume

    def generate_section(self, prompt_template: str, input_data: Dict[str, any]) -> str:
        prompt = ChatPromptTemplate.from_template(self._preprocess_template_string(prompt_template))
        chain = prompt | self.llm_cheap | StrOutputParser()
        return chain.invoke(input_data)

    def generate_header(self) -> str:
        if self.resume.personal_information:
            return self.generate_section(self.strings.prompt_header,
                                         {"personal_information": self.resume.personal_information})
        return ""

    def generate_education_section(self) -> str:
        if self.resume.education_details:
            return self.generate_section(self.strings.prompt_education,
                                         {"education_details": self.resume.education_details})
        return ""

    def generate_work_experience_section(self) -> str:
        if self.resume.experience_details:
            return self.generate_section(self.strings.prompt_working_experience,
                                         {"experience_details": self.resume.experience_details})
        return ""

    def generate_side_projects_section(self) -> str:
        if self.resume.projects:
            return self.generate_section(self.strings.prompt_side_projects, {"projects": self.resume.projects})
        return ""

    def generate_achievements_section(self) -> str:
        if self.resume.achievements:
            return self.generate_section(self.strings.prompt_achievements, {
                "achievements": self.resume.achievements,
                "certifications": self.resume.certifications,
                "job_description": self.job_description
            })
        return ""

    def generate_certifications_section(self) -> str:
        if self.resume.certifications:
            return self.generate_section(self.strings.prompt_certifications, {
                "certifications": self.resume.certifications,
                "job_description": self.job_description
            })
        return ""

    def generate_additional_skills_section(self) -> str:
        skills = set()

        if self.resume.experience_details:
            for exp in self.resume.experience_details:
                if exp.skills_acquired:
                    skills.update(exp.skills_acquired)

        if self.resume.education_details:
            for edu in self.resume.education_details:
                if edu.exam:
                    for exam in edu.exam:
                        skills.update(exam.keys())

        if skills or self.resume.languages or self.resume.interests:
            return self.generate_section(self.strings.prompt_additional_skills, {
                "languages": self.resume.languages,
                "interests": self.resume.interests,
                "skills": skills,
            })
        return ""

    def generate_html_resume(self) -> str:
        functions = {
            "header": self.generate_header,
            "education": self.generate_education_section,
            "work_experience": self.generate_work_experience_section,
            "side_projects": self.generate_side_projects_section,
            "achievements": self.generate_achievements_section,
            "certifications": self.generate_certifications_section,
            "additional_skills": self.generate_additional_skills_section,
        }

        with ThreadPoolExecutor() as executor:
            future_to_section = {executor.submit(fn): section for section, fn in functions.items()}
            results = {}
            for future in as_completed(future_to_section):
                section = future_to_section[future]
                try:
                    result = future.result()
                    if result:
                        results[section] = result
                except Exception as exc:
                    print(f'{section} ha generato un\'eccezione: {exc}')

        full_resume = "<body>\n"
        full_resume += f"  {results.get('header', '')}\n"
        full_resume += "  <main>\n"
        full_resume += f"    {results.get('education', '')}\n"
        full_resume += f"    {results.get('work_experience', '')}\n"
        full_resume += f"    {results.get('side_projects', '')}\n"
        full_resume += f"    {results.get('achievements', '')}\n"
        full_resume += f"    {results.get('certifications', '')}\n"
        full_resume += f"    {results.get('additional_skills', '')}\n"
        full_resume += "  </main>\n"
        full_resume += "</body>"
        return full_resume
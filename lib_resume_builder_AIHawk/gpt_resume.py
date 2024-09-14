import json
import os
import textwrap
import time
from pathlib import Path

import httpx
import logging
from datetime import datetime
from typing import Dict, List, Union
from dotenv import load_dotenv


from abc import ABC, abstractmethod
from langchain_core.messages.ai import AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompt_values import StringPromptValue
from concurrent.futures import ThreadPoolExecutor, as_completed

from lib_resume_builder_AIHawk.config import global_config


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


class AIModel(ABC):
    @abstractmethod
    def invoke(self, prompt: str) -> str:
        pass


class OpenAIModel(AIModel):
    def __init__(self, api_key: str, llm_model: str, llm_api_url: str):
        from langchain_openai import ChatOpenAI
        print(global_config.API_KEY,global_config.LLM_MODEL,global_config.LLM_API_URL)
        self.model = ChatOpenAI(model_name=global_config.LLM_MODEL, openai_api_key=global_config.API_KEY,
                                temperature=0.4, base_url=global_config.LLM_API_URL)

    def invoke(self, prompt: str) -> str:
        print("invoke in openai")
        response = self.model.invoke(prompt)
        print(response)
        return response


class ClaudeModel(AIModel):
    def __init__(self, api_key: str, llm_model: str, llm_api_url: str):
        from langchain_anthropic import ChatAnthropic
        self.model = ChatAnthropic(model=llm_model, api_key=api_key,
                                   temperature=0.4, base_url=llm_api_url)

    def invoke(self, prompt: str) -> str:
        response = self.model.invoke(prompt)
        return response


class OllamaModel(AIModel):
    def __init__(self, api_key: str, llm_model: str, llm_api_url: str):
        from langchain_ollama import ChatOllama
        self.model = ChatOllama(model=llm_model, base_url=llm_api_url)

    def invoke(self, prompt: str) -> str:
        response = self.model.invoke(prompt)
        return response


class GeminiModel(AIModel):
    def __init__(self, api_key:str, llm_model: str, llm_api_url: str):
        from langchain_google_genai import ChatGoogleGenerativeAI
        self.model = ChatGoogleGenerativeAI(model=llm_model, google_api_key=api_key)

    def invoke(self, prompt: str) -> str:
        response = self.model.invoke(prompt)
        return response


class AIAdapter:
    def __init__(self):
        self.model = self._create_model()

    def _create_model(self) -> AIModel:
        llm_model_type = global_config.LLM_MODEL_TYPE
        llm_model = global_config.LLM_MODEL
        llm_api_url = global_config.LLM_API_URL
        print('Using {0} with {1} from {2}'.format(
            llm_model_type, llm_model, llm_api_url))

        if llm_model_type == "openai":
            print(global_config.API_KEY, llm_model, llm_api_url)
            return OpenAIModel(global_config.API_KEY, llm_model, llm_api_url)
        elif llm_model_type == "claude":
            return ClaudeModel(global_config.API_KEY, llm_model, llm_api_url)
        elif llm_model_type == "ollama":
            return OllamaModel(global_config.API_KEY, llm_model, llm_api_url)
        elif llm_model_type == "gemini":
            return GeminiModel(global_config.API_KEY, llm_model, llm_api_url)
        else:
            raise ValueError(f"Unsupported model type: {llm_model_type}")

    def invoke(self, prompt: str) -> str:
        return self.model.invoke(prompt)


class LLMLogger:

    def __init__(self, llm: Union[OpenAIModel, OllamaModel, ClaudeModel, GeminiModel]):

        self.llm = llm
        logger.debug("LLMLogger successfully initialized with LLM: %s", llm)

    @staticmethod
    def log_request(prompts, parsed_reply: Dict[str, Dict]):
        logger.debug("Starting log_request method")
        logger.debug("Prompts received: %s", prompts)
        logger.debug("Parsed reply received: %s", parsed_reply)

        try:
            calls_log = os.path.join(
                Path("data_folder/output"), "open_ai_calls.json")
            logger.debug("Logging path determined: %s", calls_log)
        except Exception as e:
            logger.error("Error determining the log path: %s", str(e))
            raise

        if isinstance(prompts, StringPromptValue):
            logger.debug("Prompts are of type StringPromptValue")
            prompts = prompts.text
            logger.debug("Prompts converted to text: %s", prompts)
        elif isinstance(prompts, Dict):
            logger.debug("Prompts are of type Dict")
            try:
                prompts = {
                    f"prompt_{i + 1}": prompt.content
                    for i, prompt in enumerate(prompts.messages)
                }
                logger.debug("Prompts converted to dictionary: %s", prompts)
            except Exception as e:
                logger.error(
                    "Error converting prompts to dictionary: %s", str(e))
                raise
        else:
            logger.debug(
                "Prompts are of unknown type, attempting default conversion")
            try:
                prompts = {
                    f"prompt_{i + 1}": prompt.content
                    for i, prompt in enumerate(prompts.messages)
                }
                logger.debug(
                    "Prompts converted to dictionary using default method: %s", prompts)
            except Exception as e:
                logger.error(
                    "Error converting prompts using default method: %s", str(e))
                raise

        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.debug("Current time obtained: %s", current_time)
        except Exception as e:
            logger.error("Error obtaining current time: %s", str(e))
            raise

        try:
            token_usage = parsed_reply["usage_metadata"]
            output_tokens = token_usage["output_tokens"]
            input_tokens = token_usage["input_tokens"]
            total_tokens = token_usage["total_tokens"]
            logger.debug("Token usage - Input: %d, Output: %d, Total: %d",
                         input_tokens, output_tokens, total_tokens)
        except KeyError as e:
            logger.error("KeyError in parsed_reply structure: %s", str(e))
            raise

        try:
            model_name = parsed_reply["response_metadata"]["model_name"]
            logger.debug("Model name: %s", model_name)
        except KeyError as e:
            logger.error("KeyError in response_metadata: %s", str(e))
            raise

        try:
            prompt_price_per_token = 0.00000015
            completion_price_per_token = 0.0000006
            total_cost = (input_tokens * prompt_price_per_token) + \
                (output_tokens * completion_price_per_token)
            logger.debug("Total cost calculated: %f", total_cost)
        except Exception as e:
            logger.error("Error calculating total cost: %s", str(e))
            raise

        try:
            log_entry = {
                "model": model_name,
                "time": current_time,
                "prompts": prompts,
                "replies": parsed_reply["content"],
                "total_tokens": total_tokens,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_cost": total_cost,
            }
            logger.debug("Log entry created: %s", log_entry)
        except KeyError as e:
            logger.error(
                "Error creating log entry: missing key %s in parsed_reply", str(e))
            raise

        try:
            with open(calls_log, "a", encoding="utf-8") as f:
                json_string = json.dumps(
                    log_entry, ensure_ascii=False, indent=4)
                f.write(json_string + "\n")
                logger.debug("Log entry written to file: %s", calls_log)
        except Exception as e:
            logger.error("Error writing log entry to file: %s", str(e))
            raise


class LoggerChatModel:

    def __init__(self, llm: Union[OpenAIModel, OllamaModel, ClaudeModel, GeminiModel]):
        self.llm = llm
        logger.debug(
            "LoggerChatModel successfully initialized with LLM: %s", llm)

    def __call__(self, messages: List[Dict[str, str]]) -> str:
        logger.debug("Entering __call__ method with messages: %s", messages)
        while True:
            try:
                logger.debug("Attempting to call the LLM with messages")

                reply = self.llm.invoke(messages)
                logger.debug("LLM response received: %s", reply)

                parsed_reply = self.parse_llmresult(reply)
                logger.debug("Parsed LLM reply: %s", parsed_reply)

                LLMLogger.log_request(
                    prompts=messages, parsed_reply=parsed_reply)
                logger.debug("Request successfully logged")

                return reply

            except httpx.HTTPStatusError as e:
                logger.error("HTTPStatusError encountered: %s", str(e))
                if e.response.status_code == 429:
                    retry_after = e.response.headers.get('retry-after')
                    retry_after_ms = e.response.headers.get('retry-after-ms')

                    if retry_after:
                        wait_time = int(retry_after)
                        logger.warning(
                            "Rate limit exceeded. Waiting for %d seconds before retrying (extracted from 'retry-after' header)...",
                            wait_time)
                        time.sleep(wait_time)
                    elif retry_after_ms:
                        wait_time = int(retry_after_ms) / 1000.0
                        logger.warning(
                            "Rate limit exceeded. Waiting for %f seconds before retrying (extracted from 'retry-after-ms' header)...",
                            wait_time)
                        time.sleep(wait_time)
                    else:
                        wait_time = 30
                        logger.warning(
                            "'retry-after' header not found. Waiting for %d seconds before retrying (default)...",
                            wait_time)
                        time.sleep(wait_time)
                else:
                    logger.error("HTTP error occurred with status code: %d, waiting 30 seconds before retrying",
                                 e.response.status_code)
                    time.sleep(30)

            except Exception as e:
                logger.error("Unexpected error occurred: %s", str(e))
                logger.info(
                    "Waiting for 30 seconds before retrying due to an unexpected error.")
                time.sleep(30)
                continue

    def parse_llmresult(self, llmresult: AIMessage) -> Dict[str, Dict]:
        logger.debug("Parsing LLM result: %s", llmresult)

        try:
            content = llmresult.content
            response_metadata = llmresult.response_metadata
            id_ = llmresult.id
            usage_metadata = llmresult.usage_metadata

            parsed_result = {
                "content": content,
                "response_metadata": {
                    "model_name": response_metadata.get("model_name", ""),
                    "system_fingerprint": response_metadata.get("system_fingerprint", ""),
                    "finish_reason": response_metadata.get("finish_reason", ""),
                    "logprobs": response_metadata.get("logprobs", None),
                },
                "id": id_,
                "usage_metadata": {
                    "input_tokens": usage_metadata.get("input_tokens", 0),
                    "output_tokens": usage_metadata.get("output_tokens", 0),
                    "total_tokens": usage_metadata.get("total_tokens", 0),
                },
            }

            logger.debug("Parsed LLM result successfully: %s", parsed_result)
            return parsed_result

        except KeyError as e:
            logger.error(
                "KeyError while parsing LLM result: missing key %s", str(e))
            raise

        except Exception as e:
            logger.error(
                "Unexpected error while parsing LLM result: %s", str(e))
            raise



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
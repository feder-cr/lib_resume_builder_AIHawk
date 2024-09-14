import json
import os
import time
import unittest
from unittest.mock import patch, MagicMock
from lib_resume_builder_AIHawk import Resume, ResumeGenerator, StyleManager, FacadeManager
from pathlib import Path
import base64
import yaml
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestPDFGeneration(unittest.TestCase):

    def setUp(self):
        base_dir = Path(__file__).resolve().parent
        with open(base_dir / 'yaml_example/config.yaml', 'r') as f:
            self.config = yaml.safe_load(f)

        with open(base_dir / 'yaml_example/plain_text_resume.yaml', 'r') as f:
            self.plain_text_resume = yaml.safe_load(f)

        with open(base_dir / 'yaml_example/secrets.yaml', 'r') as f:
            self.secrets = yaml.safe_load(f)

        # Extract necessary data
        self.llm_api_key = self.secrets['llm_api_key']
        self.output_path = Path("data_folder/output")

        self.plain_text_resume = yaml.dump(self.plain_text_resume, default_flow_style=False)

        # Initialize components
        self.style_manager = StyleManager()
        self.resume_generator = ResumeGenerator()
        logger.info(self.plain_text_resume)
        self.resume_object = Resume(self.plain_text_resume)
        self.resume_generator_manager = FacadeManager(
            self.llm_api_key, self.style_manager, self.resume_generator, self.resume_object, self.output_path, self.config
        )
        os.system('cls' if os.name == 'nt' else 'clear')
        # Ensure style is selected
        self.resume_generator_manager.choose_style(test_flag=True)
        os.system('cls' if os.name == 'nt' else 'clear')

        # Create the necessary directory and file
        self.output_path.mkdir(parents=True, exist_ok=True)
        calls_log = self.output_path / "open_ai_calls.json"
        if not calls_log.exists():
            with open(calls_log, "w", encoding="utf-8") as f:
                json.dump([], f)

    @patch('lib_resume_builder_AIHawk.manager_facade.os.system')
    def test_pdf_generation(self, mock_os_system):
        # Generate the PDF
        logger.info("Generating PDF...")
        pdf_base64 = self.resume_generator_manager.pdf_base64()
        self.assertIsNotNone(pdf_base64)

        # Save the PDF to disk
        folder_path = 'generated_cv'
        os.makedirs(folder_path, exist_ok=True)
        file_path_pdf = os.path.join(folder_path, "CV_test.pdf")
        logger.info(f"Saving PDF to {file_path_pdf}...")
        with open(file_path_pdf, "wb") as f:
            f.write(base64.b64decode(pdf_base64))



        # Assert that the file exists and is not empty // Final Check
        self.assertTrue(os.path.exists(file_path_pdf))
        self.assertGreater(os.path.getsize(file_path_pdf), 0)

if __name__ == '__main__':
    unittest.main()
# lib_resume_builder_AIHawk

🚀 **Join Our Telegram Community!** 🚀

Join our **Telegram community** for:
- **Support with AIHawk software**
- **Share your experiences** with AIhawk and learn from others
- **Job search tips** and **resume advice**
- **Idea exchange** and resources for your projects

📲 **[Join now!](https://t.me/AIhawkCommunity)**

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Configuration](#configuration)
4. [Usage](#usage)
5. [Dependencies](#dependencies)
6. [Documentation](#documentation)
8. [Troubleshooting](#troubleshooting)
9. [How to Contribute](#how-to-contribute)
   - [Web Designers](#web-designers)
   - [Prompt Engineers](#prompt-engineers)
   - [Software Engineers](#software-engineers)
   - [Other Contributions](#other-contributions)
10. [Credits](#credits)
11. [License](#license)
12. [Disclaimer](#disclaimer)

## Introduction

`lib_resume_builder_AIHawk` is a Python library designed to simplify the creation of personalized, professional resumes. By integrating with GPT models, this library allows you to generate resumes that are tailored to specific job descriptions and formatted in various styles. It provides a flexible approach to resume building with minimal effort.

## Features

- **Dynamic Resume Styling:** Use different pre-defined styles to create visually appealing resumes.
- **Job Description Integration:** Customize resumes based on job description URLs.
- **Flexible Configuration:** Set up resume details using YAML configuration files.
- **Interactive CLI:** Easily generate resumes via an interactive command-line interface.

## Configuration



## Usage

Here’s a step-by-step example of how to use `lib_resume_builder_AIHawk` to generate a resume:

1. **Import the Required Classes**

   ```python
   from lib_resume_builder_AIHawk import Resume, StyleManager, ResumeGenerator, FacadeManager
   import os
   import base64
   from pathlib import Path
   from lib_resume_builder_AIHawk.utils import validate_secrets
   ```

2. **Setup and Configuration**

   ```python
   def main():
       folder = "log"
       if not os.path.exists(folder):
           os.makedirs(folder)
       
       log_path = Path(folder).resolve()
       api_key = validate_secrets(Path("secrets.yaml"))
       
       with open("plain_text_resume.yaml", "r") as file:
           plain_text_resume = file.read()
           resume_object = Resume(plain_text_resume)
       
       style_manager = StyleManager()
       resume_generator = ResumeGenerator()
       manager = FacadeManager(api_key, style_manager, resume_generator, resume_object, log_path)
       
       if os.path.exists("resume.pdf"):
           os.remove("resume.pdf")
       
       with open("resume.pdf", "xb") as f:
           f.write(base64.b64decode(manager.pdf_base64()))
   
   if __name__ == "__main__":
       main()
   ```

## Dependencies

`lib_resume_builder_AIHawk` requires the following Python packages:

- `langchain`
- `langchain-community`
- `langchain-core`
- `langchain-openai`
- `langchain-text-splitters`
- `langsmith`
- `openai`
- `regex==2024.7.24`
- `selenium==4.9.1`
- `webdriver-manager==4.0.2`
- `inquirer`
- `faiss-cpu`


## Documentation

Here’s a detailed documentation for each module in the `lib_resume_builder_AIHawk` library:

---

## lib_resume_builder_AIHawk Documentation

### Resume

#### Overview

The `Resume` class represents a resume created from plain text. It takes resume details in YAML format and provides methods to interact with and manipulate these details.

#### Class Definition

```python
class Resume:
    def __init__(self, plain_text_resume: str):
        """
        Initializes the Resume object with plain text resume details.
        
        :param plain_text_resume: A string containing resume details in YAML format.
        """
```

### Configuring `plain_text_resume.yaml`

This YAML file contains all the personal and professional details needed for resume generation.

1. **Create the File**

   Create a file named `plain_text_resume.yaml` in your project directory.

2. **Define Personal Information**

   ```yaml
   personal_information:
     name: [Name]
     surname: [Surname]
     date_of_birth: "[DD/MM/YYYY]"
     country: [Country]
     city: [City]
     address: [Address]
     phone_prefix: "[+Country Code]"
     phone: "[Phone Number]"
     email: [Email Address]
     github: [GitHub URL]
     linkedin: [LinkedIn URL]
   ```

3. **Provide Education Details**

   ```yaml
   education_details:
     - degree: [Degree Type]
       university: [University Name]
       gpa: "[GPA]"
       graduation_year: "[Graduation Year]"
       field_of_study: [Field of Study]
       exam:
         [Course Name]: "[Grade]"
   ```

4. **List Experience Details**

   ```yaml
   experience_details:
     - position: [Job Title]
       company: [Company Name]
       employment_period: "[MM/YYYY - MM/YYYY or Present]"
       location: [Location]
       industry: [Industry]
       key_responsibilities:
         - [Responsibility Description]
       skills_acquired:
         - [Skill]
   ```

5. **Detail Your Projects**

   ```yaml
   projects:
     - name: [Project Name]
       description: [Project Description]
       link: "[Project URL]"
   ```

6. **Add Achievements**

   ```yaml
   achievements:
     - name: [Achievement Title]
       description: [Achievement Description]
   ```

7. **List Certifications**

   ```yaml
   certifications:
     - [Certification Name]
   ```

8. **Detail Your Language Skills**

   ```yaml
   languages:
     - language: [Language]
       proficiency: [Proficiency Level]
   ```

9. **Add Interests**

   ```yaml
   interests:
     - [Interest]
   ```


### StyleManager

#### Overview

The `StyleManager` class manages the different styles available for formatting resumes. It provides methods to retrieve and apply these styles.

#### Class Definition

```python
class StyleManager:
    def __init__(self):
        """
        Initializes the StyleManager with default styles.
        """
```

#### Methods

- **`__init__()`**  
  Initializes the `StyleManager` with a set of predefined resume styles.

- **`get_styles()`**  
  Returns a list of available resume styles.

- **`apply_style(resume: Resume, style_name: str)`**  
  Applies a specified style to the given resume object.

### ResumeGenerator

#### Overview

The `ResumeGenerator` class handles the process of generating a resume document based on the details provided and the selected style.

#### Class Definition

```python
class ResumeGenerator:
    def __init__(self):
        """
        Initializes the ResumeGenerator.
        """
```

#### Methods

- **`__init__()`**  
  Initializes the `ResumeGenerator`.

- **`generate_pdf(resume: Resume, style_name: str) -> bytes`**  
  Generates a PDF resume based on the provided resume details and style. Returns the PDF file content as a byte string.

- **`generate_html(resume: Resume, style_name: str) -> str`**  
  Generates an HTML representation of the resume based on the provided details and style. Returns the HTML content as a string.

### FacadeManager

#### Overview

The `FacadeManager` class provides a simplified interface to interact with the `Resume`, `StyleManager`, and `ResumeGenerator` classes. It manages the overall process of generating a resume PDF.

### Class Definition

```python
class FacadeManager:
    def __init__(self, api_key: str, style_manager: StyleManager, resume_generator: ResumeGenerator, resume: Resume, log_path: Path):
        """
        Initializes the FacadeManager with the necessary components.
        
        :param api_key: OpenAI API key for GPT integration.
        :param style_manager: An instance of StyleManager.
        :param resume_generator: An instance of ResumeGenerator.
        :param resume: An instance of Resume.
        :param log_path: Path to the directory where logs will be stored.
        """
```

#### Methods

- **`__init__(api_key: str, style_manager: StyleManager, resume_generator: ResumeGenerator, resume: Resume, log_path: Path)`**  
  Initializes the `FacadeManager` with the API key, style manager, resume generator, resume, and log path.

- **`pdf_base64()`**  
  Generates a base64-encoded PDF of the resume.

### Utils

#### Overview

The `utils` module contains utility functions used by the other modules. These include functions for validation and file management.


## Troubleshooting

For issues, open an issue on GitHub or join our Telegram community for support.
📲 [Join now!](https://t.me/AIhawkCommunity)

## Contributors

- [feder-cr](https://github.com/feder-cr) - Creator and Lead Developer

## How to Contribute

We welcome contributions to `lib_resume_builder_AIHawk`! Whether you are a designer, prompt engineer, software engineer, or have other skills, here’s how you can help:

### Web Designers

Enhance resume templates with improved visual design. [Learn more.](how_to_contribute/web_designer.md)

### Prompt Engineers

Help refine prompts for better resume customization. [Learn more.](how_to_contribute/prompt_engineer.md)

### Software Engineers

Submit pull requests to improve functionality or fix bugs. [Learn more.](https://docs.github.com/en/get-started/exploring-projects-on-github/contributing-to-a-project)

### Other Contributions

You can also contribute by:
- Reporting issues
- Suggesting new features
- Improving documentation

## Credits

*(To be added)*

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

`lib_resume_builder_AIHawk` is designed to assist with resume creation. While it aims to be helpful, it may not cover all specific requirements for every job application.

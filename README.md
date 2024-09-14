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
3. [Usage](#usage)
4. [Dependencies](#dependencies)
5. [Documentation](#documentation)
6. [Troubleshooting](#troubleshooting)
7. [How to Contribute](#how-to-contribute)
   - [Web Designers](#web-designers)
   - [Prompt Engineers](#prompt-engineers)
   - [Software Engineers](#software-engineers)
   - [Other Contributions](#other-contributions)
8. [License](#license)
9. [Disclaimer](#disclaimer)

## Introduction

`lib_resume_builder_AIHawk` is a Python lib designed to simplify the creation of personalized, professional resumes. By integrating with GPT models, this library allows you to generate resumes that are tailored to specific job descriptions and formatted in various styles. It provides a flexible approach to resume building with minimal effort.

## Features

- **Dynamic Resume Styling:** Use different pre-defined styles to create visually appealing resumes.
- **Job Description Integration:** Customize resumes based on job description URLs.
- **Flexible Configuration:** Set up resume details using YAML configuration files.
- **Interactive CLI:** Easily generate resumes via an interactive command-line interface.

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

(TODO) (:


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

## Testing and Contributing

### Setting Up the Development Environment

1. Clone the repository:
   ```
   git clone [repository_url]
   cd [repository_name]
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up pre-commit hooks:
   ```
   pip install pre-commit
   pre-commit install
   ```

### Running Tests

To run the unit tests:

```bash
python -m unittest lib_resume_builder_AIHawk/unit-test/pdf_generation.py
```

**Note:** For end-to-end (E2E) tests, you need to provide a valid API token. Ensure you have set this up before running the full test suite.


### Pre-commit Hooks

We use pre-commit hooks to maintain code quality and run tests automatically before each commit. The pre-commit configuration will run the unit tests specified above.

**Important:** Always run `pre-commit install` after cloning the repository or when the pre-commit configuration changes. This ensures you have the latest checks in place and prevents pushing potential bugs to the repository.

If you encounter any issues or have questions, please open an issue in the repository or contact the maintainers.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

`lib_resume_builder_AIHawk` is designed to assist with resume creation. While it aims to be helpful, the service may not cover all specific requirements for every job application. We assume no responsibility for the quality or accuracy of the generated resumes.


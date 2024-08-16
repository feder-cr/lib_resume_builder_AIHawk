from setuptools import setup, find_packages

setup(
    name='lib_resume_builder_AIHawk',
    version='0.1',
    description='A package to generate AI-assisted resumes using GPT models',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='feder-cr',
    author_email='federico.elia.majo@gmail.com',
    url='https://github.com/feder-cr/lib_resume_builder_AIHawk',
    packages=find_packages(include=['lib_resume_builder_AIHawk', 'lib_resume_builder_AIHawk.*']),
    install_requires=[ 
        'langchain==0.2.11',
        'langchain-community==0.2.10',
        'langchain-core==0.2.24',
        'langchain-openai==0.1.17',
        'langchain-text-splitters==0.2.2',
        'langsmith==0.1.93',
        'openai==1.37.1',
        'regex==2024.7.24',
        'selenium==4.9.1',
        'webdriver-manager==4.0.2',
        'inquirer',
        'langchainhub',
        'unstructured',
        'faiss-cpu',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',  
    include_package_data=True,  # Include altri file indicati nel MANIFEST.in
)

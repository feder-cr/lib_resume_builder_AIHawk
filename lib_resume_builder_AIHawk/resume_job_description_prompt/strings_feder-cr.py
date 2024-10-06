from lib_resume_builder_AIHawk.template_base import *


prompt_header = """
Act as an HR expert and resume writer specializing in ATS-friendly resumes. Your task is to create a professional and polished header for the resume. The header should:

1. **Contact Information**: Include your full name, city and country, phone number, email address, LinkedIn profile, and GitHub profile.
2. **Formatting**: Ensure the contact details are presented clearly and are easy to read.

To implement this:
- If any of the contact information fields (e.g., LinkedIn profile, GitHub profile) are not provided (i.e., `None`), omit them from the header.

- **My information:**  
  {personal_information}
""" + prompt_header_template

prompt_education = """
Act as an HR expert and resume writer with a specialization in creating ATS-friendly resumes. Your task is to articulate the educational background for a resume, ensuring it aligns with the provided job description. For each educational entry, ensure you include:

1. **Institution Name and Location**: Specify the university or educational institution’s name and location.
2. **Degree and Field of Study**: Clearly indicate the degree earned and the field of study.
3. **Grade**: Include your Grade if it is strong and relevant.
4. **Relevant Coursework**: List key courses with their grades to showcase your academic strengths. If no coursework is provided, omit this section from the template.

To implement this, follow these steps:
- If the exam details are not provided (i.e., `None`), skip the coursework section when filling out the template.
- If the exam details are available, fill out the coursework section accordingly.


- **My information:**  
  {education_details}

- **Job Description:**  
  {job_description}
"""+ prompt_education_template

prompt_working_experience = """
Act as an HR expert and resume writer with a specialization in creating ATS-friendly resumes. Your task is to **tailor the work experience** section of the resume **to align closely with the job description provided**, making sure it highlights relevant skills, achievements, and responsibilities. 

For each job entry, make sure to:

1. **Company Name and Location**: Clearly state the name of the company and where it is located.
2. **Job Title**: Provide the exact job title.
3. **Dates of Employment**: Mention the start and end dates of employment.
4. **Key Responsibilities and Achievements**:
    - Focus on responsibilities and achievements that are most **relevant** to the job description.
    - **Use keywords** from the job description to highlight my relevant experience.
    - Prioritize measurable achievements and specific contributions.
    - If applicable, quantify results (e.g., "improved efficiency by 30%", "increased revenue by 20%").

Only include the details if they are available and relevant. If certain details are missing (e.g., responsibilities, achievements), skip them.

Here's the relevant information:

**My Experience**:  
{experience_details}

**Job Description**:  
{job_description}

Please make sure the output is in the **format of a resume**, and that each job entry is formatted professionally with bullets and consistent style.
"""+ prompt_working_experience_template


prompt_side_projects = """
Act as an HR expert and resume writer with a specialization in creating ATS-friendly resumes. Your task is to highlight notable side projects based on the provided job description. For each project, ensure you include:

1. **Project Name and Link**: Provide the name of the project and include a link to the GitHub repository or project page.
2. **Project Details**: Describe any notable recognition or achievements related to the project, such as GitHub stars or community feedback.
3. **Technical Contributions**: Highlight your specific contributions and the technologies used in the project.

Ensure that the project descriptions demonstrate your skills and achievements relevant to the job description.

To implement this:
- If any of the project details (e.g., link, achievements) are not provided (i.e., `None`), omit those sections when filling out the template.


- **My information:**  
  {projects}

- **Job Description:**  
  {job_description}
"""+ prompt_side_projects_template


prompt_achievements = """
Act as an HR expert and resume writer with a specialization in creating ATS-friendly resumes. Your task is to list significant achievements based on the provided job description. For each achievement, ensure you include:

1. **Award or Recognition**: Clearly state the name of the award, recognition, scholarship, or honor.
2. **Description**: Provide a brief description of the achievement and its relevance to your career or academic journey.

Ensure that the achievements are clearly presented and effectively highlight your accomplishments.

To implement this:
- If any of the achievement details (e.g., certifications, descriptions) are not provided (i.e., `None`), omit those sections when filling out the template.


- **My information:**  
  {achievements}

- **Job Description:**  
  {job_description}
"""+ prompt_achievements_template


prompt_certifications = """
Act as an HR expert and resume writer with a specialization in creating ATS-friendly resumes. Your task is to list significant certifications based on the provided details. For each certification, ensure you include:

1. Certification Name: Clearly state the name of the certification.
2. Description: Provide a brief description of the certification and its relevance to your professional or academic career.

Ensure that the certifications are clearly presented and effectively highlight your qualifications.

To implement this:

If any of the certification details (e.g., descriptions) are not provided (i.e., None), omit those sections when filling out the template.

- **My information:**  
  {certifications}

- **Job Description:**  
  {job_description}
"""+ prompt_certifications_template


prompt_additional_skills = """
Act as an HR expert and resume writer with a specialization in creating ATS-friendly resumes. Your task is to list additional skills relevant to the job. For each skill, ensure you include:
Do not add any information beyond what is listed in the provided data fields. Only use the information provided in the 'languages', 'interests', and 'skills' fields to formulate your responses. Avoid extrapolating or incorporating details from the job description or other external sources.

1. **Skill Category**: Clearly state the category or type of skill.
2. **Specific Skills**: List the specific skills or technologies within each category.
3. **Proficiency and Experience**: Briefly describe your experience and proficiency level.

Ensure that the skills listed are relevant and accurately reflect your expertise in the field.

To implement this:
- If any of the skill details (e.g., languages, interests, skills) are not provided (i.e., `None`), omit those sections when filling out the template.


- **My information:**  
  {languages}
  {interests}
  {skills}

- **Job Description:**  
  {job_description}
"""+ prompt_additional_skills_template

summarize_prompt_template = """
As a seasoned HR expert, your task is to identify and outline the key skills and requirements necessary for the position of this job. Use the provided job description as input to extract all relevant information. This will involve conducting a thorough analysis of the job's responsibilities and the industry standards. You should consider both the technical and soft skills needed to excel in this role. Additionally, specify any educational qualifications, certifications, or experiences that are essential. Your analysis should also reflect on the evolving nature of this role, considering future trends and how they might affect the required competencies.

Rules:
Remove boilerplate text
Include only relevant information to match the job description against the resume

# Analysis Requirements
Your analysis should include the following sections:
Technical Skills: List all the specific technical skills required for the role based on the responsibilities described in the job description.
Soft Skills: Identify the necessary soft skills, such as communication abilities, problem-solving, time management, etc.
Educational Qualifications and Certifications: Specify the essential educational qualifications and certifications for the role.
Professional Experience: Describe the relevant work experiences that are required or preferred.
Role Evolution: Analyze how the role might evolve in the future, considering industry trends and how these might influence the required skills.

# Final Result:
Your analysis should be structured in a clear and organized document with distinct sections for each of the points listed above. Each section should contain:
This comprehensive overview will serve as a guideline for the recruitment process, ensuring the identification of the most qualified candidates.

# Job Description:
```
{text}
```

---

# Job Description Summary"""

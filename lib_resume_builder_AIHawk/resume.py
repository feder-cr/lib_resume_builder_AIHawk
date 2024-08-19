from dataclasses import dataclass, field
from typing import List, Dict, Any
import yaml

@dataclass
class PersonalInformation:
    name: str
    surname: str
    date_of_birth: str
    country: str
    city: str
    address: str
    phone_prefix: str
    phone: str
    email: str
    github: str
    linkedin: str

@dataclass
class Exam:
    name: str
    grade: str

@dataclass
class Education:
    degree: str
    university: str
    gpa: str
    graduation_year: str
    field_of_study: str
    exam: List[Exam]

@dataclass
class Responsibility:
    description: str

@dataclass
class Experience:
    position: str
    company: str
    employment_period: str
    location: str
    industry: str
    key_responsibilities: List[Responsibility]
    skills_acquired: List[str]

@dataclass
class Project:
    name: str
    description: str
    link: str

@dataclass
class Achievement:
    name: str
    description: str

@dataclass
class Language:
    language: str
    proficiency: str

class Resume:
    def __init__(self, yaml_str: str):
        try:
            # Parse the YAML string
            data = yaml.safe_load(yaml_str)
        except yaml.YAMLError as e:
            raise ValueError("Error parsing YAML file.") from e
        except AttributeError as ae:
            raise AttributeError(f"AttributeError while parsing YAML: {ae}") from ae
        except Exception as e:
            raise Exception(f"Unexpected error while parsing YAML: {e}") from e

        # Ensure the parsed data is a dictionary
        if not isinstance(data, dict):
            raise TypeError("YAML data must be a dictionary.")
        
        try:
            # Process personal information
            self.personal_information = PersonalInformation(**data['personal_information'])
        except KeyError as e:
            raise KeyError(f"Required field {e} is missing in personal_information data.") from e
        except TypeError as e:
            raise TypeError(f"Error in personal_information data: {e}") from e
        except AttributeError as ae:
            raise AttributeError(f"AttributeError in personal_information processing: {ae}") from ae
        except Exception as e:
            raise Exception(f"Unexpected error in personal_information processing: {e}") from e

        try:
            # Process education details
            self.education_details = [
                Education(
                    **{k: v for k, v in edu.items() if k != 'exam'},
                    exam=[Exam(name=k, grade=v) for k, v in edu.get('exam', {}).items()]
                ) for edu in data['education_details']
            ]
        except KeyError as e:
            raise KeyError(f"Required field {e} is missing in education_details data.") from e
        except TypeError as e:
            raise TypeError(f"Error in education_details data: {e}") from e
        except AttributeError as ae:
            raise AttributeError(f"AttributeError in education_details processing: {ae}") from ae
        except Exception as e:
            raise Exception(f"Unexpected error in education_details processing: {e}") from e

        try:
            # Process experience details
            self.experience_details = [
                Experience(
                    **{k: v for k, v in exp.items() if k not in ['key_responsibilities', 'skills_acquired']},
                    key_responsibilities=[
                        Responsibility(description=list(resp.values())[0]) for resp in exp.get('key_responsibilities', [])
                    ],
                    skills_acquired=exp.get('skills_acquired', [])
                ) for exp in data['experience_details']
            ]
        except KeyError as e:
            raise KeyError(f"Required field {e} is missing in experience_details data.") from e
        except TypeError as e:
            raise TypeError(f"Error in experience_details data: {e}") from e
        except AttributeError as ae:
            raise AttributeError(f"AttributeError in experience_details processing: {ae}") from ae
        except Exception as e:
            raise Exception(f"Unexpected error in experience_details processing: {e}") from e

        try:
            # Process projects
            self.projects = [Project(**proj) for proj in data.get('projects', [])]
        except TypeError as e:
            raise TypeError(f"Error in projects data: {e}") from e
        except AttributeError as ae:
            raise AttributeError(f"AttributeError in projects processing: {ae}") from ae
        except Exception as e:
            raise Exception(f"Unexpected error in projects processing: {e}") from e

        try:
            # Process achievements
            self.achievements = [Achievement(**ach) for ach in data.get('achievements', [])]
        except TypeError as e:
            raise TypeError(f"Error in achievements data: {e}") from e
        except AttributeError as ae:
            raise AttributeError(f"AttributeError in achievements processing: {ae}") from ae
        except Exception as e:
            raise Exception(f"Unexpected error in achievements processing: {e}") from e

        try:
            # Process certifications
            self.certifications = data.get('certifications', [])
            if not isinstance(self.certifications, list):
                raise TypeError("Certifications should be a list.")
        except TypeError as e:
            raise TypeError(f"Error in certifications data: {e}") from e
        except AttributeError as ae:
            raise AttributeError(f"AttributeError in certifications processing: {ae}") from ae
        except Exception as e:
            raise Exception(f"Unexpected error in certifications processing: {e}") from e

        try:
            # Process languages
            self.languages = [Language(**lang) for lang in data.get('languages', [])]
        except TypeError as e:
            raise TypeError(f"Error in languages data: {e}") from e
        except AttributeError as ae:
            raise AttributeError(f"AttributeError in languages processing: {ae}") from ae
        except Exception as e:
            raise Exception(f"Unexpected error in languages processing: {e}") from e

        try:
            # Process interests
            self.interests = data.get('interests', [])
            if not isinstance(self.interests, list):
                raise TypeError("Interests should be a list.")
        except TypeError as e:
            raise TypeError(f"Error in interests data: {e}") from e
        except AttributeError as ae:
            raise AttributeError(f"AttributeError in interests processing: {ae}") from ae
        except Exception as e:
            raise Exception(f"Unexpected error in interests processing: {e}") from e


        def format_dataclass(obj):
            return "\n".join(f"{field.name}: {getattr(obj, field.name)}" for field in obj.__dataclass_fields__.values())


    def __str__(self):

        return (f"Personal Information:\n{format_dataclass(self.personal_information)}\n\n"
            "Education Details:\n" + "\n".join(
                f"  - {edu.degree} in {edu.field_of_study} from {edu.university}, "
                f"GPA: {edu.gpa}, Graduation Year: {edu.graduation_year}\n"
                f"    Exams:\n" + "\n".join(f"      {exam.name}: {exam.grade}" for exam in edu.exam)
                for edu in self.education_details
            ) + "\n\n"
            "Experience Details:\n" + "\n".join(
                f"  - {exp.position} at {exp.company} ({exp.employment_period}), {exp.location}, {exp.industry}\n"
                f"    Key Responsibilities:\n" + "\n".join(f"      - {resp.description}" for resp in exp.key_responsibilities) + "\n"
                f"    Skills Acquired: {', '.join(exp.skills_acquired)}"
                for exp in self.experience_details
            ) + "\n\n"
            "Projects:\n" + "\n".join(
                f"  - {proj.name}: {proj.description}\n    Link: {proj.link}"
                for proj in self.projects
            ) + "\n\n"
            "Achievements:\n" + "\n".join(
                f"  - {ach.name}: {ach.description}"
                for ach in self.achievements
            ) + "\n\n"
            "Certifications: " + ", ".join(self.certifications) + "\n\n"
            "Languages:\n" + "\n".join(
                f"  - {lang.language} ({lang.proficiency})"
                for lang in self.languages
            ) + "\n\n"
            "Interests: " + ", ".join(self.interests)
        )

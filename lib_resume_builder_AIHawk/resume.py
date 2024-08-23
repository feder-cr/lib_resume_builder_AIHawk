from dataclasses import dataclass, field
from typing import List, Dict, Any
import yaml

from dataclasses import dataclass
from typing import List

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

    def __str__(self):
        return (f"Name: {self.name} {self.surname}\n"
                f"Date of Birth: {self.date_of_birth}\n"
                f"Country: {self.country}\n"
                f"City: {self.city}\n"
                f"Address: {self.address}\n"
                f"Phone: {self.phone_prefix} {self.phone}\n"
                f"Email: {self.email}\n"
                f"GitHub: {self.github}\n"
                f"LinkedIn: {self.linkedin}")

@dataclass
class Exam:
    name: str
    grade: str

    def __str__(self):
        return f"{self.name}: {self.grade}"

@dataclass
class Education:
    degree: str
    university: str
    gpa: str
    graduation_year: str
    field_of_study: str
    exam: List[Exam]

    def __str__(self):
        exams_str = '\n  '.join(str(exam) for exam in self.exam)
        return (f"Degree: {self.degree}\n"
                f"University: {self.university}\n"
                f"GPA: {self.gpa}\n"
                f"Graduation Year: {self.graduation_year}\n"
                f"Field of Study: {self.field_of_study}\n"
                f"Exams:\n  {exams_str}")

@dataclass
class Responsibility:
    description: str

    def __str__(self):
        return self.description

@dataclass
class Experience:
    position: str
    company: str
    employment_period: str
    location: str
    industry: str
    key_responsibilities: List[Responsibility]
    skills_acquired: List[str]

    def __str__(self):
        responsibilities_str = '\n  '.join(str(responsibility) for responsibility in self.key_responsibilities)
        skills_str = ', '.join(self.skills_acquired)
        return (f"Position: {self.position}\n"
                f"Company: {self.company}\n"
                f"Employment Period: {self.employment_period}\n"
                f"Location: {self.location}\n"
                f"Industry: {self.industry}\n"
                f"Key Responsibilities:\n  {responsibilities_str}\n"
                f"Skills Acquired: {skills_str}")

@dataclass
class Project:
    name: str
    description: str
    link: str

    def __str__(self):
        return (f"Project Name: {self.name}\n"
                f"Description: {self.description}\n"
                f"Link: {self.link}")

@dataclass
class Achievement:
    name: str
    description: str

    def __str__(self):
        return f"{self.name}: {self.description}"

@dataclass
class Language:
    language: str
    proficiency: str

    def __str__(self):
        return f"{self.language} (Proficiency: {self.proficiency})"


class Resume:
    def __init__(self, yaml_str: str):
        try:
            # Parse the YAML string
            data = yaml.safe_load(yaml_str)
            if not isinstance(data, dict):
                raise TypeError("YAML data must be a dictionary.")
            
            # Validate the structure of the YAML data
            self._validate_structure(data)
            
        except yaml.YAMLError as e:
            raise ValueError("Error parsing YAML file.") from e
        except TypeError as e:
            raise TypeError(f"YAML data is not a dictionary: {e}") from e
        except Exception as e:
            raise Exception(f"Unexpected error while parsing YAML: {e}") from e

        # Validate and process personal information
        try:
            self.personal_information = self._process_personal_information(data.get('personal_information', {}))
        except KeyError as e:
            raise KeyError(f"Required field {e} is missing in personal_information data.") from e
        except TypeError as e:
            raise TypeError(f"Error in personal_information data: {e}") from e
        except AttributeError as e:
            raise AttributeError(f"AttributeError in personal_information processing: {e}") from e
        except Exception as e:
            raise Exception(f"Unexpected error in personal_information processing: {e}") from e

        # Validate and process education details
        try:
            self.education_details = self._process_education_details(data.get('education_details', []))
        except KeyError as e:
            raise KeyError(f"Required field {e} is missing in education_details data.") from e
        except TypeError as e:
            raise TypeError(f"Error in education_details data: {e}") from e
        except AttributeError as e:
            raise AttributeError(f"AttributeError in education_details processing: {e}") from e
        except Exception as e:
            raise Exception(f"Unexpected error in education_details processing: {e}") from e

        # Validate and process experience details
        try:
            self.experience_details = self._process_experience_details(data.get('experience_details', []))
        except KeyError as e:
            raise KeyError(f"Required field {e} is missing in experience_details data.") from e
        except TypeError as e:
            raise TypeError(f"Error in experience_details data: {e}") from e
        except AttributeError as e:
            raise AttributeError(f"AttributeError in experience_details processing: {e}") from e
        except Exception as e:
            raise Exception(f"Unexpected error in experience_details processing: {e}") from e

        # Validate and process projects
        try:
            self.projects = self._process_projects(data.get('projects', []))
        except TypeError as e:
            raise TypeError(f"Error in projects data: {e}") from e
        except AttributeError as e:
            raise AttributeError(f"AttributeError in projects processing: {e}") from e
        except Exception as e:
            raise Exception(f"Unexpected error in projects processing: {e}") from e

        # Validate and process achievements
        try:
            self.achievements = self._process_achievements(data.get('achievements', []))
        except TypeError as e:
            raise TypeError(f"Error in achievements data: {e}") from e
        except AttributeError as e:
            raise AttributeError(f"AttributeError in achievements processing: {e}") from e
        except Exception as e:
            raise Exception(f"Unexpected error in achievements processing: {e}") from e

        # Validate and process certifications
        try:
            self.certifications = self._process_certifications(data.get('certifications', []))
        except TypeError as e:
            raise TypeError(f"Error in certifications data: {e}") from e
        except AttributeError as e:
            raise AttributeError(f"AttributeError in certifications processing: {e}") from e
        except Exception as e:
            raise Exception(f"Unexpected error in certifications processing: {e}") from e

        # Validate and process languages
        try:
            self.languages = self._process_languages(data.get('languages', []))
        except TypeError as e:
            raise TypeError(f"Error in languages data: {e}") from e
        except AttributeError as e:
            raise AttributeError(f"AttributeError in languages processing: {e}") from e
        except Exception as e:
            raise Exception(f"Unexpected error in languages processing: {e}") from e

        # Validate and process interests
        try:
            self.interests = self._process_interests(data.get('interests', []))
        except TypeError as e:
            raise TypeError(f"Error in interests data: {e}") from e
        except AttributeError as e:
            raise AttributeError(f"AttributeError in interests processing: {e}") from e
        except Exception as e:
            raise Exception(f"Unexpected error in interests processing: {e}") from e

    def _validate_structure(self, data: Dict[str, Any]):
        """
        Validate that the YAML data conforms to the expected structure.
        """
        expected_keys = {
            'personal_information': dict,
            'education_details': list,
            'experience_details': list,
            'projects': list,
            'achievements': list,
            'certifications': list,
            'languages': list,
            'interests': list
        }
        for key, expected_type in expected_keys.items():
            if key not in data:
                raise KeyError(f"Missing expected key: {key}")
            if not isinstance(data[key], expected_type):
                raise TypeError(f"Expected {key} to be of type {expected_type.__name__}, but got {type(data[key]).__name__}")

    def _process_personal_information(self, data: Dict[str, Any]) -> PersonalInformation:
        try:
            return PersonalInformation(**data)
        except TypeError as e:
            raise TypeError(f"Invalid data for PersonalInformation: {e}") from e
        except AttributeError as e:
            raise AttributeError(f"AttributeError in PersonalInformation: {e}") from e
        except Exception as e:
            raise Exception(f"Unexpected error in PersonalInformation processing: {e}") from e

    def _process_education_details(self, data: List[Dict[str, Any]]) -> List[Education]:
        education_list = []
        for edu in data:
            try:
                exams = [Exam(name=k, grade=v) for k, v in edu.get('exam', {}).items()]
                education = Education(
                    degree=edu['degree'],
                    university=edu['university'],
                    gpa=edu['gpa'],
                    graduation_year=edu['graduation_year'],
                    field_of_study=edu['field_of_study'],
                    exam=exams
                )
                education_list.append(education)
            except KeyError as e:
                raise KeyError(f"Missing field in education details: {e}") from e
            except TypeError as e:
                raise TypeError(f"Invalid data for Education: {e}") from e
            except AttributeError as e:
                raise AttributeError(f"AttributeError in Education: {e}") from e
            except Exception as e:
                raise Exception(f"Unexpected error in Education processing: {e}") from e
        return education_list

    def _process_experience_details(self, data: List[Dict[str, Any]]) -> List[Experience]:
        experience_list = []
        for exp in data:
            try:
                key_responsibilities = [
                    Responsibility(description=list(resp.values())[0])
                    for resp in exp.get('key_responsibilities', [])
                ]
                skills_acquired = [str(skill) for skill in exp.get('skills_acquired', [])]
                experience = Experience(
                    position=exp['position'],
                    company=exp['company'],
                    employment_period=exp['employment_period'],
                    location=exp['location'],
                    industry=exp['industry'],
                    key_responsibilities=key_responsibilities,
                    skills_acquired=skills_acquired
                )
                experience_list.append(experience)
            except KeyError as e:
                raise KeyError(f"Missing field in experience details: {e}") from e
            except TypeError as e:
                raise TypeError(f"Invalid data for Experience: {e}") from e
            except AttributeError as e:
                raise AttributeError(f"AttributeError in Experience: {e}") from e
            except Exception as e:
                raise Exception(f"Unexpected error in Experience processing: {e}") from e
        return experience_list

    def _process_projects(self, data: List[Dict[str, Any]]) -> List[Project]:
        project_list = []
        for proj in data:
            try:
                project = Project(
                    name=proj['name'],
                    description=proj['description'],
                    link=proj['link']
                )
                project_list.append(project)
            except KeyError as e:
                raise KeyError(f"Missing field in project details: {e}") from e
            except TypeError as e:
                raise TypeError(f"Invalid data for Project: {e}") from e
            except AttributeError as e:
                raise AttributeError(f"AttributeError in Project: {e}") from e
            except Exception as e:
                raise Exception(f"Unexpected error in Project processing: {e}") from e
        return project_list

    def _process_achievements(self, data: List[Dict[str, Any]]) -> List[Achievement]:
        achievement_list = []
        for ach in data:
            try:
                achievement = Achievement(**ach)
                achievement_list.append(achievement)
            except KeyError as e:
                raise KeyError(f"Missing field in achievements data: {e}") from e
            except TypeError as e:
                raise TypeError(f"Invalid data for Achievement: {e}") from e
            except AttributeError as e:
                raise AttributeError(f"AttributeError in Achievement: {e}") from e
            except Exception as e:
                raise Exception(f"Unexpected error in Achievement processing: {e}") from e
        return achievement_list

    def _process_certifications(self, data: Any) -> List[str]:
        if not isinstance(data, list):
            raise TypeError("Certifications should be a list.")
        return [str(cert) for cert in data]

    def _process_languages(self, data: List[Dict[str, Any]]) -> List[Language]:
        language_list = []
        for lang in data:
            try:
                language = Language(**lang)
                language_list.append(language)
            except KeyError as e:
                raise KeyError(f"Missing field in languages data: {e}") from e
            except TypeError as e:
                raise TypeError(f"Invalid data for Language: {e}") from e
            except AttributeError as e:
                raise AttributeError(f"AttributeError in Language: {e}") from e
            except Exception as e:
                raise Exception(f"Unexpected error in Language processing: {e}") from e
        return language_list

    def _process_interests(self, data: Any) -> List[str]:
        if not isinstance(data, list):
            raise TypeError("Interests should be a list.")
        return [str(interest) for interest in data]

    def __str__(self):
        def format_dataclass(obj):
            return "\n".join(f"{field.name}: {getattr(obj, field.name)}" for field in obj.__dataclass_fields__.values())

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

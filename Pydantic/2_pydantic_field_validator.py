from pydantic import BaseModel, field_validator, EmailStr
from typing import List

class Patient(BaseModel):
    name: str
    age: int
    email: EmailStr
    married: bool
    allergies: List[str]
    
    # like we want email from specific domain only
    @field_validator('email')
    @classmethod
    def email_validator(cls, value):
        valid_domains = ['hdfc.com', 'icici.com']
        
        domain_name = value.split('@')[-1]
        
        if domain_name not in valid_domains:
            raise ValueError('Not a valid email')
        return value
    
    
    # like we want name always in capital letter
    @field_validator('name')
    @classmethod
    def name_upper(cls, value):
        return value.upper()


def createPatient(patient: Patient): 
    print(patient.name)
    print(patient.age)
    print(patient.married)
    print(patient.email)
    print(patient.allergies)
    print("created")
    
patient_info = {'name': "Aastha", 'age': '18','email': "abc@hdfc.com", 'married': False, 'allergies': ['cold', 'dust']}

patient1 = Patient(**patient_info)

createPatient(patient1)


# field_validator work on a single data, it is used to perform specific validation
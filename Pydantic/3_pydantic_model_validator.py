from pydantic import BaseModel, EmailStr, model_validator
from typing import List, Dict

class Patient(BaseModel):
    name: str
    age: int
    email: EmailStr
    married: bool
    allergies: List[str]
    contact_details: Dict[str,str]
    
    @model_validator(mode='after') #It does not require any specific field name, because here we work on whole pydantic model
    def validate_emergency_contact(cls, model):
        if model.age > 60 and 'emergency' not in model.contact_details:
            raise ValueError("Patient older than 60 must have an emergency contact")
        return model

def createPatient(patient: Patient): 
    print(patient.name)
    print(patient.age)
    print(patient.married)
    print(patient.email)
    print(patient.allergies)
    print("created")
    
patient_info = {'name': "Aastha", 'age': '18','email': "abc@hdfc.com", 'married': False, 'allergies': ['cold', 'dust'], 'contact_details': {"phone": "7860075090"}}

patient1 = Patient(**patient_info)

createPatient(patient1)


# field_validator work on a single data, it is used to perform specific validation
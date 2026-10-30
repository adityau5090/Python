from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name: Annotated[str, Field(max_length=50, title="Name of the patient", description="Give the name of patient in less then 50 chars")]
    email: EmailStr
    age: Annotated[int, Field(strict=True)]
    weight: float = Field(gt=0, lt=200)
    married: bool
    linkdin: AnyUrl
    allergies: Annotated[Optional[List[str]], Field(default=None, max_length=5)]
    contact_details: Dict[str,str]
    
def insert_patient(patient: Patient):
    print(patient.name)
    print(patient.email)
    print(patient.age)
    print(patient.linkdin)
    print(patient.allergies)
    print('inserted')
    
patient_info = {'name': 'nitish', 'age': 30, 'email': "abc@gmail.com",'linkdin': "http://linkdin.com/322", 'weight': 70.5, 'married': True, 'contact_details': {'email': 'abc@gmail.com', 'phone': '678899776'}, 'allergies': ["dust", "love", "sex", "fuck", "kiss",]}

patient1 = Patient(**patient_info)

insert_patient(patient1)
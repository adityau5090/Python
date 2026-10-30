from pydantic import BaseModel, EmailStr, Field, computed_field
from typing import Annotated

class Patient(BaseModel):
    name: str
    email: EmailStr
    age: Annotated[int, Field(strict=True)]
    weight: float = Field(gt=0, lt=200, strict=True)   # in kg
    height: float # in meter
    married: bool
    
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2), 2)
        return bmi
    
    
def created(patient: Patient):
    print(patient.name)
    print(patient.email)
    print(patient.age)
    print(patient.weight)
    print(patient.height)
    print(patient.bmi)
    print(patient.married)
    
patient_info = {'name': 'Pasta', "email": "astha@gmail.com", "age": 18, "weight": 40.0, 'height': 1.55, 'married': 'false'}

patient1 = Patient(**patient_info)

created(patient1)
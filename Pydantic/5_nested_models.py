from pydantic import BaseModel

class Address(BaseModel):
    city: str
    state: str
    pin: str
    

class Patient(BaseModel):
    name: str
    gender: str
    age: int
    address: Address
    
address_dict = {'city': 'gurgaon', 'state': 'haryana', 'pin': '221115'}

address1 = Address(**address_dict)

patient_info = {'name': 'Devil', 'gender': 'male', 'age': 24, 'address': address1}

patient1 = Patient(**patient_info)

def printPatient(patient: Patient):
    print(patient.name)
    print(patient.gender)
    print(patient.age)
    print(patient.address.city)
    print(patient.address.state)
    print(patient.address.pin)
    
printPatient(patient1)
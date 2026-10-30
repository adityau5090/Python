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

temp = patient1.model_dump()
# print(temp)
# print(type(temp))


temp2 = patient1.model_dump_json()
# print(temp2)
# print(type(temp2))


temp3 = patient1.model_dump(include=['name', 'gender'])
print(temp3)

temp4 = patient1.model_dump(exclude=['name', 'gender'])
print(temp4)

temp5 = patient1.model_dump(exclude={'address':['state']})
print(temp5)
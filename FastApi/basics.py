from fastapi import FastAPI, Path, HTTPException, Query
import json
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
from fastapi.responses import JSONResponse

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description="ID of the patient", examples=['P001', 'P002'])]
    name: Annotated[str, Field(..., description="Name of the patient")]
    city: Annotated[str, Field(..., description="City of the patient")]
    age:  Annotated[int, Field(..., gt=0, lt=120, description="Age of the patient", strict=True, )]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description="Gender of patient")]
    height: Annotated[float, Field(..., gt=0, description="Height of the patient in meters")]
    weight: Annotated[float, Field(..., gt=0, description="Weight of the patient in kg")]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2), 2)
        return bmi
    
    @computed_field
    @property
    def vedict(self) -> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Okay'
        elif self.bmi < 30:
            return 'Normal'
        else:
            return 'Obese'
 
 
class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]       
    city: Annotated[Optional[str], Field(default=None)]       
    age: Annotated[Optional[int], Field(default=None, strict=True, gt=0)]       
    gender: Annotated[Optional[Literal["male", 'female', 'other']], Field(default=None)]     
    height: Annotated[Optional[float], Field(default=None, gt=0)]  
    weight: Annotated[Optional[float], Field(default=None, gt=0)]  
    
        
def load_data():
    with open("patients.json", 'r') as f:
        data = json.load(f);
    return data

def save_data(data):
    with open("patients.json", 'w') as f:
        json.dump(data, f)
        
@app.get("/")
def hello():
    return {'message': "Namaste Duniya"}

@app.get("/about")
def about():
    return {'message': "CampusX is an education platform"}

@app.get("/view")
def view():
    return load_data()

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(..., description="ID of the patient in the DB", example="P001")):
    data = load_data()
    
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get("/sort")
def sort_patient(sort_by: str = Query(..., description="Sort on the basis of height, weight or bmi"), order: str = Query('asc', description="Sort in asc or desc order")):
    valid_fields = ['height', 'weight', 'bmi']
    
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid field select from {valid_fields}") 
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail=f"Invalid order, select between asc or desc")
    
    data = load_data()
    sort_order = True if order=='desc' else False
    
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)
    
    return sorted_data

@app.post("/create")
def create_patient(patient: Patient):
    data = load_data()
    
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exist with this id')
    
    data[patient.id] = patient.model_dump(exclude=['id']) # convert pydantic object into python dict
    
    save_data(data) 
    
    return JSONResponse(status_code=201, content={'message': 'patient created successfully'})

@app.put("/edit/{patient_id}")
def update(patient_id: str, patient_udate: PatientUpdate):
    data = load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=400, detail='Patient not found')
    
    existing_patient_info = data[patient_id]
    
    updated_patient_info = patient_udate.model_dump(exclude_unset=True) # only convert those data in python dict which user explicitly sends
    
    #here we set the new values
    for key,val in updated_patient_info.items():
        existing_patient_info[key] = val
        
    # but now we got a problem that bmi and verdict are still same we need to update them too
    # so what we do -> we convert our updated data into Patien object so it calculate bmi and verdict again
    existing_patient_info['id'] = patient_id
    patient_pydentic_object = Patient(**existing_patient_info)  
    
    data[patient_id] = patient_pydentic_object.model_dump(exclude=['id'])
    
    save_data(data)
    
    return JSONResponse(status_code=201, content={'message': "Patient data updated"})

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    
    data = load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=400, detail="Patient not found with this Id")
    
    del data[patient_id] 
    
    save_data(data)
    
    return JSONResponse(status_code=201, content={'message': "Patient deleted"})
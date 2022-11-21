import json
from typing import Dict, Optional
from bson.objectid import ObjectId
# from database import client
from fastapi import FastAPI, Path, Query, HTTPException, status

from models import Employee
from mongoengine import connect, disconnect
from mongoengine.queryset.visitor import Q
from pydantic import BaseModel
from setting import tutorial1
import os
from dotenv import load_dotenv

load_dotenv()
URI = os.getenv('DATABASE_URL')


class NewEmployee(BaseModel):
    emp_id: int
    Name: str
    age: int


class UpdateEmployee(BaseModel):
    emp_id: Optional[int]
    Name: Optional[str]
    age: Optional[int]


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}


app = FastAPI()
connect(host=URI)


@app.get('/')
async def hello_world():
    return {"Hello": "world"}


@app.get("/get_all_employees")
def get_all_employees():
    employees = json.loads(Employee.objects().to_json())
    return {"employees": employees}


@app.get('/employee/{emp_id}')
def get_employee(emp_id: int = Path(..., gt=0)):
    employee = Employee.objects.get(emp_id=emp_id)
    employee_dict = {
        "emp_id": {
            "emp_id": employee.emp_id,
            "name": employee.Name,
            "age": employee.age

        }
    }
    return employee_dict


@app.get('/search_employee')
def search_employees(name: str, age: int = Query(None, gt=18)):
    employees = json.loads(Employee.objects.filter(
        Q(Name__icontains=name) | Q(age=age)).to_json())
    return {"employees": employees}


@app.post('/add_empolyee')
def add_employees(emp: NewEmployee):
    new_employee = Employee(emp_id=emp.emp_id, Name=emp.Name, age=emp.age)
    new_employee.save()
    return {"messagae": "employee has been"}


@app.put('/update/{emp_id}')
def update_employee(emp_id: int = Path(..., gt=0)):

    if not ObjectId.is_valid(emp_id):
        raise HTTPException(status_code=404,
                            detail=f"Invalid id: {emp_id}")

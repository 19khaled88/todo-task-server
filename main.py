
import uuid
from typing import Optional

from database import get_db
from fastapi import FastAPI
from pydantic import BaseModel


class Todo(BaseModel):
    id: int
    skill: str
    status: str

    # class Config:
    #     orm_mode = True


# def student_helper(student) -> dict:
#     return {
#         "id": str(student["_id"]),
#         "fullname": student["fullname"],
#         "email": student["email"],
#         "course_of_study": student["course_of_study"],
#         "year": student["year"],
#         "GPA": student["gpa"],
#     }

def todo_helper(todo) -> dict:
    return {
        "id": str(todo["id"]),
        "skill": todo["skill"],
        "status": todo["status"],

    }


class TodoUpdate(BaseModel):
    id: int
    skill: Optional[str]
    status: Optional[str]


app = FastAPI()


@app.get("/")
def home():
    return {"message": uuid.uuid1()}


@app.get("/todo/{id}", response_model=Todo)
def get_single_todo(id: int):
    db = get_db()
    col = db.get_collection("Todos")
    std = col.find_one({"id": id})
    return std


@app.get('/todos')
async def get_all_todo():
    todos = []
    db = get_db()
    col = db.get_collection("Todos")
    for todo in col.find():
        todos.append(todo_helper(todo))
    return todos


@app.post("/todo")
def create_todo(data: Todo):
    db = get_db()
    col = db.get_collection("Todos")
    new_todo = col.insert_one(data.dict())
    if new_todo .acknowledged:
        return {"message": f"{data.skill} Todos  created"}
    return {"message": "error occured while creating a todo"}


# @app.put("/student")
# def update_student(data: StudnetsUpdate):
#     db = get_db()
#     col = db.get_collection("Students")
#     std_dict = {k: v for k, v in data.dict().items() if v is not None}
#     result = col.update_one({"id": data.id}, {"$set": std_dict})
#     if result.modified_count == 1:
#         return {"message": f"Students updated."}
#     return {"message": f"error occured while updating student {data.name}"}

@app.put("/todo")
def update_todo(data: TodoUpdate):
    db = get_db()
    col = db.get_collection("Todos")
    todo_dict = {k: v for k, v in data.dict().items() if v is not None}
    result = col.update_one({"id": data.id}, {"$set": todo_dict})
    if result.modified_count == 1:
        return {"message": f"Todo updated."}
    return {"message": f"error occured while updating todo {data.skill}"}


@app.delete("/todo/{id}")
def delete_todo(id: int):
    db = get_db()
    col = db.get_collection("Todos")
    result = col.delete_one({"id": id})
    if result.deleted_count == 1:
        return {"message": "Todo deleted"}
    return {"message": "error occured while deleting todo."}

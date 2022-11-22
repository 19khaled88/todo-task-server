
import uuid
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

from database import get_db
from fastapi import FastAPI
from pydantic import BaseModel


class Todo(BaseModel):
    id: int
    todo: str
    status: str


class CreateTodo(BaseModel):
    id: int
    todo: str
    status: str

    # class Config:
    #     orm_mode = True


def todo_helper(todo) -> dict:
    return {
        "id": int(todo["id"]),
        "todo": todo["todo"],
        "status": todo["status"],

    }


class TodoUpdate(BaseModel):
    id: int
    todo: Optional[str]
    status: Optional[str]


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


# @app.post("/todo")
# def create_todo(data: Todo):
#     db = get_db()
#     col = db.get_collection("Todos")
#     new_todo = col.insert_one(data.dict())
#     if new_todo .acknowledged:
#         return {"message": f"{data.skill} Todos  created", "status": "200","success":"true"}
#     return {"message": "error occured while creating a todo", "status": "400","success":"false"}


@app.get('/matchTodo/{status}')
async def get_matched_todo(status: str):
    todos = []
    db = get_db()
    col = db.get_collection("Todos")
    for todo in col.find():
        if todo['status'] == status:

            todos.append(todo_helper(todo))

        # todos.append(todo_helper(todo))

    return todos


@app.post("/todo")
def create_todo(data: CreateTodo):

    db = get_db()
    col = db.get_collection("Todos")
    new_todo = col.insert_one(data.dict())

    if new_todo .acknowledged:
        return {"message": f"{data.todo} Todos  created", "status": "200", "success": "true"}
    return {"message": "error occured while creating a todo", "status": "400", "success": "false"}

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
        return {"message": f"Todo updated.", "status": "200", "success": "true"}
    return {"message": f"error occured while updating todo {data.todo}", "status": "400", "success": "false"}


@app.delete("/todo/{id}")
def delete_todo(id: int):

    db = get_db()
    col = db.get_collection("Todos")
    result = col.delete_one({"id": id})
    if result.deleted_count == 1:
        return {"message": "Todo deleted", "status": "200", "success": "true"}
    return {"message": "error occured while deleting todo.", "status": "400", "success": "false"}

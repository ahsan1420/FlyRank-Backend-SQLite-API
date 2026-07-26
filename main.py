from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import (
    initialize_database,
    get_all_tasks,
    get_task_by_id,
    create_task
)

app = FastAPI(
    title="Task API",
    description="SQLite CRUD API",
    version="2.0"
)


class TaskCreate(BaseModel):
    title: str


@app.on_event("startup")
def startup():
    initialize_database()


@app.get("/")
def home():
    return {
        "message": "SQLite Database Connected"
    }


@app.get("/tasks")
def read_tasks():
    return get_all_tasks()


@app.get("/tasks/{task_id}")
def read_task(task_id: int):

    task = get_task_by_id(task_id)

    if task:
        return task

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )


@app.post("/tasks", status_code=201)
def add_task(task: TaskCreate):

    if not task.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    return create_task(task.title)

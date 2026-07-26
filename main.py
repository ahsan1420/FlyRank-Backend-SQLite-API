from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from database import (
    initialize_database,
    get_all_tasks,
    get_task_by_id,
    create_task,
    update_task,
    delete_task
)

app = FastAPI(
    title="Task API",
    description="SQLite CRUD API",
    version="2.0"
)


class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: str
    done: bool


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


@app.put("/tasks/{task_id}")
def edit_task(task_id: int, task: TaskUpdate):

    if not task.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    updated = update_task(
        task_id,
        task.title,
        task.done
    )

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return updated


@app.delete("/tasks/{task_id}", status_code=204)
def remove_task(task_id: int):

    deleted = delete_task(task_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return

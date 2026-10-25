from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# in-memory database to store tasks
tasks = [
    {
    "id": 1,
    "title": "Task 1",
    "done": False
    },
    {
    "id": 2, 
    "title": "Task 2", 
    "done": False
    },
    {
    "id": 3, 
    "title": "Task 3",
    "done": True
    }
]

class Tasks(BaseModel):
    id: int
    title: str
    done: bool

#root directory
@app.get("/")
def get_task():
    return {
        "status": "success",
        "message": "welcome to the backend server"
    }

#Fetch all tasks
@app.get("/tasks")
def get_tasks():
    return tasks

#Fetch a specific task by its ID using a path parameter.
@app.get("/tasks/{id}")
def read_task(id: int):
    for task in tasks:                   #loop through the tasks list to find a task with the matching ID
        if task["id"] == id:             #Check matching ID
            return task
    return {"error": f"Task {id} not found"}

#Create a task
@app.post("/tasks")
def create_task(task: Tasks):
    new_task = {
        "id": len(tasks) + 1,
        "title": task.title,
        "done": task.done
    }
    tasks.append(new_task)
    return new_task

#Put Endpoint
@app.put("/tasks/{id}")
def update_task(id: int, updated_data: Tasks):
    for task in tasks:
        if task["id"] == id:
            task["title"] = updated_data.title
            task["done"] = updated_data.done
            return {f"Task {id} has been updated"}
    return {f"Task {id} is not found"}

#Delete a specific task by its ID using a path parameter.
@app.delete("/tasks/{id}")
def delete_task(id: int):
    for task in tasks:
        if task["id"] == id:
            tasks.remove(task)
            return {"message": f"Task {id} deleted"}
    return {"error": f"Task {id} not found"}

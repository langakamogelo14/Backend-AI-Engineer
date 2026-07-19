from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse

crud = FastAPI()

#in-memory database to store tasks
tasks = [
    {"id": 1, "title": "Task 1", "done": False},
    {"id": 2, "title": "Task 2", "done": False},
    {"id": 3, "title": "Task 3", "done": True}
]

@crud.get("/")
def read_item():
    return {
        "name": "Task API", 
        "version": "1.0", 
        "endpoints": ["/tasks"],
        "health": "/health"
    }

@crud.get("/health")
def health_check():
    return {"status": "ok"}

#Endpoint to return the whole list
@crud.get("/tasks")
def get_tasks():
    return tasks

#Returns a single task from the list using its ID
@crud.get("/tasks/{id}")             
def read_tasks(id:int):
    for task in tasks:
        if task["id"] == id:
            return task
    return JSONResponse(
        status_code=404,
        content={"error": f"Task {id} not found"}
        )

#User task
@crud.post("/tasks")
def create_task(task_data: dict):
    #Validate the input (The server never trusts the client!)
    #We use .get() so it doesn't crash if "title" is missing entirely
    title = task_data.get("title", "").strip()
    
    if not title:
        return JSONResponse(
            status_code=400, 
            content={"error": "Title is required and cannot be empty"}
        )
    
    #Figure out the next free ID
    next_id = 1
    if tasks:  # If the list isn't empty, find the highest ID and add 1
        next_id = max(t["id"] for t in tasks) + 1
        
    #Create the new task dictionary
    new_task = {
        "id": next_id,
        "title": title,
        "done": False
    }
    
    #Save it to our in-memory database
    tasks.append(new_task)
    
    #Return the receipt (status 201 Created)
    return JSONResponse(
        status_code=201, 
        content=new_task
        )  #curl.exe -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d "{\"title\":\"Buy milk\"}"

#Endpoint to update a task
@crud.put("/tasks/{task_id}")
def update_task(task_id: int, task_data: dict):
    #Check for completely empty body
    if not task_data:
        return JSONResponse(status_code=400, content={"error": "Request body cannot be empty"})
    
    #Find the task
    for task in tasks:
        if task["id"] == task_id:
            #Update title if provided (and not empty)
            if "title" in task_data:
                title = str(task_data["title"]).strip()
                if not title:
                    return JSONResponse(status_code=400, content={"error": "Title cannot be empty"})
                task["title"] = title
            
            #Update done status if provided
            if "done" in task_data:
                task["done"] = bool(task_data["done"])
                
            return task
            
    #If loop finishes without finding the task
    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})

#Endpoint to delete a task
@crud.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)  # Remove the task from the list
            return Response(status_code=204)  # 204 means "Success, but I have no data to send back"
            
    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})




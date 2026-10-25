import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

class Tasks(BaseModel):
    id: int
    title: str
    done: bool


#Create the database
def init_db():
    #Connect to the database
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    #Create the database table for 'tasks'
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        done BOOLEAN
        )
    """)
    
    #Check the amount of entries already in the db
    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]
    
    #if the table is empty create the default db with 3 entries
    if count == 0:
        cursor.execute("INSERT INTO tasks (title, done) VALUES ('Task 1', 0)")
        cursor.execute("INSERT INTO tasks (title, done) VALUES ('Task 2', 0)")
        cursor.execute("INSERT INTO tasks (title, done) VALUES ('Task 3', 1)")
        conn.commit()
    
    conn.close()
    
init_db()        #Run the database




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
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, title, done FROM tasks")
    rows = cursor.fetchall()
    conn.close()
    
    #Convert the db rows to the API's format (Dictionary)
    task_list = []
    for row in rows:
        task_list.append({
            "id": row[0],
            "title": row[1],
            "done": bool(row[2])    #convert 0/1 to False/True
        })  
    return task_list


#Fetch a specific task by its ID using a path parameter.
@app.get("/tasks/{id}")
def read_task(id: int):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, title, done FROM tasks WHERE id = ?", (id,))
    row = cursor.fetchone()
    conn.close()
    
    #Error message the row is not found
    if row is None:
        return {f"error": "Task not found"}
    
    return {
        "id": row[0],
        "title": row[1],
        "done": bool(row[2])
    }


#Create a task
@app.post("/tasks")
def create_task(task: Tasks):
    if not task.title or task.title.strip() == "":
        return {f"Missing Title"}
    
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    
    # Insert the new task into the database
    cursor.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)", (task.title, task.done))
    conn.commit()
    
    # Grab the ID number that SQLite automatically created for this new row
    new_id = cursor.lastrowid
    conn.close()
      
    return {
        "id": new_id,
        "title": task.title,
        "done": task.done
    }



#Put Endpoint
@app.put("/tasks/{id}")
def update_task(id: int, updated_data: Tasks):
    if not updated_data.title or updated_data.title.strip() == "":
        return {f"Error, Missing title"}
    
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    # Check if the task exists first
    cursor.execute("SELECT id FROM tasks WHERE id = ?", (id,))
    if cursor.fetchone() is None:
        conn.close()
        return {f"Error, Task not found"}
    
    # Update the row in the database
    cursor.execute(
        "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
        (updated_data.title, updated_data.done, id)
    )
    
    conn.commit()
    conn.close()

    return {
        "id": id,
        "title": updated_data.title,
        "done": updated_data.done
    }
    
 
#Delete a specific task by its ID using a path parameter.
@app.delete("/tasks/{id}")
def delete_task(id: int):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    
    #Check if the task exists first
    cursor.execute("SELECT id FROM tasks WHERE id = ?", (id,))
    if cursor.fetchone() is None:
        conn.close()
        return {f"Task not found"}
        
    # Delete the row from the database
    cursor.execute("DELETE FROM tasks WHERE id = ?", (id,))
    conn.commit()
    conn.close()
   
    return {f"Task {id} deleted"}


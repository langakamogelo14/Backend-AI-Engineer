# FastAPI In-Memory Task Manager API

A lightweight, beginner-friendly RESTful CRUD (Create, Read, Update, Delete) API built with [FastAPI](https://fastapi.tiangolo.com/) and [Pydantic](https://docs.pydantic.dev/). This project uses an in-memory list to store, retrieve, update, and delete tasks.

---

## Features

- **Root Greeting**: Quick health check and welcome message.
- **Get All Tasks**: Retrieve the full list of tasks.
- **Get Single Task**: Fetch a specific task by its unique ID.
- **Create Task**: Add a new task with automatic ID assignment.
- **Update Task**: Modify the title and completion status of an existing task.
- **Delete Task**: Remove a task by its ID.
- **Interactive Documentation**: Auto-generated Swagger UI and ReDoc endpoints.

---

## Project Structure

```text
├── main.py          # FastAPI application logic and routes
├── README.md        # Project documentation
└── requirements.txt # Project dependencies
```

---

## Installation & Setup

### 1. Prerequisites
Ensure you have Python 3.8+ installed on your system.

### 2. Clone or Create the Project Directory
```bash
mkdir fastapi-task-manager
cd fastapi-task-manager
```

### 3. Set Up a Virtual Environment (Recommended)
```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows (Command Prompt / PowerShell)
python -m venv venv
venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install fastapi uvicorn
```

---

## Running the Application

Save your Python code as `main.py` and run the development server using `uvicorn`:

```bash
uvicorn main:app --reload
```

- `--reload`: Enables hot-reloading so the server automatically restarts whenever you save changes to the code.
- By default, the application runs on: **`http://127.0.0.1:8000`**

---

## Interactive API Documentation

FastAPI provides built-in documentation interfaces out of the box:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) (Interactive testing interface)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) (Clean, structured documentation)

---

## Data Models

### Task Object
| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | `int` | Unique identifier for the task |
| `title` | `str` | Title / description of the task |
| `done` | `bool` | Completion status (`true` or `false`) |

---

## API Endpoints Reference

### 1. Root Welcome
- **Method:** `GET`
- **Path:** `/`
- **Description:** Returns a welcome message.
- **Response (`200 OK`):**
  ```json
  {
    "status": "success",
    "message": "welcome to the backend server"
  }
  ```

---

### 2. Get All Tasks
- **Method:** `GET`
- **Path:** `/tasks`
- **Description:** Returns all tasks stored in the database.
- **Response (`200 OK`):**
  ```json
  [
    {
      "id": 1,
      "title": "Task 1",
      "done": false
    },
    {
      "id": 2,
      "title": "Task 2",
      "done": false
    },
    {
      "id": 3,
      "title": "Task 3",
      "done": true
    }
  ]
  ```

---

### 3. Get a Specific Task
- **Method:** `GET`
- **Path:** `/tasks/{id}`
- **Description:** Retrieve a single task matching the given path parameter `id`.
- **Response (`200 OK` - Found):**
  ```json
  {
    "id": 2,
    "title": "Task 2",
    "done": false
  }
  ```
- **Response (Not Found):**
  ```json
  {
    "error": "Task 99 not found"
  }
  ```

---

### 4. Create a Task
- **Method:** `POST`
- **Path:** `/tasks`
- **Description:** Adds a new task. The `id` is automatically calculated based on the current length of the task list.
- **Request Body:**
  ```json
  {
    "id": 0,
    "title": "Buy groceries",
    "done": false
  }
  ```
  *(Note: The `id` provided in the request body is overwritten by the server's auto-generated ID).*
- **Response (`200 OK`):**
  ```json
  {
    "id": 4,
    "title": "Buy groceries",
    "done": false
  }
  ```

---

### 5. Update a Task
- **Method:** `PUT`
- **Path:** `/tasks/{id}`
- **Description:** Updates the `title` and `done` values for the specified task.
- **Request Body:**
  ```json
  {
    "id": 1,
    "title": "Task 1 (Updated)",
    "done": true
  }
  ```
- **Response (Found):**
  ```json
  [
    "Task 1 has been updated"
  ]
  ```
- **Response (Not Found):**
  ```json
  [
    "Task 99 is not found"
  ]
  ```

---

### 6. Delete a Task
- **Method:** `DELETE`
- **Path:** `/tasks/{id}`
- **Description:** Deletes the task with the specified ID.
- **Response (`200 OK` - Success):**
  ```json
  {
    "message": "Task 1 deleted"
  }
  ```
- **Response (Not Found):**
  ```json
  {
    "error": "Task 99 not found"
  }
  ```

---

## Important Development Notes

1. **In-Memory Volatility**: The data stored in the `tasks` list resides entirely in RAM. Restarting or stopping the server resets the list to the original 3 default tasks.
2. **Recommended Future Enhancements**:
   - **Separate Input Schema**: Create a separate Pydantic model for task creation without requiring the client to send a dummy `id`.
   - **Standard HTTP Exceptions**: Use `raise HTTPException(status_code=404, detail="Task not found")` instead of returning error dictionaries to ensure standard HTTP status codes.
   - **Persistent Storage**: Integrate SQLite, PostgreSQL, or MongoDB with an ORM like SQLAlchemy or SQLModel for permanent data storage.
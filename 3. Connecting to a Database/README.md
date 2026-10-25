# FastAPI + SQLite Task Manager API (Phase 2)

A RESTful CRUD (Create, Read, Update, Delete) API built with [FastAPI](https://fastapi.tiangolo.com/), [Pydantic](https://docs.pydantic.dev/), and Python's built-in `sqlite3` library. 

In Phase 2 of this project, the volatile in-memory task list from Phase 1 has been replaced with a persistent **SQLite database (`tasks.db`)**. The API endpoints and client behavior remain consistent while ensuring that all tasks survive server restarts.

---

## Architecture Overview

* **Phase 1:** `Client` $\rightarrow$ `FastAPI` $\rightarrow$ `In-Memory List` *(Data lost on restart)*
* **Phase 2:** `Client` $\rightarrow$ `FastAPI` $\rightarrow$ `SQLite Database (tasks.db)` *(Data persists permanently)*

---

## Why SQLite Was Chosen

1. **Zero Configuration & Serverless**: SQLite does not require installing or running a separate database server process. It comes built directly into Python via the standard `sqlite3` module.
2. **Single-File Persistence**: The entire database (tables, schemas, and records) is stored inside a single portable file (`tasks.db`), making it ideal for local development, rapid prototyping, and learning relational SQL fundamentals.
3. **Seamless SQL Transition**: Using standard SQL queries (`SELECT`, `INSERT`, `UPDATE`, `DELETE`) in SQLite makes it straightforward to migrate to larger client-server databases like PostgreSQL or MySQL in the future without changing the API layer.

---

## Database Storage & Automatic Initialization

* **Where the Database File is Stored**: The database is stored locally in the root directory of this project folder as **`tasks.db`**.
* **Automatic Setup (`init_db`)**: When the FastAPI server starts up:
  1. It automatically creates `tasks.db` if the file does not already exist.
  2. It executes `CREATE TABLE IF NOT EXISTS tasks` to create the `tasks` table with columns `id` (`INTEGER PRIMARY KEY AUTOINCREMENT`), `title` (`TEXT`), and `done` (`BOOLEAN`).
  3. It checks the current row count (`SELECT COUNT(*) FROM tasks`) and inserts 3 starter tasks **only if the table is completely empty** (`count == 0`), preventing duplicate entries on subsequent server restarts.

---

## Project Structure

```text
├── main.py          # FastAPI application and SQLite database logic
├── tasks.db         # Auto-generated SQLite database file
├── Screenshot/      # Folder containing project & DB viewer screenshots
└── README.md        # Project documentation
```

---

## How to Start the Project

### 1. Prerequisites
Ensure you have **Python 3.8+** installed on your computer.

### 2. Install Dependencies
```bash
pip install fastapi uvicorn
```

### 3. Run the Development Server
```bash
uvicorn main:app --reload
```
* The server will start at: **`http://127.0.0.1:8000`**
* `tasks.db` will automatically be created and seeded in the same folder on the first run.

### 4. Interactive API Documentation
* **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Database Schema (`tasks` Table)

| Column | SQLite Type | Python Type | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER PRIMARY KEY AUTOINCREMENT` | `int` | Unique auto-incrementing identifier for each task |
| `title` | `TEXT` | `str` | Description or name of the task |
| `done` | `BOOLEAN` (`0` or `1`) | `bool` | Completion status (`0` = `False`, `1` = `True`) |

---

## API Endpoints Reference

### 1. Root Health Check
* **Method:** `GET`
* **Path:** `/`
* **Response:**
  ```json
  {
    "status": "success",
    "message": "welcome to the backend server"
  }
  ```

### 2. Get All Tasks
* **Method:** `GET`
* **Path:** `/tasks`
* **SQL Executed:** `SELECT id, title, done FROM tasks`
* **Response:**
  ```json
  [
    { "id": 1, "title": "Task 1", "done": false },
    { "id": 2, "title": "Task 2", "done": false },
    { "id": 3, "title": "Task 3", "done": true }
  ]
  ```

### 3. Get a Specific Task by ID
* **Method:** `GET`
* **Path:** `/tasks/{id}`
* **SQL Executed:** `SELECT id, title, done FROM tasks WHERE id = ?`
* **Response (Found):**
  ```json
  {
    "id": 1,
    "title": "Task 1",
    "done": false
  }
  ```
* **Response (Not Found):**
  ```json
  {
    "error": "Task not found"
  }
  ```

### 4. Create a New Task
* **Method:** `POST`
* **Path:** `/tasks`
* **SQL Executed:** `INSERT INTO tasks (title, done) VALUES (?, ?)`
* **Request Body:**
  ```json
  {
    "id": 0,
    "title": "Learn SQLite with FastAPI",
    "done": false
  }
  ```
* **Response:**
  ```json
  {
    "id": 4,
    "title": "Learn SQLite with FastAPI",
    "done": false
  }
  ```

### 5. Update an Existing Task
* **Method:** `PUT`
* **Path:** `/tasks/{id}`
* **SQL Executed:** `UPDATE tasks SET title = ?, done = ? WHERE id = ?`
* **Request Body:**
  ```json
  {
    "id": 1,
    "title": "Task 1 (Completed)",
    "done": true
  }
  ```
* **Response (Found):**
  ```json
  {
    "id": 1,
    "title": "Task 1 (Completed)",
    "done": true
  }
  ```

### 6. Delete a Task
* **Method:** `DELETE`
* **Path:** `/tasks/{id}`
* **SQL Executed:** `DELETE FROM tasks WHERE id = ?`
* **Response (Success):**
  ```json
  [
    "Task 1 deleted"
  ]
  ```

---

## Exploring the Database & Example SQL Queries

You can inspect and modify `tasks.db` directly using **DB Browser for SQLite** or the **VS Code SQLite Viewer** extension.

### Example SQL Queries Executed

```sql
-- 1. List every task in the database
SELECT * FROM tasks;

-- 2. Show only completed tasks
SELECT * FROM tasks WHERE done = 1;

-- 3. Count the total number of tasks
SELECT COUNT(*) FROM tasks;

-- 4. Mark every task as completed
UPDATE tasks SET done = 1;

-- 5. Delete all completed tasks
DELETE FROM tasks WHERE done = 1;
```

---

## Database Viewer Screenshot

![SQLite Database Viewer Screenshot](./Screenshot/sqlite_viewer.png)
*(Note: Replace `./Screenshot/sqlite_viewer.png` with the exact filename of your screenshot inside the `Screenshot` folder).*
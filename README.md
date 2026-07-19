# FastAPI Task Manager (CRUD API)

This is a simple, fully functional CRUD (Create, Read, Update, Delete) API built using [FastAPI](https://fastapi.tiangolo.com/) as part of the FlyRank AI Internship (Week 2). 

It uses an in-memory Python list to store and manage a database of "Tasks".

## 🚀 Features

- **Create**: Add new tasks to the list (`POST`)
- **Read**: View all tasks or find a specific task by its ID (`GET`)
- **Update**: Modify the title or completion status of an existing task (`PUT`)
- **Delete**: Remove a task from the list permanently (`DELETE`)
- **Input Validation**: Automatically rejects empty titles or invalid requests with proper HTTP error codes (`400 Bad Request`, `404 Not Found`, `422 Unprocessable Entity`).

## 🛠️ How to Run the Server

1. Make sure you have FastAPI installed:
   ```bash
   pip install "fastapi[standard]"
   ```
2. Start the development server from your terminal:
   ```bash
   fastapi dev Assignment_CRUD_API.py
   ```
   *(Note: You can also use `uvicorn Assignment_CRUD_API:crud --reload`)*

## 📖 Interactive API Documentation (Swagger UI)

FastAPI automatically generates a beautiful, interactive documentation page for your API. You can use this to test all of your endpoints directly from your browser without needing to use `curl` or Postman!

1. Start your server.
2. Open your web browser and navigate to: **[http://localhost:8000/docs](http://localhost:8000/docs)**

*(See the included screenshot for an example of the Swagger UI interface!)*

## 📍 API Endpoints

| Method | Endpoint | Description | Status Codes |
| :--- | :--- | :--- | :--- |
| **GET** | `/` | Returns basic API info and available endpoints. | `200 OK` |
| **GET** | `/health` | Simple health check to ensure server is running. | `200 OK` |
| **GET** | `/tasks` | Returns the entire list of all tasks. | `200 OK` |
| **GET** | `/tasks/{id}` | Returns a single task matching the given ID. | `200 OK`, `404 Not Found` |
| **POST** | `/tasks` | Creates a new task. Requires a JSON body (e.g., `{"title": "Buy milk"}`). | `201 Created`, `400 Bad Request` |
| **PUT** | `/tasks/{id}` | Updates an existing task's title or `done` status. | `200 OK`, `400 Bad Request`, `404 Not Found` |
| **DELETE** | `/tasks/{id}` | Deletes the specified task from the list. | `204 No Content`, `404 Not Found` |

---
*Built during the FlyRank AI Internship - Week 2*

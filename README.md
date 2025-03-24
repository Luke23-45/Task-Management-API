
# Task Management API

This API allows users to register (using JWT), log in, and perform CRUD (Create, Read, Update, Delete) operations on tasks. It supports advanced features such as filtering, searching, ordering, pagination, rate limiting, and logging.

## Table of Contents

- [Introduction](#introduction)
- [Base URL](#base-url)
- [Authentication](#authentication)
  - [Obtaining an Access Token](#obtaining-an-access-token)
    - [User Registration](#user-registration)
    - [User Login](#user-login)
  - [Using the Access Token](#using-the-access-token)
- [Task Management Endpoints](#task-management-endpoints)
  - [Create a New Task](#create-a-new-task)
  - [Read All Tasks](#read-all-tasks)
  - [Read a Specific Task](#read-a-specific-task)
  - [Update a Task](#update-a-task)
  - [Delete a Task](#delete-a-task)
- [Filtering, Ordering, Searching & Pagination Examples](#filtering-ordering-searching--pagination-examples)
- [Rate Limiting & Throttling](#rate-limiting--throttling)
- [Logging & Monitoring](#logging--monitoring)
- [Error Handling](#error-handling)

## Introduction

This API enables users to manage their tasks by registering, logging in, and performing standard CRUD operations. In addition, it supports various advanced features such as filtering, searching, ordering, pagination, rate limiting, and logging.

## Base URL

All API endpoints are prefixed by the following base URL:

```
http://127.0.0.1:8000/api/
```

## Authentication

The API uses **JSON Web Tokens (JWT)** to authenticate users. After registering and logging in, you'll receive an access token that must be used in all subsequent requests to protected endpoints.

### Obtaining an Access Token

#### User Registration

- **Endpoint:** `/api/users/register/`
- **Method:** `POST`
- **Request Body (JSON):**

  ```json
  {
    "full_name": "Your Full Name",
    "email": "[email address removed]",
    "password": "your_strong_password"
  }
  ```

- **Response:**
  - **Status:** `201 Created`

#### User Login

- **Endpoint:** `/api/users/login/`
- **Method:** `POST`
- **Request Body (JSON):**

  ```json
  {
    "username": "[email address]",
    "password": "your_strong_password"
  }
  ```

- **Response:**
  - **Status:** `200 OK`
  - **Body (JSON):**

    ```json
    {
      "refresh": "YOUR_REFRESH_TOKEN",
      "access": "YOUR_ACCESS_TOKEN"
    }
    ```

### Using the Access Token

For every request to a protected endpoint (e.g., `/api/tasks/`), include the header:

```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

Replace `YOUR_ACCESS_TOKEN` with the token received during login.

## Task Management Endpoints

All task-related endpoints require authentication. The base URL for task management is `/api/tasks/`.

### Create a New Task

- **Endpoint:** `/api/tasks/`
- **Method:** `POST`
- **Headers:**

  ```
  Content-Type: application/json
  Authorization: Bearer YOUR_ACCESS_TOKEN
  ```

- **Request Body (JSON):**

  ```json
  {
    "title": "Buy groceries",
    "description": "Milk, bread, eggs, and cheese",
    "status": "pending"
  }
  ```

- **Response:**
  - **Status:** `201 Created`
  - **Body (JSON Example):**

    ```json
    {
      "title": "Buy groceries",
      "description": "Milk, bread, eggs, and cheese",
      "status": "pending"
    }
    ```

### Read All Tasks

- **Endpoint:** `/api/tasks/`
- **Method:** `GET`
- **Headers:**

  ```
  Authorization: Bearer YOUR_ACCESS_TOKEN
  ```

- **Optional Query Parameters:**
  - **`status`**: Filter tasks by status (e.g., `pending`, `in_progress`, `completed`).
  - **`search`**: Search tasks by keyword in the title or description.
  - **`ordering`**: Order tasks by a specific field. Use a `-` prefix for descending order.
  - **`page`**: Specify the page number for pagination.
- **Response:**
  - **Status:** `200 OK`
  - **Body (JSON Example - Paginated):**

    ```json
    {
      "count": 25,
      "next": "http://127.0.0.1:8000/api/tasks/?page=2",
      "previous": null,
      "results": [
        {
          "id": 1,
          "user": 1,
          "title": "Buy groceries",
          "description": "Milk, bread, eggs, and cheese",
          "status": "pending",
          "created_at": "2025-03-24T10:00:00Z",
          "updated_at": "2025-03-24T10:00:00Z"
        }
        // ... more task objects
      ]
    }
    ```

### Read a Specific Task

- **Endpoint:** `/api/tasks/{id}/`
  Replace `{id}` with the task's ID.
- **Method:** `GET`
- **Headers:**

  ```
  Authorization: Bearer YOUR_ACCESS_TOKEN
  ```

- **Response:**
  - **Status:**
    - `200 OK` if the task exists and belongs to the user.
    - `404 Not Found` if the task does not exist or is inaccessible.
  - **Body (JSON Example):**

    ```json
    {
      "id": 1,
      "user": 1,
      "title": "Buy groceries",
      "description": "Milk, bread, eggs, and cheese",
      "status": "pending",
      "created_at": "2025-03-24T10:00:00Z",
      "updated_at": "2025-03-24T10:00:00Z"
    }
    ```

### Update a Task

- **Endpoint:** `/api/tasks/{id}/`
  Replace `{id}` with the task's ID.
- **Method:** `PUT`
- **Headers:**

  ```
  Content-Type: application/json
  Authorization: Bearer YOUR_ACCESS_TOKEN
  ```

- **Request Body (JSON):**

  ```json
  {
    "title": "Buy groceries and vegetables",
    "status": "in_progress"
  }
  ```

- **Response:**
  - **Status:**
    - `200 OK` on successful update.
    - `404 Not Found` if the task does not exist or is inaccessible.
  - **Body (JSON Example):**

    ```json
    {
      "title": "Buy groceries and vegetables",
      "description": "Milk, bread, eggs, and cheese",
      "status": "in_progress"
    }
    ```

### Delete a Task

- **Endpoint:** `/api/tasks/{id}/`
  Replace `{id}` with the task's ID.
- **Method:** `DELETE`
- **Headers:**

  ```
  Authorization: Bearer YOUR_ACCESS_TOKEN
  ```

- **Response:**
  - **Status:**
    - `204 No Content` on successful deletion.
    - `404 Not Found` if the task does not exist or is inaccessible.
  - **Body:** Empty

## Filtering, Ordering, Searching & Pagination Examples

Below are specific examples of using filtering, ordering, and pagination features with the `/api/tasks/` endpoint:

### Filtering by Status

- **Get all tasks with the status "pending":**

  ```
  GET http://127.0.0.1:8000/api/tasks/?status=pending
  ```

- **Get all tasks with the status "in_progress":**

  ```
  GET http://127.0.0.1:8000/api/tasks/?status=in_progress
  ```

- **Get all tasks with the status "completed":**

  ```
  GET http://127.0.0.1:8000/api/tasks/?status=completed
  ```

### Searching by Keyword

- **Search for tasks containing the word "meeting" in the title or description:**

  ```
  GET http://127.0.0.1:8000/api/tasks/?search=meeting
  ```

- **Search for tasks containing the word "urgent":**

  ```
  GET http://127.0.0.1:8000/api/tasks/?search=urgent
  ```

### Ordering Tasks

- **Order tasks alphabetically by title (ascending):**

  ```
  GET http://127.0.0.1:8000/api/tasks/?ordering=title
  ```

- **Order tasks by title in reverse alphabetical order (descending):**

  ```
  GET http://127.0.0.1:8000/api/tasks/?ordering=-title
  ```

- **Order tasks by their creation date, newest first (descending - default):**

  ```
  GET http://127.0.0.1:8000/api/tasks/?ordering=-created_at
  ```

- **Order tasks by their creation date, oldest first (ascending):**

  ```
  GET http://127.0.0.1:8000/api/tasks/?ordering=created_at
  ```

- **Order tasks by their status (ascending):**

  ```
  GET http://127.0.0.1:8000/api/tasks/?ordering=status
  ```

- **Order tasks by their last updated date, newest first (descending):**

  ```
  GET http://127.0.0.1:8000/api/tasks/?ordering=-updated_at
  ```

### Pagination

Assuming `PAGE_SIZE` is set to 10 in your settings:

- **Get the first page of tasks:**

  ```
  GET http://127.0.0.1:8000/api/tasks/?page=1
  ```

  *Note: Omitting the `page` parameter typically defaults to the first page.*

- **Get the second page of tasks:**

  ```
  GET http://127.0.0.1:8000/api/tasks/?page=2
  ```

- **Get the third page of tasks:**

  ```
  GET http://127.0.0.1:8000/api/tasks/?page=3
  ```

### Combining Features

- **Get the first page of "pending" tasks, ordered by title:**

  ```
  GET http://127.0.0.1:8000/api/tasks/?status=pending&ordering=title&page=1
  ```

- **Get all "completed" tasks that contain the word "project", ordered by last updated date (newest first):**

  ```
  GET http://127.0.0.1:8000/api/tasks/?status=completed&search=project&ordering=-updated_at
  ```

## Rate Limiting & Throttling

To prevent abuse, the API enforces rate limits:

- **Anonymous Users:** 100 requests per minute.
- **Authenticated Users:** 300 requests per minute.

If the limit is exceeded, the API will return a `429 Too Many Requests` status code.

## Logging & Monitoring

The API utilizes Django's logging framework to monitor events and issues. Logs are output to:

- A file: `logs/task_management.log`


## Error Handling

Standard HTTP status codes are used to indicate request outcomes:

- **400 Bad Request:** The server cannot process the request due to client error (e.g., invalid JSON).
- **401 Unauthorized:** Authentication is required and has failed or not been provided.
- **403 Forbidden:** The client does not have permission to access the resource.
- **404 Not Found:** The requested resource was not found.
- **429 Too Many Requests:** Rate limit exceeded.
- **500 Internal Server Error:** An unexpected error occurred on the server.


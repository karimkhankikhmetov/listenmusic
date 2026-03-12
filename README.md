# 🎵 Music Streaming API

A simple **FastAPI-based music streaming backend** that allows users to register, log in, upload tracks, stream them, list tracks, and delete them.

## 🚀 Features

* User registration
* User authentication
* Upload music files
* List tracks with pagination and search
* Stream music
* Delete tracks (authorized users)

---

# 🛠 Tech Stack

* **Framework:** FastAPI
* **API Format:** REST
* **Database:** sqlite

---

# 📦 Installation

```bash
git clone https://github.com/yourusername/music-api.git
cd music-api
pip install -r requirements.txt
```

Run the server:

```bash
uvicorn main:app --reload
```

Server will start at:

```
http://127.0.0.1:8000
```

Interactive documentation:

```
http://127.0.0.1:8000/docs
```

---

# 🔐 Authentication

This API uses **Bearer authentication**.

1. Register a user
2. Login to receive an access token
3. Use the token in protected routes

Example header:

```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

---

# 📡 API Endpoints

## Root

### GET /

Returns API status.

**Response**

```json
{
  "message": "API running"
}
```

---

# 👤 Authentication

## Register

### POST /register

Create a new user.

**Request**

Form URL encoded:

```
username=yourname
password=yourpassword
```

**Response**

```json
{
  "message": "User registered successfully"
}
```

---

## Login

### POST /login

Login and receive an access token.

**Request**

Form URL encoded:

```
username=yourname
password=yourpassword
```

**Response**

```json
{
  "access_token": "token",
  "token_type": "bearer"
}
```

---

# 🎧 Music Endpoints

## Upload Music

### POST /upload

Upload a music file.

**Authentication Required**

**Request**

Multipart form data:

```
file: audio file
title: track title
```

**Response**

```json
{
  "message": "Track uploaded"
}
```

---

## List Tracks

### GET /tracks

Retrieve available tracks.

**Query Parameters**

| Parameter | Type    | Default  | Description     |
| --------- | ------- | -------- | --------------- |
| page      | integer | 1        | Page number     |
| limit     | integer | 20       | Items per page  |
| search    | string  | optional | Search by title |

Example:

```
GET /tracks?page=1&limit=10&search=rock
```

---

## Stream Track

### GET /tracks/{track_id}/stream

Stream a specific music track.

**Parameters**

| Name     | Type   | Description      |
| -------- | ------ | ---------------- |
| track_id | string | Track identifier |

Example:

```
GET /tracks/abc123/stream
```

---

## Delete Track

### DELETE /tracks/{track_id}

Delete a track.

**Authentication Required**

**Parameters**

| Name     | Type   | Description      |
| -------- | ------ | ---------------- |
| track_id | string | Track identifier |

---

# ⚠️ Error Responses

### Validation Error (422)

Returned when request data is invalid.

Example:

```json
{
  "detail": [
    {
      "loc": ["body", "username"],
      "msg": "field required",
      "type": "value_error"
    }
  ]
}
```

---

# 📂 Project Structure (example)

```
project
│
├── main.py
├── models.py
├── auth.py
├── routes
│   ├── auth.py
│   ├── tracks.py
│
├── storage
│   └── uploads
│
└── requirements.txt
```

---

# 📖 API Documentation

FastAPI automatically provides documentation:

* Swagger UI:
  `/docs`

* ReDoc:
  `/redoc`

---

# 🧑‍💻 Author

mini project to expereience **FastAPI**. the music is stored in the root of the project which is horrible but since this project is not that that serious i decided that it is ok. 

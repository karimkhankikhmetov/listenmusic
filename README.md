# 🎵 listenmusic

A REST API for uploading and streaming music, built with FastAPI. Made to get hands-on experience with FastAPI, JWT auth, and file handling.

## Stack

- **FastAPI** — framework
- **SQLite** — database
- **SQLAlchemy** — ORM
- **JWT (python-jose)** — authentication
- **mutagen** — reading MP3 metadata (duration)
- **passlib + bcrypt** — password hashing

## Setup

```bash
git clone https://github.com/karimkhankikhmetov/listenmusic.git
cd listenmusic
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API runs at `http://127.0.0.1:8000`  
Swagger UI at `http://127.0.0.1:8000/docs`

---

## Endpoints

### Auth

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/register` | No | Register a new user |
| POST | `/login` | No | Login and get access token |

**Register** — `application/x-www-form-urlencoded`
```
username=yourname&password=yourpassword
```

**Login** — `application/x-www-form-urlencoded`
```
username=yourname&password=yourpassword&grant_type=password
```
Returns:
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

> Tokens are valid for 24 hours. Include in protected requests as:  
> `Authorization: Bearer YOUR_TOKEN`

---

### Tracks

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/tracks` | No | List tracks (paginated, searchable) |
| POST | `/upload` | ✅ Yes | Upload an MP3 |
| GET | `/tracks/{track_id}/stream` | No | Stream a track |
| DELETE | `/tracks/{track_id}` | ✅ Yes | Delete your own track |

**GET /tracks** — query params:

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| page | int | 1 | Page number |
| limit | int | 20 | Results per page |
| search | string | — | Search by title or author |

Example: `GET /tracks?search=travis&page=1&limit=10`

Response:
```json
{
  "page": 1,
  "limit": 10,
  "total": 47,
  "pages": 5,
  "results": [
    {
      "id": "uuid",
      "title": "track title",
      "author": "username",
      "duration": "3:45",
      "file_size": 8192000
    }
  ]
}
```

**POST /upload** — `multipart/form-data`
```
file: <mp3 file>
title: track title
```
Only MP3 files accepted. Author is taken from the JWT token automatically.

**DELETE /tracks/{track_id}**  
Only the user who uploaded the track can delete it. Returns 403 otherwise.

---

## Notes

- MP3 files are stored locally in `storage/music/` — not production-ready, fine for a mini project
- Only MP3 (`audio/mpeg`) uploads are accepted
- Passwords are hashed with bcrypt
- Search is case-insensitive

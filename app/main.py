from fastapi import FastAPI, UploadFile, File, HTTPException, Form, Depends
from fastapi.responses import StreamingResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError

from app.database import SessionLocal, engine
from app.models import Track, User
from app.security import hash_password, verify_password, create_access_token

from mutagen.mp3 import MP3

import os
import uuid

from app import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

UPLOAD_DIR = "storage/music"
os.makedirs(UPLOAD_DIR, exist_ok=True)

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# -----------------------------
# Получение текущего пользователя
# -----------------------------
def get_current_user(token: str = Depends(oauth2_scheme)):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    db = SessionLocal()

    user = db.query(User).filter(User.username == username).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


# -----------------------------
# Root
# -----------------------------
@app.get("/")
def root():
    return {"message": "Music API is running"}


# -----------------------------
# Upload (LOGIN REQUIRED)
# -----------------------------
@app.post("/upload")
async def upload_music(
    file: UploadFile = File(...),
    title: str = Form(...),
    user: User = Depends(get_current_user)
):

    if file.content_type != "audio/mpeg":
        raise HTTPException(status_code=400, detail="Only MP3 files allowed")

    file_id = str(uuid.uuid4())
    stored_filename = f"{file_id}.mp3"
    file_path = os.path.join(UPLOAD_DIR, stored_filename)

    content = await file.read()

    with open(file_path, "wb") as buffer:
        buffer.write(content)

    audio = MP3(file_path)
    duration = int(audio.info.length)

    db = SessionLocal()

    new_track = Track(
        id=file_id,
        title=title,
        original_name=file.filename,
        stored_name=stored_filename,
        author=user.username,  # ← теперь автор из токена
        duration=duration,
        file_size=len(content)
    )

    db.add(new_track)
    db.commit()
    db.close()

    return {"message": "Uploaded successfully", "id": file_id}


# -----------------------------
# List tracks
# -----------------------------
@app.get("/tracks")
def list_tracks(
        page: int = 1,
        limit: int = 20,
        search: str = None
):
    db = SessionLocal()

    query = db.query(Track)

    if search:
        query = query.filter(
            Track.title.ilike(f"%{search}%") |
            Track.author.ilike(f"%{search}%")
        )

    total = query.count()

    offset = (page - 1) * limit
    tracks = query.offset(offset).limit(limit).all()

    result = []
    for track in tracks:
        minutes = track.duration // 60
        seconds = track.duration % 60
        result.append({
            "id": track.id,
            "title": track.title,
            "author": track.author,
            "duration": f"{minutes}:{seconds:02d}",
            "file_size": track.file_size
        })

    db.close()

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "pages": (total + limit - 1) // limit,
        "results": result
    }


# -----------------------------
# Stream
# -----------------------------
@app.get("/tracks/{track_id}/stream")
def stream_track(track_id: str):

    db = SessionLocal()

    track = db.query(Track).filter(Track.id == track_id).first()

    if not track:
        db.close()
        raise HTTPException(status_code=404, detail="Track not found")

    file_path = os.path.join(UPLOAD_DIR, track.stored_name)

    if not os.path.exists(file_path):
        db.close()
        raise HTTPException(status_code=404, detail="File not found")

    def iterfile():
        with open(file_path, "rb") as file:
            yield from file

    db.close()

    return StreamingResponse(iterfile(), media_type="audio/mpeg")


# -----------------------------
# Delete (LOGIN REQUIRED)
# -----------------------------
@app.delete("/tracks/{track_id}")
def delete_track(
    track_id: str,
    user: User = Depends(get_current_user)
):

    db = SessionLocal()

    track = db.query(Track).filter(Track.id == track_id).first()

    if not track:
        db.close()
        raise HTTPException(status_code=404, detail="Track not found")

    # нельзя удалить чужой трек
    if track.author != user.username:
        raise HTTPException(status_code=403, detail="Not your track")

    file_path = os.path.join(UPLOAD_DIR, track.stored_name)

    if os.path.exists(file_path):
        os.remove(file_path)

    db.delete(track)
    db.commit()
    db.close()

    return {"message": "Track deleted successfully"}


# -----------------------------
# Register
# -----------------------------
@app.post("/register")
def register(
    username: str = Form(...),
    password: str = Form(...)
):

    db = SessionLocal()

    existing = db.query(User).filter(User.username == username).first()

    if existing:
        raise HTTPException(status_code=400, detail="User exists")

    hashed = hash_password(password)

    user = User(
        username=username,
        password_hash=hashed
    )

    db.add(user)
    db.commit()

    return {"message": "user created"}


# -----------------------------
# Login
# -----------------------------

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):

    db = SessionLocal()

    username = form_data.username
    password = form_data.password

    user = db.query(User).filter(User.username == username).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not verify_password(password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": user.username})

    return {
        "access_token": token,
        "token_type": "bearer"
    }
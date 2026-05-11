from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from datetime import datetime

app = FastAPI()

# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# DATABASE
# =========================

def init_db():
    conn = sqlite3.connect("database.db")

    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS chat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            message TEXT,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()

# =========================
# SHOW FRONTEND
# =========================

@app.get("/")
async def home():
    return FileResponse("index.html")

# =========================
# CHAT API
# =========================

@app.post("/chat")
async def chat(request: Request):

    data = await request.json()

    user_message = data.get("message")

    conn = sqlite3.connect("database.db")

    c = conn.cursor()

    c.execute(
        "INSERT INTO chat (role, message, timestamp) VALUES (?, ?, ?)",
        ("user", user_message, str(datetime.now()))
    )

    # AI RESPONSE
    bot_reply = f"คุณพิมพ์ว่า: {user_message}"

    c.execute(
        "INSERT INTO chat (role, message, timestamp) VALUES (?, ?, ?)",
        ("bot", bot_reply, str(datetime.now()))
    )

    conn.commit()
    conn.close()

    return JSONResponse({
        "response": bot_reply
    })

# =========================
# LOAD HISTORY
# =========================

@app.get("/history")
async def history():

    conn = sqlite3.connect("database.db")

    c = conn.cursor()

    c.execute("SELECT role, message, timestamp FROM chat")

    rows = c.fetchall()

    conn.close()

    return rows

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import sqlite3
from datetime import datetime

app = FastAPI()

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

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <body style="background:#111;color:white;font-family:sans-serif;">
            <h1>AI Chat</h1>
            <form method="post" action="/chat">
                <input name="message" style="width:300px;">
                <button type="submit">Send</button>
            </form>
        </body>
    </html>
    """

@app.post("/chat")
async def chat(request: Request):
    form = await request.form()
    user_message = form["message"]

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("INSERT INTO chat (role, message, timestamp) VALUES (?, ?, ?)",
              ("user", user_message, str(datetime.now())))

    bot_reply = f"คุณพิมพ์ว่า: {user_message}"

    c.execute("INSERT INTO chat (role, message, timestamp) VALUES (?, ?, ?)",
              ("bot", bot_reply, str(datetime.now())))

    conn.commit()
    conn.close()

    return HTMLResponse(f"<h2>{bot_reply}</h2><a href='/'>กลับ</a>")

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import sqlite3
import subprocess

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# === Login Page ===
@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": ""})


# === Vulnerable SQL Login ===
@app.post("/auth", response_class=HTMLResponse)
async def auth(request: Request, username: str = Form(...), password: str = Form(...)):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # ⚠️ INTENTIONAL SQL Injection vulnerability
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    result = cursor.fetchone()

    if result:
        return RedirectResponse("/dashboard", status_code=303)

    return templates.TemplateResponse("login.html", {
        "request": request,
        "error": "Invalid username or password"
    })


# === Dashboard ===
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return """
    <h1>🏦 Welcome to National Bank Internal Dashboard</h1>
    <p>Use the system to view account information.</p>
    <a href="/account?id=1">View Account 1</a><br>
    <a href="/challenge">Go to Challenge Page</a>
    """


# === Vulnerable Path Traversal ===
@app.get("/view", response_class=HTMLResponse)
async def view_file(request: Request, doc: str = ""):
    try:
        with open(doc, "r") as f:
            content = f.read()
    except Exception as e:
        content = f"Error: {e}"

    return templates.TemplateResponse("view.html", {
        "request": request,
        "doc": doc,
        "content": content
    })


# === Command Injection (ping) ===
@app.get("/ping", response_class=HTMLResponse)
async def ping_host(request: Request, host: str = ""):
    try:
        command = f"ping -c 2 {host}"  # ⚠️ vulnerable
        output = subprocess.getoutput(command)
    except Exception as e:
        output = f"Error: {e}"

    return templates.TemplateResponse("ping.html", {
        "request": request,
        "host": host,
        "output": output
    })


# === Vulnerable Account Viewer (FLAG on id=3) ===
@app.get("/account", response_class=HTMLResponse)
async def view_account(request: Request, id: int = 1):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(f"SELECT owner, balance FROM accounts WHERE id={id}")
    row = cursor.fetchone()

    if not row:
        content = "Account not found"
    else:
        owner, balance = row
        content = f"Account Owner: {owner}<br>Balance: {balance}"

        # BACKDOOR FLAG
        if id == 3:
            try:
                secret = open("secret/flag4.txt").read()
                content += f"<br><br><b>Secret Flag:</b> {secret}"
            except:
                content += "<br><br>(Missing flag4.txt)"

    return templates.TemplateResponse("account.html", {
        "request": request,
        "content": content
    })


# === Challenge Page ===
@app.get("/challenge", response_class=HTMLResponse)
async def challenge_page(request: Request):
    return templates.TemplateResponse("challenge.html", {
        "request": request,
        "result": "",
        "result_class": ""
    })


@app.post("/challenge", response_class=HTMLResponse)
async def submit_challenge(request: Request, flag: str = Form(...)):
    correct_flag = open("secret/flag4.txt").read().strip()

    if flag.strip() == correct_flag:
        result = "✔ Correct flag!"
        result_class = "success"
    else:
        result = "✘ Wrong flag, try again."
        result_class = "error"

    return templates.TemplateResponse("challenge.html", {
        "request": request,
        "result": result,
        "result_class": result_class
    })



from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_methods=["*"], 
    allow_headers=["*"]
)

base_dir = os.path.dirname(__file__)
templates_dir = os.path.abspath(os.path.join(base_dir, "..", "templates"))
static_dir  = os.path.abspath(os.path.join(base_dir, "..", "static"))

app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", response_class=HTMLResponse)
async def home():
    with open(os.path.join(templates_dir,"index.html")) as f:
        return f.read()

@app.post("/calculate")
async def calculate(date1: str = Form(...), date2: str = Form(...)):
    ## algorithm stuff

    parts1 = date1.split("/")
    d1 = int(parts1[0])
    m1 = int(parts1[1])
    y1 = int(parts1[2])

    parts2 = date2.split("/")
    d2 = int(parts2[0])
    m2 = int(parts2[1])
    y2 = int(parts2[2])

    months1 = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    months2 = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    total1 = 0
    y = 0
    while y < y1:
        if (y % 400 == 0) or (y % 4 == 0 and y % 100 != 0):
            total1 += 366
        else:
            total1 += 365
        y += 1

    m = 1
    while m < m1:
        if (y1 % 400 == 0) or (y1 % 4 == 0 and y1 % 100 != 0):
            total1 += months2[m-1]
        else:
            total1 += months1[m-1]
        m += 1

    total1 += d1

    total2 = 0
    y = 0
    while y < y2:
        if (y % 400 == 0) or (y % 4 == 0 and y % 100 != 0):
            total2 += 366
        else:
            total2 += 365
        y += 1

    m = 1
    while m < m2:
        if (y2 % 400 == 0) or (y2 % 4 == 0 and y2 % 100 != 0):
            total2 += months2[m-1]
        else:
            total2 += months1[m-1]
        m += 1

    total2 += d2

    days_diff = total2 - total1
    if days_diff < 0:
        days_diff = -days_diff

    with open(os.path.join(templates_dir, "index.html")) as f:
        html = f.read()
    result_html = f'<div class="result">Days between dates: <strong>{days_diff}</strong></div>'
    return HTMLResponse(content=html.replace('<!-- the result space -->', result_html))



from pathlib import Path
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

from image_service import generate_image_job

BASE_DIR = Path(__file__).resolve().parent
OUTPUTS_DIR = BASE_DIR / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="Image Turbo Web Trigger")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
app.mount("/outputs", StaticFiles(directory=OUTPUTS_DIR), name="outputs")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/generate")
def generate(prompt: str = Form(...), width: int = Form(768), height: int = Form(512)) -> dict:
    if not prompt.strip():
        raise HTTPException(status_code=400, detail="prompt 不能是空白")
    if width < 64 or height < 64 or width > 2048 or height > 2048:
        raise HTTPException(status_code=400, detail="寬高需介於 64~2048")

    result = generate_image_job(prompt=prompt.strip(), width=width, height=height, base_output_dir=OUTPUTS_DIR)
    return result

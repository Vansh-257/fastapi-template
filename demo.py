from fastapi import FastAPI, File, UploadFile, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import pandas as pd
import io

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/csv-viewer", response_class=HTMLResponse)
async def csv_viewer(request: Request, file: UploadFile = File(...)):
    try:
        content = await file.read()
        df = pd.read_csv(io.StringIO(content.decode('utf-8')))
        columns = list(df)
        rows = df.values.tolist()
        return templates.TemplateResponse("index.html", {"request": request, "columns": columns, "rows": rows})
    except Exception as e:
        return templates.TemplateResponse("error.html", {"request": request, "error_message": str(e)})

import os
from dotenv import load_dotenv

load_dotenv()


if __name__ == "__main__":
    os.system("uvicorn demo:app --reload --host 0.0.0.0 --port 7003")
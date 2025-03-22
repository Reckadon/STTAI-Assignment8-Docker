from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import httpx

app = FastAPI()

# Configure templates directory for HTML rendering
templates = Jinja2Templates(directory="templates")

# Backend service URL (Docker-internal hostname)
BACKEND_URL = "http://34.47.145.245:9567"  # Replace "backend" with the backend container name in Docker Compose

@app.get("/")
async def home(request: Request):
    """
    Render the homepage with input for search and insert operations.
    """
    return templates.TemplateResponse("index.html", {"request": request, "result": None})

@app.post("/search")
async def search_document(request: Request, query: str = Form(...)):
    """
    Send a search query to the backend and display results.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BACKEND_URL}/search", params={"query": query})
            result = response.json()
        return templates.TemplateResponse("index.html", {"request": request, "result": result})
    except Exception as e:
        return templates.TemplateResponse("index.html", {"request": request, "result": f"Error: {str(e)}"})

@app.post("/insert")
async def insert_document(request: Request, content: str = Form(...)):
    """
    Send a document to the backend for insertion into Elasticsearch.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{BACKEND_URL}/insert", json={"content": content})
            result = response.json()
        return templates.TemplateResponse("index.html", {"request": request, "result": result})
    except Exception as e:
        return templates.TemplateResponse("index.html", {"request": request, "result": f"Error: {str(e)}"})

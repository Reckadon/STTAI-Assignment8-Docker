from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import requests, os

app = FastAPI()

# Configure templates directory for HTML rendering
templates = Jinja2Templates(directory="templates")

# Backend service URL (external or Docker-internal hostname)
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

@app.get("/")
def home(request: Request):
    """
    Render the homepage with input for search and insert operations.
    """
    return templates.TemplateResponse("index.html", {"request": request, "result": None})

@app.post("/get")
def search_document(request: Request, query: str = Form(...)):
    """
    Send a search query to the backend and display results.
    """
    try:
        # Send GET request to the backend
        response = requests.get(f"{BACKEND_URL}/get", params={"query": query})
        response.raise_for_status()  # Raise an exception for HTTP errors
        raw_result = response.json()  # Parse JSON response
        
        # Extract relevant fields (index and content)
        processed_result = [
            {"index": hit["_source"]["index"], "content": hit["_source"]["doc"]["content"]}
            for hit in raw_result.get("hits", {}).get("hits", [])
        ]

        return templates.TemplateResponse("index.html", {"request": request, "result": processed_result})
    except Exception as e:
        return templates.TemplateResponse("index.html", {"request": request, "result": f"Error: {str(e)}"})


@app.post("/insert")
def insert_document(request: Request, index: str = Form(...), title: str = Form(...), content: str = Form(...)):
    """
    Send a document to the backend for insertion into Elasticsearch.
    """
    try:
        # Format the request payload correctly
        payload = {
            "index": index,
            "doc": {
                "title": title,
                "content": content
            }
        }

        # Send POST request to the backend with JSON data
        response = requests.post(f"{BACKEND_URL}/insert", json=payload, headers={"Content-Type": "application/json"})
        response.raise_for_status()  # Raise an exception for HTTP errors

        result = response.json()  # Parse JSON response
        return templates.TemplateResponse("index.html", {"request": request, "result": result})

    except Exception as e:
        return templates.TemplateResponse("index.html", {"request": request, "result": f"Error: {str(e)}"})

# @app.post("/insert")
# def insert_document(request: Request, content: str = Form(...)):
#     """
#     Send a document to the backend for insertion into Elasticsearch.
#     """
#     try:
#         # Send POST request to the backend with formatted content
#         response = requests.post(f"{BACKEND_URL}/insert", json={"content": content})
#         response.raise_for_status()  # Raise an exception for HTTP errors
#         result = response.json()  # Parse JSON response
#         return templates.TemplateResponse("index.html", {"request": request, "result": result})
#     except Exception as e:
#         return templates.TemplateResponse("index.html", {"request": request, "result": f"Error: {str(e)}"})
from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()
ES_URL = "http://es-app:9567/my_index/_doc/"

@app.post("/insert")
def insert_document(doc: dict):
    response = requests.post(ES_URL, json=doc)
    return response.json()


@app.get("/get")
def get_document(query: str):
    """
    Search for documents in Elasticsearch using a match query.
    """
    try:
        # Use a match query to search for documents
        search_body = {
            "query": {
                "match": {
                    "doc.content": query
                }
            }
        }
        response = requests.get(ES_URL + "_search", json=search_body)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve document: {str(e)}")

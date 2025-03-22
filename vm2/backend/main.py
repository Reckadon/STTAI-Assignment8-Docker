from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()
ES_URL = "http://elasticsearch:9200/my_index/_doc/"

@app.post("/insert")
def insert_document(doc: dict):
    response = requests.post(ES_URL, json=doc)
    return response.json()

@app.get("/get")
def get_document():
    response = requests.get(ES_URL + "_search", json={"query": {"match_all": {}}})
    return response.json()


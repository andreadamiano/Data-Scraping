from fastapi import FastAPI

app = FastAPI()  # Creates the API

@app.get("/")  # Listens to `http://localhost:8000/`
def home():
    return {"message": "Hello World!"}
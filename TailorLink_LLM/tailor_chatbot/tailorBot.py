from fastapi import FastAPI

app = FastAPI()

@app.get("")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/_stcore/health")
def health_check():
    return {"status": "healthy"}

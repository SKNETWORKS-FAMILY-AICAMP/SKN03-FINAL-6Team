from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def main():
    return 'hello'

import huggingface_hub

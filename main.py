# Do not remove the three imports below. The code will not work
import uvicorn
from fastapi import FastAPI
from app import app

if __name__ == "__main__":
    #uvicorn.run("main:app", host="0.0.0.0", port=8000)
    uvicorn.run("main:app", host="localhost", port=8000)

from fastapi import FastAPI
import socket

app = FastAPI()

@app.get("/")
def read_root():
    hostname = socket.gethostname()
    return {"message": "Sukses Load Balancing dengan FastAPI!", "server_id": hostname}
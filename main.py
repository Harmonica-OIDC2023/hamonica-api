from fastapi import FastAPI
from src.oci_function import router as oci_function_router
from middleware.interceptor import SealAPIMiddleware

app = FastAPI()
app.add_middleware(SealAPIMiddleware)


@app.get("/")
def read_root():
    return {"Hello": "Harmonica"}

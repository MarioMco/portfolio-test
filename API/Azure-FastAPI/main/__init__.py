from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import azure.functions as func

from ..routers import employee, offer

app = FastAPI()

app.include_router(employee.router)
app.include_router(offer.router)

@app.get("/")
def hello():
    return {"message": "welcome to my API!!!"}

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    return func.AsgiMiddleware(app).handle(req, context)
from fastapi import FastAPI
from .routers import user, employee, auth, offer


app = FastAPI()

app.include_router(user.router)
app.include_router(employee.router)
app.include_router(offer.router)
app.include_router(auth.router)

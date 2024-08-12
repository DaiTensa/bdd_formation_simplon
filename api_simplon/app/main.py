from fastapi import FastAPI
from app.routers import formations, formacodes


app = FastAPI()

# Include the routers
app.include_router(formations.router)
app.include_router(formacodes.router)
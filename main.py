# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.endpoints.flavors import router as flavor_router
from api.endpoints.toppings import router as topping_router
from api.endpoints.extra import router as extra_router
from api.endpoints.sales import router as sales_router
from api.endpoints.purchases import router as purchases_router
from api.endpoints.analytics import router as analytics_router
from database import create_db_and_tables

from models.toppings import Toppings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(flavor_router)
app.include_router(topping_router)
app.include_router(extra_router)
app.include_router(sales_router)
app.include_router(purchases_router)
app.include_router(analytics_router)

@app.on_event("startup")
def on_startup():
    print("created")
    create_db_and_tables()

from fastapi import FastAPI
from .models import *
from .db import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

from app.workplace import controllers
from app.auth import controllers
from app.rpc import rpc_router

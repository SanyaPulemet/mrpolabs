from fastapi import FastAPI
from controller import main_controller

app = FastAPI()

app.include_router(main_controller.router)
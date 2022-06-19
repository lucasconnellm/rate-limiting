from fastapi import FastAPI

from app.bootstrap import Bootstrap


app: FastAPI = Bootstrap.create_app()

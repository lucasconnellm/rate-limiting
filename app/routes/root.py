from datetime import datetime

from fastapi.routing import APIRouter
from pydantic import BaseModel


class Time(BaseModel):
    right_now: datetime


root_router: APIRouter = APIRouter()


@root_router.get("/", response_model=Time)
async def root() -> Time:
    return Time(right_now=datetime.now())

import sys

sys.path.insert(0, "../peewee_db_get/")
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from peewee_api_names import NameApi_1


file_path = Path(__file__).absolute()
file_dir_path = file_path.parent
original_working_path = Path("./").absolute()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


api = NameApi_1()

app = FastAPI()
sub_api = FastAPI()
sub_page = FastAPI()
app.mount("/api", sub_api)
app.mount("/page", sub_page)

# uvicorn fastapi:app --reload

app.mount("/static", StaticFiles(directory=file_dir_path / "static"), name="static")


@app.get("/")
def root():
    return {"message": "Hello World"}


@sub_page.get("/all_videos")
def all_videos_page():
    return FileResponse(file_dir_path / "./static/html/all_videos.html")


@sub_api.get("/all_videoItems")
def get_all_videoItems():
    videoItems = api.get_items2()
    return videoItems
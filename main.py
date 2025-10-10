from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fallback import fallback_coords
import os, json, random
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


with open("data/global_cities.json") as f:
    CITIES = json.load(f)

@app.get("/")
async def read_root(request: Request):
    coord = random.choice(CITIES)
    fallback = random.choice(fallback_coords)
    lat, lng = coord["lat"], coord["lng"]

    return templates.TemplateResponse("index.html", {
        "request": request,
        "API_KEY": os.getenv("GOOGLE_MAP_API"),
        "lat": lat,
        "lng": lng,
        "radius": 10000,
        "fallback_lat": fallback["lat"],
        "fallback_lng": fallback["lng"],
        "zoom": 2
    })

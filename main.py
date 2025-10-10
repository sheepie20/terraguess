from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fallback import fallback_coords
import os, json, random
from dotenv import load_dotenv
from shapely.geometry import shape, Point

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load city data
with open("data/global_cities.json") as f:
    CITIES = json.load(f)

# Load US GeoJSON shape
with open("data/gz_2010_us_outline_5m.json") as f:
    us_geojson = json.load(f)

us_shape = shape(us_geojson['features'][0]['geometry'])

def is_in_usa(lat, lng):
    """Check if a coordinate is inside the US using the GeoJSON."""
    point = Point(lng, lat)  # Shapely uses (x, y) -> (lng, lat)
    return us_shape.contains(point)

def get_usa_coord():
    """Return a random USA coordinate (city or fallback)."""
    coord = random.choice(CITIES)
    lat, lng = coord["lat"], coord["lng"]

    if not is_in_usa(lat, lng):
        coord = random.choice(fallback_coords[:9])
        lat, lng = coord["lat"], coord["lng"]

    fallback = random.choice(fallback_coords[:9])
    return {
        "lat": lat,
        "lng": lng,
        "radius": 5000,
        "fallback_lat": fallback["lat"],
        "fallback_lng": fallback["lng"],
        "zoom": 4
    }

# ---------- Root endpoint (global with optional country) ----------
@app.get("/")
async def root(request: Request, country: str = None):
    if country and country.upper() == "US":
        data = get_usa_coord()
    else:
        coord = random.choice(CITIES)
        fallback = random.choice(fallback_coords)
        lat, lng = coord["lat"], coord["lng"]
        data = {
            "lat": lat,
            "lng": lng,
            "radius": 10000,
            "fallback_lat": fallback["lat"],
            "fallback_lng": fallback["lng"],
            "zoom": 2
        }

    return templates.TemplateResponse("index.html", {
        "request": request,
        "API_KEY": os.getenv("GOOGLE_MAP_API"),
        **data
    })

# ---------- USA endpoint (still available separately) ----------
@app.get("/usa")
async def usa(request: Request):
    return get_usa_coord()

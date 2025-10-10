# TerraGuess

A web-based geographic guessing game that combines **Google Street View** and **Leaflet** maps. Users are presented with a random Street View panorama and must guess its location on a mini map. After submitting a guess, the map expands to fullscreen, showing the user's guess, the actual location, a connecting line, and the distance between them.

---

## Features

- **Random Street View panoramas** with a fallback location if unavailable.
- **Mini Leaflet map** for placing guesses.
- **Fullscreen map view** on submitting a guess.
- **Markers for guess and actual location**, connected by a line.
- **Distance calculation** between guess and actual location.
- **Top overlay** showing distance and a “Play Again” button.
- **English map tiles** (via Carto Positron).
- Fully **client-side rendering** with FastAPI backend supplying coordinates and API key.

---

## Technologies Used

- [FastAPI](https://fastapi.tiangolo.com/) – backend serving HTML and static assets.
- [Google Maps JavaScript API](https://developers.google.com/maps/documentation/javascript/overview) – for Street View panoramas.
- [Leaflet](https://leafletjs.com/) – interactive map for guessing.
- [Carto Positron tiles](https://carto.com/) – English-language base map tiles.
- HTML, CSS, JavaScript – frontend.

---

## Installation & Setup

1. **Clone the repository**

```bash
git clone https://github.com/sheepie20/terraguess.git
cd terraguess
````

2. **Install dependencies**

```bash
pip install fastapi uvicorn python-dotenv
```

3. **Create a `.env` file** with your Google Maps API key:

```env
GOOGLE_MAP_API=YOUR_GOOGLE_MAPS_API_KEY
```

4. **Run the FastAPI server**

```bash
uvicorn main:app --reload
```

5. **Open your browser** at `http://127.0.0.1:8000`.

---

## File Structure

```
streetview-geoguess/
│
├─ main.py              # FastAPI app
├─ templates/
│   └─ index.html       # HTML page
├─ static/
│   ├─ script.js        # JavaScript logic
│   └─ style.css        # CSS styles
├─ .env                 # Google Maps API key
└─ README.md
```

---

## Usage

1. The game shows a Street View panorama at a random location.
2. Click on the mini map to place your guess.
3. Click **Submit Guess**:

   * The mini map expands fullscreen.
   * Your guess and actual location are displayed.
   * A line connects your guess and the actual location.
   * The distance between your guess and the actual location is shown at the top.
4. Click **Play Again** to reload a new location.

---

## Customization

* **Change the fallback location** in `main.py` (`fallback_coords`).
* **Adjust the Street View radius** in `script.js` (`radius` variable).
* **Use different map tiles** by updating the Leaflet tile layer URL.

---

## License

MIT License – feel free to use and modify this project.

---

## Notes

* Make sure your Google Maps API key has **Street View and Maps JavaScript API** enabled.
* The game currently uses a **single guess marker** and expands the mini map to fullscreen when a guess is submitted.
* Map labels are in English using Carto Positron tiles.

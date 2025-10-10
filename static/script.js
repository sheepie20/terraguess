// ---------- Read config from HTML ----------
const actualLat = streetViewConfig.actualLat;
const actualLng = streetViewConfig.actualLng;
const fallbackLat = streetViewConfig.fallbackLat;
const fallbackLng = streetViewConfig.fallbackLng;
const radius = streetViewConfig.radius;

let streetViewLat = actualLat;
let streetViewLng = actualLng;

// ---------- Initialize Street View ----------
function initStreetView() {
    const streetViewService = new google.maps.StreetViewService();
    const request = {
        location: { lat: actualLat, lng: actualLng },
        radius: radius,
        preference: google.maps.StreetViewPreference.NEAREST,
        sources: [google.maps.StreetViewSource.OUTDOOR]
    };

    streetViewService.getPanorama(request, (data, status) => {
        if (status === google.maps.StreetViewStatus.OK) {
            streetViewLat = data.location.latLng.lat();
            streetViewLng = data.location.latLng.lng();

            new google.maps.StreetViewPanorama(document.getElementById("street-view"), {
                pano: data.location.pano,
                visible: true,
                pov: { heading: 165, pitch: 0 },
                zoom: 0,
                addressControl: false,  // hides location label
                linksControl: false,    // optional: hides arrows
                panControl: false,      // optional: hides pan control
                enableCloseButton: false
            });
        } else {
            console.warn("Using fallback location.");
            const fallbackRequest = {
                location: { lat: fallbackLat, lng: fallbackLng },
                radius: radius,
                preference: google.maps.StreetViewPreference.NEAREST,
                sources: [google.maps.StreetViewSource.OUTDOOR]
            };
            streetViewService.getPanorama(fallbackRequest, (data, status) => {
                if (status === google.maps.StreetViewStatus.OK) {
                    streetViewLat = data.location.latLng.lat();
                    streetViewLng = data.location.latLng.lng();

                    new google.maps.StreetViewPanorama(document.getElementById("street-view"), {
                        pano: data.location.pano,
                        visible: true,
                        pov: { heading: 165, pitch: 0 },
                        zoom: 0,
                        addressControl: false,
                        linksControl: false,
                        panControl: false,
                        enableCloseButton: false
                    });
                } else {
                    console.error("No panorama found for fallback coordinates.");
                }
            });
        }
    });
}

// ---------- Initialize Leaflet mini map (English tiles) ----------
const southWest = L.latLng(-85, -180);
const northEast = L.latLng(85, 180);
const worldBounds = L.latLngBounds(southWest, northEast);

const map = L.map('guess-map', {
    zoomControl: false,
    minZoom: 2,
    maxZoom: 18,
    maxBounds: worldBounds,
    maxBoundsViscosity: 1.0
}).setView([0, 0], 2);

// Carto Positron tiles (English)
L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; OpenStreetMap &copy; CARTO',
    subdomains: 'abcd',
    maxZoom: 19
}).addTo(map);

let guessMarker = null;
let actualMarker = null;
let lineBetween = null;

// ---------- Click to place guess ----------
map.on('click', function(e) {
    if (e.originalEvent.target.id === "submit-btn") return;

    if (guessMarker) map.removeLayer(guessMarker);

    guessMarker = L.marker(e.latlng, {
        icon: L.icon({
            iconUrl: 'https://maps.google.com/mapfiles/ms/icons/blue-dot.png',
            iconSize: [32, 32],
            iconAnchor: [16, 32]
        }),
        title: "Your Guess"
    }).addTo(map).bindPopup("Your Guess").openPopup();
});

// ---------- Submit Guess ----------
function submitGuess() {
    if (!guessMarker) return;

    const guessLatLng = guessMarker.getLatLng();

    // Remove previous actual marker or line
    if (actualMarker) map.removeLayer(actualMarker);
    if (lineBetween) map.removeLayer(lineBetween);

    // Add actual location marker
    actualMarker = L.marker([streetViewLat, streetViewLng], {
        icon: L.icon({
            iconUrl: 'https://maps.google.com/mapfiles/ms/icons/red-dot.png',
            iconSize: [32, 32],
            iconAnchor: [16, 32]
        }),
        title: "Actual Location"
    }).addTo(map).bindPopup("Actual Location").openPopup();

    // Draw line between guess and actual
    lineBetween = L.polyline([guessLatLng, [streetViewLat, streetViewLng]], {color: 'orange', weight: 3}).addTo(map);

    // Expand mini map to fullscreen
    const mapDiv = document.getElementById('guess-map');
    mapDiv.style.position = 'fixed';
    mapDiv.style.top = '0';
    mapDiv.style.left = '0';
    mapDiv.style.width = '100vw';
    mapDiv.style.height = '100vh';
    mapDiv.style.zIndex = '2000';
    map.invalidateSize();

    // Zoom map to fit both markers
    const group = L.featureGroup([guessMarker, actualMarker]);
    map.fitBounds(group.getBounds().pad(0.2));

    // Ensure guess marker stays visible
    guessMarker.addTo(map).bindPopup("Your Guess").openPopup();

    // ---------- Show distance and overlay ----------
    const R = 6371;
    const toRad = deg => deg * Math.PI / 180;
    const dLat = toRad(streetViewLat - guessLatLng.lat);
    const dLng = toRad(streetViewLng - guessLatLng.lng);
    const a = Math.sin(dLat/2)**2 +
              Math.cos(toRad(guessLatLng.lat)) *
              Math.cos(toRad(streetViewLat)) *
              Math.sin(dLng/2)**2;
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    const distance = R * c;

    // Top overlay
    let overlay = document.getElementById("guess-overlay");
    if (!overlay) {
        overlay = document.createElement("div");
        overlay.id = "guess-overlay";
        overlay.style.position = "fixed";
        overlay.style.top = "10px";
        overlay.style.left = "50%";
        overlay.style.transform = "translateX(-50%)";
        overlay.style.background = "rgba(255,255,255,0.9)";
        overlay.style.padding = "10px 20px";
        overlay.style.borderRadius = "8px";
        overlay.style.zIndex = "2100";
        overlay.style.fontFamily = "sans-serif";
        overlay.style.display = "flex";
        overlay.style.gap = "10px";
        document.body.appendChild(overlay);
    }

    overlay.innerHTML = `
        <span>Your guess is ${distance.toFixed(2)} km from the actual location.</span>
        <button id="guess-refresh-top" style="padding:5px 10px; cursor:pointer;">Play Again</button>
    `;

    document.getElementById("guess-refresh-top").addEventListener("click", () => {
        location.reload();
    });
}

// ---------- Bottom refresh button ----------
document.getElementById("guess-refresh").addEventListener("click", () => {
    location.reload();
});

// ---------- Fix rendering on hover / interaction ----------
const guessMapDiv = document.getElementById('guess-map');
guessMapDiv.addEventListener('mouseenter', () => setTimeout(() => map.invalidateSize(), 300));
guessMapDiv.addEventListener('mouseleave', () => setTimeout(() => map.invalidateSize(), 300));
map.on('mousedown', () => guessMapDiv.classList.add('interacting'));
map.on('mouseup', () => guessMapDiv.classList.remove('interacting'));
map.on('touchstart', () => guessMapDiv.classList.add('interacting'));
map.on('touchend', () => guessMapDiv.classList.remove('interacting'));

// ---------- Add Submit Guess button ----------
const submitBtn = L.control({position: 'bottomright'});
submitBtn.onAdd = function() {
    const div = L.DomUtil.create('div', 'leaflet-bar');
    div.innerHTML = '<button id="submit-btn" style="padding:5px 10px; cursor:pointer;">Submit Guess</button>';
    return div;
};
submitBtn.addTo(map);

// ---------- Submit event ----------
document.getElementById("submit-btn").addEventListener("click", submitGuess);

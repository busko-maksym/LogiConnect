'use client';

import React, { useState } from "react";
import { MapContainer, TileLayer, Polyline, Marker } from "react-leaflet";
import L from "leaflet"; // Для створення іконок
import "leaflet/dist/leaflet.css";

// Налаштування стандартної іконки для маркерів
const defaultIcon = L.icon({
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
  iconSize: [25, 41], // Розмір іконки
  iconAnchor: [12, 41], // Точка прив'язки (центр нижньої частини)
});

const App = () => {
  const [start, setStart] = useState(null); // Початкова локація
  const [end, setEnd] = useState(null); // Кінцева локація
  const [route, setRoute] = useState([]); // Координати маршруту
  const [distance, setDistance] = useState(null); // Відстань

  // Функція для обробки пошуку координат через Nominatim API
  const fetchCoordinates = async (location) => {
    const response = await fetch(
      `https://nominatim.openstreetmap.org/search?format=json&q=${location}`
    );
    const data = await response.json();
    if (data.length > 0) {
      return { name: location, coords: [parseFloat(data[0].lat), parseFloat(data[0].lon)] };
    }
    return null;
  };

  // Функція для обчислення маршруту через OSRM API
  const calculateRoute = async () => {
    if (start && end) {
      const url = `https://router.project-osrm.org/route/v1/driving/${start.coords[1]},${start.coords[0]};${end.coords[1]},${end.coords[0]}?overview=full&geometries=geojson`;
      const response = await fetch(url);
      const data = await response.json();

      if (data.routes.length > 0) {
        const routeCoordinates = data.routes[0].geometry.coordinates.map(([lon, lat]) => [lat, lon]);
        setRoute(routeCoordinates);
        setDistance((data.routes[0].distance / 1000).toFixed(2)); // Відстань у км
      }
    }
  };

  const handleSearch = async (location, setter) => {
    const result = await fetchCoordinates(location);
    if (result) setter(result);
  };

  return (
    <div style={{ display: "flex", height: "100vh" }}>
      {/* Ліва панель для вибору міст */}
      <div style={{ width: "30%", padding: "10px", backgroundColor: "#f9f9f9", borderRight: "1px solid #ddd" }}>
        <h3>Введіть міста</h3>
        <div>
          <label>Звідки:</label>
          <input
            type="text"
            placeholder="Наприклад, Львів"
            onBlur={(e) => handleSearch(e.target.value, setStart)}
            style={{ width: "100%", marginBottom: "10px", padding: "5px" }}
          />
        </div>
        <div>
          <label>Куди:</label>
          <input
            type="text"
            placeholder="Наприклад, Київ"
            onBlur={(e) => handleSearch(e.target.value, setEnd)}
            style={{ width: "100%", marginBottom: "10px", padding: "5px" }}
          />
        </div>
        <button
          onClick={calculateRoute}
          style={{ width: "100%", padding: "10px", backgroundColor: "#007BFF", color: "#fff", border: "none", cursor: "pointer" }}
        >
          Побудувати маршрут
        </button>

        {/* Відображення відстані */}
        {distance && (
          <div style={{ marginTop: "20px" }}>
            <h4>Результати:</h4>
            <p>Відстань: {distance} км</p>
          </div>
        )}
      </div>

      {/* Карта */}
      <div style={{ width: "70%" }}>
        <MapContainer
          center={start ? start.coords : [50.4501, 30.5234]} // Центруємо на початковій точці або Києві
          zoom={6}
          style={{ height: "100%", width: "100%" }}
        >
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          />
          {start && <Marker position={start.coords} icon={defaultIcon} />}
          {end && <Marker position={end.coords} icon={defaultIcon} />}
          {route.length > 0 && <Polyline positions={route} color="blue" />}
        </MapContainer>
      </div>
    </div>
  );
};

export default App;

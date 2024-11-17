import requests


def get_coordinates(city_name):
    # Nominatim API for geocoding
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": city_name,
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": "LogiConnect1.0 (maksikusplay@gmail.com)"  # Replace with your app name and email
    }

    try:
        response = requests.get(url, params=params, headers=headers)

        if response.status_code != 200:
            return False
        data = response.json()

        if not data:
            return False

        lat = float(data[0].get("lat", 0))
        lon = float(data[0].get("lon", 0))
        return [lat, lon]

    except Exception as e:
        return False

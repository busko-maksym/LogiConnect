import requests
from geopy.distance import geodesic
import math

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


def generate_intermediate_points(start, end, num_points=10):
    lat_step = (end[0] - start[0]) / num_points
    lon_step = (end[1] - start[1]) / num_points
    return [(start[0] + i * lat_step, start[1] + i * lon_step) for i in range(1, num_points + 1)]


def is_within_radius(point1, point2, radius_km=60):
    km = geodesic(point1, point2).kilometers
    print(km)
    return km <= radius_km


def consolidate_by_points(points, location_one, location_two, radius_km=30, cosine_threshold=0.8):
    vector_AB = get_vector(location_one[0], location_one[1])
    vector_CD = get_vector(location_two[0], location_two[1])

    cosine_sim = cosine_similarity(vector_AB, vector_CD)
    if cosine_sim < cosine_threshold:
        print("cosine: "+str(cosine_sim))
        return False
    start_match = any(is_within_radius(location_two[0], point, radius_km) for point in points)
    end_match = any(is_within_radius(location_two[1], point, radius_km) for point in points)
    print(start_match, end_match)
    return start_match and end_match


def get_vector(start, end):
    return (end[0] - start[0], end[1] - start[1])


def cosine_similarity(vector1, vector2):
    dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]
    magnitude1 = math.sqrt(vector1[0] ** 2 + vector1[1] ** 2)
    magnitude2 = math.sqrt(vector2[0] ** 2 + vector2[1] ** 2)

    if magnitude1 == 0 or magnitude2 == 0:
        return 0
    return dot_product / (magnitude1 * magnitude2)


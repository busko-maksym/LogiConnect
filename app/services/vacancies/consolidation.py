import math
from concurrent.futures import ThreadPoolExecutor

import requests
from bson import ObjectId
from geopy.distance import geodesic

from app.core.config import customer_db, cars_db, vacancies_db


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
    return km <= radius_km


def consolidate_by_points(points, location_one, location_two, radius_km=30, cosine_threshold=0.8):
    vector_AB = get_vector(location_one[0], location_one[1])
    vector_CD = get_vector(location_two[0], location_two[1])
    cosine_sim = cosine_similarity(vector_AB, vector_CD)
    if cosine_threshold < cosine_sim:
        home_way = False
    elif cosine_sim < -0.8:
        home_way = True
    else:
        return [None, False]
    start_match = any(is_within_radius(location_two[0], point, radius_km) for point in points)
    end_match = any(is_within_radius(location_two[1], point, radius_km) for point in points)
    return [home_way, start_match and end_match]


def get_vector(start, end):
    return (end[0] - start[0], end[1] - start[1])


def cosine_similarity(vector1, vector2):
    dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]
    magnitude1 = math.sqrt(vector1[0] ** 2 + vector1[1] ** 2)
    magnitude2 = math.sqrt(vector2[0] ** 2 + vector2[1] ** 2)

    if magnitude1 == 0 or magnitude2 == 0:
        return 0
    return dot_product / (magnitude1 * magnitude2)


def process_vacancy(vac, vacancy, points):
    if not isinstance(vac, dict) or "first_coords" not in vac or "second_coords" not in vac:
        print(f"Invalid vacancy format: {vac}")  # Debugging
        return None

    try:
        ab_vector = [tuple(vacancy["first_coords"]), tuple(vacancy["second_coords"])]
        cd_vector = [tuple(vac["first_coords"]), tuple(vac["second_coords"])]
    except TypeError as e:
        print(f"Type error with vacancy coordinates: {e}, vacancy: {vac}")
        return None

    consolid_results = consolidate_by_points(points, ab_vector, cd_vector)

    if consolid_results[0] is None or consolid_results[1] is False:
        return None

    vac["_id"] = str(vac["_id"])
    vac["user_id"] = str(vac["user_id"])
    vac.pop("applicants", None)  # Safely remove 'applicants' if it exists

    try:
        a, b = ab_vector
        c, d = cd_vector
        vac["avg_deviation"] = get_route_length_osrm([a, c, d, b]) - vac["distance"]
    except Exception as e:
        print(f"Error calculating deviation: {e}")
        vac["avg_deviation"] = None
    print(vac)
    return vac


def consolidation_return(vacancy_id, token):
    user = customer_db.find_one({"_id": ObjectId(token["user_id"])})
    car = cars_db.find_one({"user_id": ObjectId(token["user_id"])})
    vacancy = vacancies_db.find_one({"_id": ObjectId(vacancy_id)})
    query = {}

    if not user:
        return {"msg": "There is no user with this id in applicants"}

    if car:
        query["weight"] = {"$lt": car["weight"] - vacancy["weight"]}
        query["volume"] = {"$lt": car["volume"] - vacancy["volume"]}

    vacancies = list(vacancies_db.find(query))
    points = generate_intermediate_points(vacancy["first_coords"], vacancy["second_coords"])

    to_return = []

    # Use ThreadPoolExecutor to process vacancies in parallel
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(lambda vac: process_vacancy(vac, vacancy, points), vacancies))

    # Filter out None results
    to_return = [vac for vac in results if vac]

    return {"msg": to_return}


def get_route_length_osrm(coords):
    base_url = "http://router.project-osrm.org/route/v1/driving/"
    coord_string = ";".join([f"{lon},{lat}" for lat, lon in coords])
    url = f"{base_url}{coord_string}?overview=false"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['routes'][0]['distance'] / 1000
    else:
        raise Exception(f"Error fetching route: {response.status_code}, {response.text}")

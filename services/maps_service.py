import os
import httpx

API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

async def find_polling_stations(lat: float, lng: float) -> list:
    if not API_KEY:
        return []
    
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    stations = []
    
    try:
        async with httpx.AsyncClient() as client:
            # Search for polling booths
            params_booth = {
                "location": f"{lat},{lng}",
                "radius": 5000,
                "keyword": "polling booth",
                "key": API_KEY
            }
            response1 = await client.get(url, params=params_booth)
            data1 = response1.json()
            if "results" in data1:
                stations.extend(data1["results"])

            # Search for election offices
            params_office = {
                "location": f"{lat},{lng}",
                "radius": 5000,
                "keyword": "election office",
                "key": API_KEY
            }
            response2 = await client.get(url, params=params_office)
            data2 = response2.json()
            if "results" in data2:
                stations.extend(data2["results"])
                
        # Deduplicate and format
        formatted_stations = []
        seen_place_ids = set()
        for station in stations:
            place_id = station.get("place_id")
            if place_id not in seen_place_ids:
                seen_place_ids.add(place_id)
                formatted_stations.append({
                    "name": station.get("name"),
                    "address": station.get("vicinity"),
                    "lat": station["geometry"]["location"]["lat"],
                    "lng": station["geometry"]["location"]["lng"],
                    "place_id": place_id,
                    "rating": station.get("rating")
                })
        
        return formatted_stations
    except Exception as e:
        print(f"Error fetching polling stations: {e}")
        return []

async def geocode_address(address: str) -> dict:
    if not API_KEY:
        return {"error": "Maps API not configured"}
        
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": API_KEY
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            data = response.json()
            
            if data.get("status") == "OK" and len(data.get("results", [])) > 0:
                result = data["results"][0]
                return {
                    "lat": result["geometry"]["location"]["lat"],
                    "lng": result["geometry"]["location"]["lng"],
                    "formatted_address": result["formatted_address"]
                }
            else:
                return {"error": "Address not found"}
    except Exception as e:
        return {"error": f"Geocoding error: {str(e)}"}

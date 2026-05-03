from fastapi import APIRouter
from pydantic import BaseModel
from services.maps_service import find_polling_stations, geocode_address

router = APIRouter()

class LocationRequest(BaseModel):
    lat: float
    lng: float

@router.post("/api/polling-locations")
async def polling_locations_endpoint(request: LocationRequest):
    try:
        locations = await find_polling_stations(request.lat, request.lng)
        return {"locations": locations, "success": True}
    except Exception as e:
        return {"locations": [], "success": False, "error": str(e)}

@router.get("/api/geocode")
async def geocode_endpoint(address: str):
    try:
        result = await geocode_address(address)
        if "error" in result:
            return {"result": result, "success": False}
        return {"result": result, "success": True}
    except Exception as e:
        return {"result": {"error": str(e)}, "success": False}

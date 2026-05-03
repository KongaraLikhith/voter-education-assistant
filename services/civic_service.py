import os
import httpx

API_KEY = os.getenv("GOOGLE_CIVIC_API_KEY")
BASE_URL = "https://www.googleapis.com/civicinfo/v2"

FALLBACK_RESPONSE = {
    "fallback": True, 
    "message": "Civic data not available for this region. Using alternative sources."
}

async def get_elections(address: str) -> dict:
    if not API_KEY:
        return {"error": "Civic API not configured", **FALLBACK_RESPONSE}
        
    url = f"{BASE_URL}/elections"
    params = {"key": API_KEY}
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            
            if response.status_code != 200:
                return FALLBACK_RESPONSE
                
            data = response.json()
            if "elections" in data and len(data["elections"]) > 0:
                return data
            else:
                return FALLBACK_RESPONSE
    except Exception:
        return FALLBACK_RESPONSE

async def get_voter_info(address: str, election_id: str = "2000") -> dict:
    if not API_KEY:
        return {"error": "Civic API not configured", **FALLBACK_RESPONSE}
        
    url = f"{BASE_URL}/voterinfo"
    params = {
        "address": address,
        "electionId": election_id,
        "key": API_KEY
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            
            if response.status_code != 200:
                return FALLBACK_RESPONSE
                
            data = response.json()
            
            # Check if any useful data was returned
            has_polling = "pollingLocations" in data
            has_early = "earlyVoteSites" in data
            has_officials = "state" in data and any("electionAdministrationBody" in state for state in data["state"])
            
            if has_polling or has_early or has_officials:
                return data
            else:
                return FALLBACK_RESPONSE
    except Exception:
        return FALLBACK_RESPONSE

async def get_representatives(address: str) -> dict:
    if not API_KEY:
        return {"error": "Civic API not configured", **FALLBACK_RESPONSE}
        
    url = f"{BASE_URL}/representatives"
    params = {
        "address": address,
        "key": API_KEY
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            
            if response.status_code != 200:
                return FALLBACK_RESPONSE
                
            data = response.json()
            
            if "offices" in data and "officials" in data:
                return data
            else:
                return FALLBACK_RESPONSE
    except Exception:
        return FALLBACK_RESPONSE

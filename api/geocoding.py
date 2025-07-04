import requests
from typing import List, Dict, Any, Tuple

def search_location(query: str) -> List[Dict[str, Any]]:
    """Search for a location using Nominatim API."""
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": query, "format": "json", "limit": 5, "polygon_geojson": 1, "addressdetails": 1}
    headers = {"User-Agent": "Geopulse/1.0"}
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Nominatim API error: {e}")
        return []

def detect_state_from_nominatim_result(nominatim_result: Dict[str, Any]) -> Tuple[str, str]:
    """
    Detects state name and code from a Nominatim API result.
    This is a simplified approach and might need refinement for global coverage.
    """
    address = nominatim_result.get("address", {})
    state = address.get("state")
    country = address.get("country")
    country_code = address.get("country_code")

    # Prioritize state if available and within known Indian states
    if state:
        if state == "Uttar Pradesh":
            return "Uttar Pradesh", "up"
        elif state == "Maharashtra":
            return "Maharashtra", "mh"
        elif state == "West Bengal":
            return "West Bengal", "wb"
    
    # Fallback to country code if state is not specifically handled
    if country_code:
        return country, country_code.lower() # Use country name and lowercase country code

    return "Unknown", "unknown"

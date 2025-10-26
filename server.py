from fastmcp import FastMCP
from dotenv import load_dotenv
import requests
import os

load_dotenv()


def geocode_location(location: str) -> tuple[float, float]:
    """Convert location string to lat/lon using Nominatim"""
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": location,
        "format": "json",
        "limit": 1,
        "countrycodes": "de"  # Restrict to Germany
    }
    headers = {"User-Agent": "GasPriceMCP/1.0"}

    response = requests.get(url, params=params, headers=headers)
    results = response.json()

    if results:
        return float(results[0]["lat"]), float(results[0]["lon"])
    raise ValueError(f"Location '{location}' not found")


tankerkoenig_api_key = os.getenv("TANKERKOENIG_API_KEY")

mcp = FastMCP("German Gas Prices")


@mcp.tool
def get_gasprice_from_location(location: str) -> str:
    """
    Get the gas price from a location in Germany.
    """
    lat, lon = geocode_location(location)

    url = "https://creativecommons.tankerkoenig.de/json/list.php"
    params = {
        "lat": lat,
        "lng": lon,
        "rad": 5,  # 5km radius
        "sort": "dist",
        "type": "all",
        "apikey": tankerkoenig_api_key
    }

    response = requests.get(url, params=params)
    data = response.json()

    if not data.get("ok"):
        return f"Error: {data.get('message', 'Unknown error')}"

    stations = data.get("stations", [])

    def get_cheapest_price(station):
        prices = [p for p in [station.get('e5'), station.get('e10'), station.get('diesel')] if p]
        return min(prices) if prices else float('inf')

    stations = sorted(stations, key=get_cheapest_price)
    if not stations:
        return f"No gas stations found near {location}"

    result = f"Gas prices near {location} ({lat:.4f}, {lon:.4f}):\n\n"
    for i, station in enumerate(stations[:5], 1):
        result += f"{i}. {station['name']} - {station['brand']}\n"
        result += f"   Address: {station['street']}, {station['postCode']} {station['place']}\n"
        result += f"   Distance: {station['dist']:.2f} km\n"
        if station.get('diesel'):
            result += f"   Diesel: €{station['diesel']:.2f}\n"
        if station.get('e5'):
            result += f"   E5: €{station['e5']:.2f}\n"
        if station.get('e10'):
            result += f"   E10: €{station['e10']:.2f}\n"
        result += "\n"

    return result



mcp.run(transport="http", host="0.0.0.0", port=8000)


    


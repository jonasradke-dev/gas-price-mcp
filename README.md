# German Gas Prices MCP Server

A FastMCP server that provides real-time gas prices for locations in Germany using the Tankerkoenig API.

## Features

- Convert location names to coordinates using OpenStreetMap/Nominatim
- Find nearby gas stations within 5km radius
- Get current prices for Diesel, E5, and E10
- Results sorted by cheapest price

## Setup

1. **Install dependencies:**
```bash
pip install fastmcp requests python-dotenv
```

2. **Get a Tankerkoenig API key:**
- Register at https://creativecommons.tankerkoenig.de/
- Get your free API key

3. **Create `.env` file:**
```
TANKERKOENIG_API_KEY=your_api_key_here
```

## Usage

**Start the server:**
```bash
python server.py
```

The server will run on `http://0.0.0.0:8000`

**Available Tool:**
- `get_gasprice_from_location(location: str)` - Get gas prices for any location in Germany

**Example locations:**
- "Berlin"
- "Munich"
- "10115" (postal code)
- "Hauptstraße 1, Hamburg"

## How it works

1. Converts location string to latitude/longitude using Nominatim
2. Queries Tankerkoenig API for stations within 5km
3. Sorts results by cheapest available fuel price
4. Returns top 5 stations with prices and addresses

## API Credits

- **Geocoding:** OpenStreetMap Nominatim
- **Gas Prices:** Tankerkoenig (CreativeCommons)
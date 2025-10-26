# German Gas Prices MCP Server

A FastMCP server that provides real-time gas prices for locations in Germany using the Tankerkoenig API.

## Features

- Convert location names to coordinates using OpenStreetMap/Nominatim
- Find nearby gas stations within 5km radius
- Get current prices for Diesel, E5, and E10
- Results sorted by cheapest price

## Setup

1. **Install dependencies:**
```bashbuilöt
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

## Deployment

### Docker Compose (Recommended)

**On your server:**
```bash
# Clone repository
git clone https://github.com/jonasradke-dev/gas-price-mcp.git
cd gas-price-mcp

# Create .env file
echo "TANKERKOENIG_API_KEY=your_key_here" > .env

# Start the service
docker compose up -d

# View logs
docker compose logs -f

# Stop the service
docker compose down
```

**Update app:**
```bash
git pull
docker compose up -d --build
```

### Docker (Manual)

**Build and run:**
```bash
docker build -t gas-price-mcp .
docker run -d \
  --name gas-price-mcp \
  --restart unless-stopped \
  -p 8000:8000 \
  -e TANKERKOENIG_API_KEY=your_key \
  gas-price-mcp
```

### Railway

1. Push to GitHub
2. Go to [Railway](https://railway.app/) and create new project
3. Connect your GitHub repository
4. Add environment variable: `TANKERKOENIG_API_KEY`
5. Railway will auto-deploy

### Render

1. Go to [Render](https://render.com/) and create new Web Service
2. Connect your GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `python server.py`
5. Add environment variable: `TANKERKOENIG_API_KEY`
6. Deploy

### Fly.io

1. Install flyctl: https://fly.io/docs/flyctl/install/
2. Create `fly.toml`:
```toml
app = "gas-price-mcp"

[build]
  dockerfile = "Dockerfile"

[[services]]
  internal_port = 8000
  protocol = "tcp"

  [[services.ports]]
    port = 80
    handlers = ["http"]

  [[services.ports]]
    port = 443
    handlers = ["tls", "http"]
```

3. Deploy:
```bash
fly launch
fly secrets set TANKERKOENIG_API_KEY=your_key
fly deploy
```

## API Credits

- **Geocoding:** OpenStreetMap Nominatim
- **Gas Prices:** Tankerkoenig (CreativeCommons)
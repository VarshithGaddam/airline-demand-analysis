from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # For React to call backend
from data_processor import fetch_flight_data, get_insights_from_gemini
import pandas as pd

app = FastAPI()

# Allow CORS for React (localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/analyze/{airport_icao}")
def analyze(airport_icao: str):
    df = fetch_flight_data(airport_icao)
    if df.empty:
        return {"error": "No data available", "data": [], "insights": ""}

    # Prepare data for frontend (convert to JSON-friendly dict)
    raw_data = df[['callsign', 'origin_country', 'route', 'mock_price']].to_dict(orient='records')
    
    # Route counts for chart
    route_counts = df['route'].value_counts().to_dict()
    
    # Price trends (sorted prices)
    prices = df.sort_values('mock_price')['mock_price'].tolist()
    
    insights = get_insights_from_gemini(df)
    
    return {
        "raw_data": raw_data,
        "route_counts": route_counts,
        "prices": prices,
        "insights": insights
    }

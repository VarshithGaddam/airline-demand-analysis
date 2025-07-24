import requests
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def fetch_flight_data(airport_icao='YSSY'):  # Default to Sydney Airport
    """Fetch live flight data from OpenSky Network API as a proxy for demand."""
    url = f"https://opensky-network.org/api/states/all?icao24=&airport={airport_icao}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()['states']
        if data:
            df = pd.DataFrame(data, columns=[
                'icao24', 'callsign', 'origin_country', 'time_position', 'last_contact',
                'longitude', 'latitude', 'baro_altitude', 'on_ground', 'velocity',
                'true_track', 'vertical_rate', 'sensors', 'geo_altitude', 'squawk',
                'spi', 'position_source'
            ])
            # Clean data: Filter Australian flights
            df = df[df['origin_country'] == 'Australia']
            
            # Enhanced: Drop rows with NaN, empty, or whitespace in 'callsign'
            df = df.dropna(subset=['callsign'])
            df = df[df['callsign'].str.strip() != '']
            
            # Enhanced: Drop rows with NaN in other key columns for complete data
            df = df.dropna(subset=['longitude', 'latitude', 'velocity'])  # Critical for mock_price and location insights
            
            if df.empty:
                return pd.DataFrame()  # Return empty if no valid rows after cleaning
            
            # Add mock prices and routes (only on cleaned data)
            df['mock_price'] = (df['velocity'] * 0.1).astype(int) + 100  # Simulated prices
            df['route'] = df['callsign'].apply(lambda x: f"SYD-{x[:3]}")  # Simulated routes
            
            # Final check: Drop any newly created NaN (e.g., if lambda fails)
            df = df.dropna(subset=['mock_price', 'route'])
            
            return df
    return pd.DataFrame()  # Empty if no data

def get_insights_from_gemini(data_df):
    """Use Gemini API to extract insights from data."""
    if data_df.empty:
        return "No data available for analysis after cleaning null values."

    # Convert DataFrame to string for Gemini prompt
    data_str = data_df.to_csv(index=False)
    prompt = f"""
    Analyze this airline flight data (as proxy for booking demand):
    {data_str}
    
    Output the response in this exact plain-text structure (no Markdown, no bullets, use colons for labels, and line breaks for separation):
    
    Airline Flight Data Analysis
    This report provides a structured summary of the airline flight data analysis, focusing on popular routes, price trends, and high-demand periods or locations. It includes actionable insights derived from the data, along with considerations for limitations and improvements.
    1. Popular Routes
    The analysis identifies key routes based on the provided data, with a strong emphasis on origins and inferred destinations.
    Dominant Route: [Your analysis here]
    Most Frequent Destinations (Inferred from callsign prefixes; note these are not direct destination airports):
    [List items, one per line, e.g., JST (Jetstar): Description]
    Actionable Insight: [Your insight here]
    2. Price Trends (Mock Price Analysis)
    The mock price data was examined for patterns, but limitations were noted.
    Price Distribution: [Your analysis here]
    Actionable Insight: [Your insight here]
    3. High-Demand Periods or Locations
    Demand was assessed using timestamps, flight counts, and geographic indicators.
    Time Period: [Your analysis here]
    Locations (Inferred from on-ground status and coordinates):
    [List items, one per line, e.g., Sydney Airport (SYD): Description]
    Actionable Insight: [Your insight here]
    Additional Considerations (Data Limitations)
    Several constraints in the dataset affect the analysis reliability.
    [List items, one per line, e.g., Missing Data: Description]
    Recommendations for Improvement
    To enhance future analyses:
    [List items, one per line, e.g., More Data: Description]
    
    Fill in the [placeholders] with concise, actionable insights based on the data. Keep the entire output in plain text.
    """

    model = genai.GenerativeModel('gemini-1.5-flash')  # Updated to gemini-1.5-flash
    response = model.generate_content(prompt)
    return response.text

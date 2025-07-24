# Airline Demand Web App

## Overview
This is a full-stack web application for analyzing airline booking market demand trends, built for a group of hostels in Australia. It fetches live flight data from the OpenSky Network API (as a proxy for demand), processes and cleans it (removing null values), generates actionable insights using Google's Gemini AI, and displays results in an interactive React frontend with tables and charts.

### Key Features
- **Data Fetching & Cleaning**: Filters Australian flights, adds simulated prices/routes, and drops rows with null/missing values (e.g., in callsign).
- **AI Insights**: Uses Gemini to provide structured summaries on popular routes, price trends, and high-demand periods/locations.
- **Visualizations**: Responsive table with borders, bar/line charts for trends.

The app is built with free tools (FastAPI, React, Plotly/Chart.js, Gemini API) and meets the assignment criteria: functionality, insights, code quality, UX, and quick setup.

## Tech Stack
- **Backend**: Python 3.10, FastAPI, Pandas, Google Generative AI
- **Frontend**: React.js, Chart.js, Axios
- **APIs**: OpenSky Network (flight data), Google Gemini (insights)

## Project Structure
```
airline-demand-react-app/
├── backend/                    # Python backend
│   ├── app.py                 # FastAPI server with API endpoints
│   ├── data_processor.py      # Data fetching, cleaning, and Gemini integration
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # Local API keys (e.g., GEMINI_API_KEY)
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── App.js             # Main component with UI and API calls
│   │   ├── App.css            # Custom styles for table, charts, and insights
│   │   ├── index.js           # React entry point
│   │   └── ...                # Other auto-generated files from create-react-app
│   ├── package.json           # Node dependencies and scripts
│   └── public/                # Static assets (e.g., index.html)
└── README.md                  # This file
```

## Setup and Local Development

### Prerequisites
- Python 3.10
- Node.js 16+ and npm
- Gemini API key (from ai.google.dev)

### Backend Setup
1. Navigate to `backend/`:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Add your Gemini key to `.env`:
   ```bash
   GEMINI_API_KEY=your_key_here
   ```
4. Run the server:
   ```bash
   uvicorn app:app --reload
   ```
   - Access at `http://localhost:8000/analyze/YSSY` (test endpoint).

### Frontend Setup
1. Navigate to `frontend/`:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the dev server:
   ```bash
   npm start
   ```
   - Access at `http://localhost:3000`. It calls the local backend by default.

### Local Testing
- In the frontend, enter an ICAO code (e.g., YSSY for Sydney) and click "Fetch and Analyze."
- Verify: No null values in table, borders on cells, charts render, structured AI insights appear.

## Troubleshooting
- **Null Values**: Handled in `data_processor.py`; test with busy ICAO like YSSY.
- **API Quotas**: Monitor Gemini usage; upgrade if needed.

## Contact
For questions, contact [your email or GitHub].
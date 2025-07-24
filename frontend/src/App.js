import React, { useState } from 'react';
import axios from 'axios';
import { Bar, Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, LineElement, Title, Tooltip, Legend, PointElement } from 'chart.js';
import './App.css';

ChartJS.register(CategoryScale, LinearScale, BarElement, LineElement, PointElement, Title, Tooltip, Legend);

function App() {
  const [airport, setAirport] = useState('YSSY');
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [error, setError] = useState('');

  const fetchData = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await axios.get(`http://localhost:8000/analyze/${airport}`);
      setData(response.data);
    } catch (err) {
      setError('Error fetching data. Try another airport.');
    }
    setLoading(false);
  };

  return (
    <div className="app-container">
      <h1>Airline Booking Market Demand Analyzer</h1>
      <input
        type="text"
        value={airport}
        onChange={(e) => setAirport(e.target.value)}
        placeholder="Enter Airport ICAO (e.g., YSSY)"
        style={{ marginRight: '10px', padding: '5px' }}
      />
      <button onClick={fetchData} disabled={loading}>
        {loading ? 'Fetching...' : 'Fetch and Analyze'}
      </button>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {data && !data.error && (
        <>
          <h2>Raw Flight Data</h2>
          <table style={{ width: '100%', border: '1px solid #ccc' }}>
            <thead>
              <tr>
                <th>Callsign</th>
                <th>Origin Country</th>
                <th>Route</th>
                <th>Mock Price</th>
              </tr>
            </thead>
            <tbody>
              {data.raw_data.map((row, index) => (
                <tr key={index}>
                  <td>{row.callsign}</td>
                  <td>{row.origin_country}</td>
                  <td>{row.route}</td>
                  <td>{row.mock_price}</td>
                </tr>
              ))}
            </tbody>
          </table>

          <h2>Popular Routes Chart</h2>
          <Bar
            data={{
              labels: Object.keys(data.route_counts),
              datasets: [{ label: 'Count', data: Object.values(data.route_counts), backgroundColor: 'rgba(75,192,192,0.6)' }]
            }}
            options={{ responsive: true }}
          />

          <h2>Price Trends Chart</h2>
          <Line
            data={{
              labels: data.prices.map((_, i) => i + 1),  // X-axis as indices
              datasets: [{ label: 'Mock Price', data: data.prices, borderColor: 'rgba(153,102,255,1)' }]
            }}
            options={{ responsive: true }}
          />

          <h2>AI-Generated Insights</h2>
          <pre className="insights-pre">{data.insights}</pre>
        </>
      )}

      {data && data.error && <p style={{ color: 'red' }}>{data.error}</p>}
    </div>
  );
}

export default App;

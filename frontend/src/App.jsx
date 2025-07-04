import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [message, setMessage] = useState('')
  const [locationQuery, setLocationQuery] = useState('')
  const [searchResults, setSearchResults] = useState([])
  const [selectedLocation, setSelectedLocation] = useState(null)
  const [analysisResults, setAnalysisResults] = useState(null)
  const [error, setError] = useState(null)

  // Fetch initial message from backend
  useEffect(() => {
    fetch('/api/') // Changed to Vercel API route
      .then(res => res.json())
      .then(data => setMessage(data.message))
      .catch(err => setError('Failed to connect to backend: ' + err.message))
  }, [])

  const handleSearch = async () => {
    setError(null)
    try {
      const response = await fetch(`/api/search?query=${locationQuery}`) // Changed to Vercel API route
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const data = await response.json()
      setSearchResults(data)
    } catch (err) {
      setError('Failed to search location: ' + err.message)
    }
  }

  const handleAnalyze = async (location) => {
    setError(null)
    try {
      const response = await fetch('/api/analyze', { // Changed to Vercel API route
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          nominatim_result: location, // Send the full nominatim result
        }),
      })
      if (!response.ok) {
        const errData = await response.json()
        throw new Error(`HTTP error! status: ${response.status} - ${errData.error}`)
      }
      const data = await response.json()
      setAnalysisResults(data)
      setSelectedLocation(location)
      setSearchResults([]) // Clear search results after selection
    } catch (err) {
      setError('Failed to analyze location: ' + err.message)
    }
  }

  return (
    <div className="App">
      <h1>Geopulse: LULC Analysis Tool</h1>
      {error && <p style={{ color: 'red' }}>Error: {error}</p>}
      <p>Backend Message: {message}</p>

      <div>
        <input
          type="text"
          value={locationQuery}
          onChange={(e) => setLocationQuery(e.target.value)}
          placeholder="Search a location (e.g., Mumbai, New York)"
        />
        <button onClick={handleSearch}>Search</button>
      </div>

      {searchResults.length > 0 && (
        <div>
          <h2>Suggestions:</h2>
          <ul>
            {searchResults.map((loc, index) => (
              <li key={index}>
                {loc.display_name}
                <button onClick={() => handleAnalyze(loc)}>Analyze</button>
              </li>
            ))}
          </ul>
        </div>
      )}

      {selectedLocation && analysisResults && (
        <div>
          <h2>Selected Location: {selectedLocation.display_name}</h2>
          <h3>Analysis Results:</h3>

          <h4>Land Cover Class Trends Over Time</h4>
          {analysisResults.trends_plot_png && (
            <img src={`data:image/png;base64,${analysisResults.trends_plot_png}`} alt="Land Cover Trends" style={{ maxWidth: '100%' }} />
          )}

          <h4>Land Cover Maps Over 10 Years</h4>
          {analysisResults.yearly_maps_png && (
            <img src={`data:image/png;base64,${analysisResults.yearly_maps_png}`} alt="Yearly Land Cover Maps" style={{ maxWidth: '100%' }} />
          )}

          <h4>Satellite Overlay (Placeholder)</h4>
          {analysisResults.overlay_map_png && (
            <img src={`data:image/png;base64,${analysisResults.overlay_map_png}`} alt="Satellite Overlay" style={{ maxWidth: '100%' }} />
          )}

          {/* You can display trends_data in a table or other format if needed */}
          {/* <pre>{JSON.stringify(analysisResults.trends_data, null, 2)}</pre> */}
        </div>
      )}
    </div>
  )
}

export default App
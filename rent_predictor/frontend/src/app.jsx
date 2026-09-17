import { useState } from 'react';
import './app.css';

const apiBaseUrl = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8001';

function App() {
    const [rooms, setRooms] = useState(2);
    const [size, setSize] = useState(700);
    const [rent, setRent] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const predictRent = async (event) => {
        event.preventDefault();
        setError('');
        setRent(null);

        const roomCount = Number(rooms);
        const area = Number(size);
        if (!roomCount || roomCount < 1 || roomCount > 4 || !area || area < 100 || area > 1200) {
            setError('Enter 1-4 rooms and an area between 100 and 1,200 sq ft.');
            return;
        }

        setLoading(true);
        try {
            const res = await fetch(`${apiBaseUrl}/predict`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ rooms: roomCount, size_sqft: area })
            });
            if (!res.ok) throw new Error('Prediction request failed');
            const data = await res.json();
            setRent(data.predicted_rent);
        } catch {
            setError('Could not reach the prediction service. Make sure the backend is running.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <main className="app-shell">
            <nav className="topbar">
                <div className="brand-mark">JP</div>
                <span className="brand-name">Jack's Property Lab</span>
                <span className="status-pill"><span className="status-dot" /> Model online</span>
            </nav>

            <section className="hero-grid">
                <div className="hero-copy">
                    <p className="eyebrow">SMART RENT ESTIMATOR</p>
                    <h1>Find the right rent for your next address.</h1>
                    <p className="hero-text">Get a quick, data-backed estimate using the property's room count and floor area.</p>
                    <div className="trust-row">
                        <div className="trust-icon">01</div>
                        <div><strong>Simple inputs</strong><span>Two details. One clear estimate.</span></div>
                    </div>
                </div>

                <form className="prediction-card" onSubmit={predictRent}>
                    <div className="card-heading">
                        <div><p className="card-kicker">PROPERTY DETAILS</p><h2>Tell us about the home</h2></div>
                        <span className="card-step">1 / 1</span>
                    </div>

                    <label htmlFor="rooms">Number of rooms</label>
                    <div className="input-wrap"><input id="rooms" type="number" min="1" max="4" value={rooms} onChange={e => setRooms(e.target.value)} /><span>1-4 rooms</span></div>

                    <label htmlFor="size">Floor area</label>
                    <div className="input-wrap"><input id="size" type="number" min="100" max="1200" value={size} onChange={e => setSize(e.target.value)} /><span>100-1,200 sq ft</span></div>

                    <button className="predict-button" type="submit" disabled={loading}>{loading ? 'Calculating...' : 'Estimate monthly rent'} <span aria-hidden="true">-&gt;</span></button>
                    {error && <p className="error-message" role="alert">{error}</p>}

                    <div className={`result-panel ${rent ? 'has-result' : ''}`} aria-live="polite">
                        <span className="result-label">ESTIMATED MONTHLY RENT</span>
                        <strong>{rent ? `${rent.toLocaleString()} TK` : '---'}</strong>
                        <span className="result-note">Based on current property data</span>
                    </div>
                </form>
            </section>

            <footer><span>JACK'S PROPERTY LAB</span><span>Designed for faster decisions</span></footer>
          </main>
    );
}

export default App;
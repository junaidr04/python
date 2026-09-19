import { useState } from 'react';
import { ArrowRight, BadgeCheck, BedDouble, CircleHelp, Compass, House, Wifi } from 'lucide-react';
import './app.css';

const apiBaseUrl = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8002';
const areas = ['GEC', 'Agrabad', '2No Gate', 'Oxygen', 'Bayezid'];

function App() {
    const [form, setForm] = useState({
        area: 'GEC',
        rooms: '3',
        seat_type: 'Shared',
        bachelor_allowed: 'Yes',
        wifi: 'Yes',
    });
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const updateField = (field, value) => setForm(current => ({ ...current, [field]: value }));

    const predictRent = async event => {
        event.preventDefault();
        setResult(null);
        setError('');
        setLoading(true);
        try {
            const response = await fetch(`${apiBaseUrl}/predict-mess`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ ...form, rooms: Number(form.rooms) }),
            });
            if (!response.ok) throw new Error('Prediction request failed');
            setResult(await response.json());
        } catch {
            setError('Prediction service is offline. Start the backend on port 8002 and try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <main className="app-shell">
            <nav className="topbar">
                <a className="brand" href="/" aria-label="Mess Finder home">
                    <span className="brand-icon"><House size={18} strokeWidth={2.4} /></span>
                    <span><strong>Mess Finder</strong><small>smart seat rent estimate</small></span>
                </a>
                <div className="nav-meta"><span className="live-dot" /> Rent model online</div>
            </nav>

            <section className="hero-layout">
                <div className="hero-copy">
                    <p className="eyebrow"><Compass size={14} /> CHITTAGONG SEAT HUNTING, SIMPLIFIED</p>
                    <h1>A better seat starts with a <em>clear number.</em></h1>
                    <p className="hero-text">Tell us what kind of mess you need. Our local rent model gives you a realistic monthly estimate per seat, before you start calling around.</p>
                    <div className="proof-row">
                        <div className="proof-item"><BadgeCheck size={18} /><span><strong>Local data</strong><small>GEC to Bayezid</small></span></div>
                        <div className="proof-item"><BedDouble size={18} /><span><strong>Seat-first</strong><small>Built for bachelors</small></span></div>
                    </div>
                </div>

                <form className="finder-panel" onSubmit={predictRent}>
                    <div className="panel-topline"><span className="panel-label">YOUR SHORTLIST</span><span className="panel-count">01 <i>/</i> 01</span></div>
                    <div className="panel-heading"><h2>Find your seat range</h2><p>A few details, then we do the math.</p></div>

                    <label htmlFor="area">Preferred area</label>
                    <select id="area" value={form.area} onChange={event => updateField('area', event.target.value)}>
                        {areas.map(area => <option key={area}>{area}</option>)}
                    </select>

                    <div className="form-row">
                        <div><label htmlFor="rooms">Rooms in mess</label><select id="rooms" value={form.rooms} onChange={event => updateField('rooms', event.target.value)}>{[1, 2, 3, 4].map(room => <option key={room} value={room}>{room} {room === 1 ? 'room' : 'rooms'}</option>)}</select></div>
                        <div><label htmlFor="seat-type">Seat type</label><select id="seat-type" value={form.seat_type} onChange={event => updateField('seat_type', event.target.value)}><option>Shared</option><option>Single</option></select></div>
                    </div>

                    <div className="preference-row">
                        <div className="preference-label"><Wifi size={16} /><span>Wi-Fi included?</span></div>
                        <div className="segmented" role="group" aria-label="Wi-Fi included"><button type="button" className={form.wifi === 'Yes' ? 'selected' : ''} onClick={() => updateField('wifi', 'Yes')}>Yes</button><button type="button" className={form.wifi === 'No' ? 'selected' : ''} onClick={() => updateField('wifi', 'No')}>No</button></div>
                    </div>
                    <div className="preference-row"><div className="preference-label"><BadgeCheck size={16} /><span>Bachelor allowed?</span></div><div className="segmented" role="group" aria-label="Bachelor allowed"><button type="button" className={form.bachelor_allowed === 'Yes' ? 'selected' : ''} onClick={() => updateField('bachelor_allowed', 'Yes')}>Yes</button><button type="button" className={form.bachelor_allowed === 'No' ? 'selected' : ''} onClick={() => updateField('bachelor_allowed', 'No')}>No</button></div></div>

                    <button className="predict-button" type="submit" disabled={loading}>{loading ? 'Working it out...' : 'Estimate my seat rent'}<ArrowRight size={18} /></button>
                    {error && <p className="error-message" role="alert">{error}</p>}
                    <div className={`result-panel ${result ? 'has-result' : ''}`} aria-live="polite">
                        <div className="result-heading"><span>ESTIMATED MONTHLY RENT / SEAT</span>{result && <span className="result-area">{result.area}</span>}</div>
                        <strong>{result ? `৳${Math.round(result.predicted_rent_per_seat).toLocaleString()}` : '৳ — — —'}</strong>
                        <span className="result-note">{result ? 'A useful starting point for your search.' : 'Your estimate will appear here.'}</span>
                    </div>
                </form>
            </section>

            <section className="bottom-strip"><div><span className="strip-number">01</span><span><strong>Choose a neighbourhood</strong><small>Pick the area closest to campus or your routine.</small></span></div><div><span className="strip-number">02</span><span><strong>Set your seat style</strong><small>Compare shared comfort with single-seat privacy.</small></span></div><div><span className="strip-number">03</span><span><strong>Know your range</strong><small>Use the estimate to shortlist with confidence.</small></span></div><CircleHelp size={18} className="help-icon" /></section>
            <footer><span>MESS FINDER / 2026</span><span>Made for smarter seat hunting</span></footer>
        </main>
    );
}

export default App;

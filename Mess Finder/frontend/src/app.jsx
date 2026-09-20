import { useState } from 'react';
import { ArrowRight, BadgeCheck, BedDouble, ExternalLink, House, LoaderCircle, MapPin, MessageCircle, Wifi } from 'lucide-react';
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
    const resultPosition = result
        ? Math.min(100, Math.max(0, ((result.predicted_rent_per_seat - result.rent_range_min) / Math.max(1, result.rent_range_max - result.rent_range_min)) * 100))
        : 50;
    const hasObservedSpread = result && result.rent_range_min < result.rent_range_max;

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
                <div className="nav-meta"><span className="live-dot" /> Estimator online</div>
            </nav>

            <section className="hero-layout">
                <div className="hero-copy">
                    <p className="eyebrow">CHITTAGONG SEAT HUNTING, SIMPLIFIED</p>
                    <h1>Know the rent<br />before you <em>call around</em>.</h1>
                    <p className="hero-text">Tell us what kind of mess you need. Our local rent model gives you a realistic monthly range per seat, built from real listings in your area.</p>
                    <div className="proof-row">
                        <div className="proof-item"><MapPin size={18} /><span><strong>5 areas covered</strong><small>GEC to Bayezid</small></span></div>
                        <div className="proof-item"><BedDouble size={18} /><span><strong>Seat-first</strong><small>Built for bachelors</small></span></div>
                    </div>
                    <div className="area-coverage" aria-label="Areas covered by the dataset"><span className="area-chip-label">AREAS WE COVER</span><div className="area-chips"><span>GEC</span><span>Agrabad</span><span>2No Gate</span><span>Oxygen</span><span>Bayezid</span></div></div>
                    <div className="journey-panel">
                        <div className="journey-heading"><span>HOW IT WORKS</span><small>FROM SEARCH TO SHORTLIST</small></div>
                        <div className="journey-steps">
                            <div className="journey-step"><span className="journey-number">01</span><div><strong>Set your brief</strong><small>Choose an area, room count and seat style.</small></div></div>
                            <span className="journey-arrow"><ArrowRight size={15} /></span>
                            <div className="journey-step"><span className="journey-number">02</span><div><strong>Read the range</strong><small>See what similar local seats cost.</small></div></div>
                            <span className="journey-arrow"><ArrowRight size={15} /></span>
                            <div className="journey-step"><span className="journey-number">03</span><div><strong>Make a move</strong><small>Open the map or contact the owner.</small></div></div>
                        </div>
                    </div>
                </div>

                <form className="finder-panel" onSubmit={predictRent}>
                    <div className="panel-heading"><h2>Find your seat range</h2><p>A few details, then we do the math.</p></div>

                    <div className="field"><label htmlFor="area">Preferred area</label>
                    <select id="area" value={form.area} onChange={event => updateField('area', event.target.value)}>
                        {areas.map(area => <option key={area}>{area}</option>)}
                    </select></div>

                    <div className="form-row">
                        <div className="field"><label htmlFor="rooms">Rooms in mess</label><select id="rooms" value={form.rooms} onChange={event => updateField('rooms', event.target.value)}>{[1, 2, 3, 4].map(room => <option key={room} value={room}>{room} {room === 1 ? 'room' : 'rooms'}</option>)}</select></div>
                        <div className="field"><label>Seat type</label><div className="segmented" role="group" aria-label="Seat type"><button type="button" className={form.seat_type === 'Shared' ? 'selected' : ''} onClick={() => updateField('seat_type', 'Shared')}>Shared</button><button type="button" className={form.seat_type === 'Single' ? 'selected' : ''} onClick={() => updateField('seat_type', 'Single')}>Single</button></div></div>
                    </div>

                    <div className="switch-row"><div className="preference-label"><Wifi size={16} /><span>Wi-Fi included</span></div><button type="button" className={`switch ${form.wifi === 'Yes' ? 'on' : ''}`} onClick={() => updateField('wifi', form.wifi === 'Yes' ? 'No' : 'Yes')} aria-pressed={form.wifi === 'Yes'} aria-label="Wi-Fi included"><span /></button></div>
                    <div className="switch-row"><div className="preference-label"><BadgeCheck size={16} /><span>Bachelor allowed</span></div><button type="button" className={`switch ${form.bachelor_allowed === 'Yes' ? 'on' : ''}`} onClick={() => updateField('bachelor_allowed', form.bachelor_allowed === 'Yes' ? 'No' : 'Yes')} aria-pressed={form.bachelor_allowed === 'Yes'} aria-label="Bachelor allowed"><span /></button></div>

                    <button className="predict-button" type="submit" disabled={loading}>{loading ? <><LoaderCircle className="button-loader" size={17} /> Calculating range...</> : <>Estimate my seat rent<ArrowRight size={18} /></>}</button>
                    {error && <p className="error-message" role="alert">{error}</p>}
                    <div className={`result-panel ${result ? 'has-result' : ''}`} aria-live="polite">
                        <div className="result-heading"><span>{hasObservedSpread ? 'OBSERVED SAMPLE RANGE / SEAT' : 'ESTIMATED MONTHLY RENT / SEAT'}</span>{result && <span className="result-area">{result.area}</span>}</div>
                        <strong>{result ? hasObservedSpread ? `৳${result.rent_range_min.toLocaleString()} – ৳${result.rent_range_max.toLocaleString()}` : `৳${Math.round(result.predicted_rent_per_seat).toLocaleString()}` : '৳ — — —'}</strong>
                        <span className="result-note">{result ? 'A useful starting point for your search.' : 'Your estimate will appear here.'}</span>
                        {hasObservedSpread && <div className="range-meter"><div className="range-track"><span className="range-fill" style={{ width: `${resultPosition}%` }} /><span className="range-marker" style={{ left: `${resultPosition}%` }} /></div><div className="range-scale"><span>Observed low</span><span>Model midpoint</span><span>Observed high</span></div></div>}
                        {result && <div className="result-actions"><a href={result.location_link} target="_blank" rel="noreferrer"><MapPin size={15} /> View on map <ExternalLink size={13} /></a><a className="facebook-action" href={`https://www.facebook.com/search/top/?q=${encodeURIComponent(`${result.area} mess rent Chittagong`)}`} target="_blank" rel="noreferrer"><MessageCircle size={15} /> Contact</a></div>}
                        {result && <p className="result-disclaimer">{hasObservedSpread ? 'Range shown, not a fixed price. ' : 'Only one matching sample is available for this room and seat type. '}Based on limited sample data across 5 areas. Confirm exact rent and availability with the owner.</p>}
                    </div>
                </form>
            </section>

            <section className="bottom-strip"><div><span className="strip-number">01</span><span><strong>Choose a neighbourhood</strong><small>Pick the area closest to campus or your routine.</small></span></div><div><span className="strip-number">02</span><span><strong>Set your seat style</strong><small>Compare shared comfort with single-seat privacy.</small></span></div><div><span className="strip-number">03</span><span><strong>Know your range</strong><small>Use the estimate to shortlist with confidence.</small></span></div><div className="strip-note"><span>BUILT FOR REAL MOVES</span><strong>Estimate. Visit. Decide.</strong></div></section>
            <footer><span>MESS FINDER / 2026</span><span>Made for smarter seat hunting</span></footer>
        </main>
    );
}

export default App;

import { useState } from 'react';

function App() {
    const [rooms, setRooms] = useState(2);
    const [size, setSize] = useState(700);
    const [rent, setRent] = useState(null);

    const predictRent = async () => {
        const res = await fetch('http://127.0.0.1:8001/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ rooms: parseInt(rooms), size_sqft: parseInt(size) })
        });
        const data = await res.json();
        setRent(data.predicted_rent);
    };

    return (
        <div style={{ textAlign: 'center', marginTop: '80px', fontFamily: 'Arial' }}>
            <h1>Jack's Rent Predictor</h1>
            <input type="number" value={rooms} onChange={e => setRooms(e.target.value)} placeholder="Rooms" />
            <input type="number" value={size} onChange={e => setSize(e.target.value)} placeholder="Size sqft" />
            <br /><br />
            <button onClick={predictRent}>Predict Rent</button>
            {rent && <h2>Predicted Rent: {rent} TK</h2>}
        </div>
    );
}

export default App;
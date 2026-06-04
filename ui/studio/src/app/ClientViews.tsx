"use client";

import { useState, useEffect } from 'react';

export function IntentForm({ targetPath }: { targetPath: string }) {
  const [name, setName] = useState('');
  const [metric, setMetric] = useState('');
  
  const submit = async (e: any) => {
    e.preventDefault();
    await fetch('http://localhost:8000/intent', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ target: targetPath, name, metric })
    });
    setName(''); setMetric('');
    window.location.reload(); // Quick refresh for MVP
  };

  return (
    <form onSubmit={submit} style={{ marginTop: '1rem', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
      <input placeholder="Feature Name (e.g. Cyberpunk Button)" value={name} onChange={e => setName(e.target.value)} style={{ padding: '0.5rem', background: '#161b22', color: '#c9d1d9', border: '1px solid #30363d' }} required />
      <input placeholder="SLA / Heuristic (e.g. O(1) or Contrast 4.5:1)" value={metric} onChange={e => setMetric(e.target.value)} style={{ padding: '0.5rem', background: '#161b22', color: '#c9d1d9', border: '1px solid #30363d' }} required />
      <button type="submit" style={{ padding: '0.5rem', background: '#238636', color: 'white', border: 'none', cursor: 'pointer', fontWeight: 'bold' }}>Inject Intent Vector</button>
    </form>
  );
}

export function VisualGallery() {
  const [items, setItems] = useState([]);
  useEffect(() => {
    fetch('http://localhost:8000/gallery').then(r => r.json()).then(d => setItems(d.items));
  }, []);

  return (
    <div style={{ marginTop: '1rem', display: 'grid', gap: '1rem' }}>
      {items.map((item: any) => (
        <div key={item.id} style={{ padding: '1rem', border: '1px solid #30363d', borderRadius: '6px', background: '#161b22' }}>
          <h4>{item.component}</h4>
          <p style={{ color: item.grade === 'PASS' ? '#3fb950' : '#f85149' }}><strong>{item.grade}</strong>: {item.heuristics}</p>
          <small style={{ color: '#8b949e' }}>{item.timestamp}</small>
        </div>
      ))}
    </div>
  );
}

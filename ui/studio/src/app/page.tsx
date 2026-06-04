export default async function FeatureStudio() {
  // Server-side fetch to the Python FastAPI backend
  const res = await fetch('http://localhost:8000/status', { cache: 'no-store' }).catch(() => null);
  const data = res ? await res.json() : { features: [] };

  return (
    <div style={{ fontFamily: 'sans-serif', background: '#0d1117', color: '#c9d1d9', minHeight: '100vh', padding: '2rem' }}>
      <h1 style={{ color: '#58a6ff' }}>RotarySlider Feature Studio</h1>
      
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem', marginTop: '2rem' }}>
        {/* Next.js Server Component Pane */}
        <section style={{ border: '1px solid #30363d', padding: '1.5rem', borderRadius: '8px' }}>
          <h2>Intent Injection & Tally Matrix</h2>
          <ul>
            {data.features.map((feat: any, i: number) => (
              <li key={i} style={{ marginBottom: '1rem' }}>
                <strong>{feat.name}</strong> <br/>
                <span style={{ color: feat.status === 'tallied' ? '#3fb950' : '#d29922' }}>
                  [{feat.status.toUpperCase()}]
                </span> - {feat.intent}
              </li>
            ))}
          </ul>
        </section>

        {/* Embedded Svelte Micro-Frontend */}
        <section>
          <iframe 
            src="http://localhost:3001" 
            style={{ width: '100%', height: '100%', border: 'none', minHeight: '300px' }}
            title="Telemetry Engine"
          />
        </section>
      </div>
    </div>
  );
}

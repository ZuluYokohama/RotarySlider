import { IntentForm, VisualGallery } from './ClientViews';

export default async function FeatureStudio() {
  const targetPath = "/data/data/com.termux/files/home/desktop/target-project";
  const res = await fetch(`http://localhost:8000/status?target=${encodeURIComponent(targetPath)}`, { cache: 'no-store' }).catch(() => null);
  const data = res ? await res.json() : { features: [] };

  return (
    <div style={{ fontFamily: 'sans-serif', background: '#0d1117', color: '#c9d1d9', minHeight: '100vh', padding: '2rem' }}>
      <h1 style={{ color: '#58a6ff' }}>RotarySlider Feature Studio</h1>
      
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem', marginTop: '2rem' }}>
        
        {/* Left Column */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
          <section style={{ border: '1px solid #30363d', padding: '1.5rem', borderRadius: '8px' }}>
            <h2 style={{ borderBottom: '1px solid #30363d', paddingBottom: '0.5rem' }}>Inject New Intent</h2>
            <IntentForm targetPath={targetPath} />
          </section>

          <section style={{ border: '1px solid #30363d', padding: '1.5rem', borderRadius: '8px' }}>
            <h2 style={{ borderBottom: '1px solid #30363d', paddingBottom: '0.5rem' }}>Active Intent Vectors</h2>
            <ul style={{ marginTop: '1rem', listStyle: 'none', padding: 0 }}>
              {data.features.map((feat: any, i: number) => (
                <li key={i} style={{ marginBottom: '1rem', background: '#161b22', padding: '1rem', borderRadius: '6px' }}>
                  <strong>{feat.name}</strong> <br/>
                  <span style={{ color: feat.status === 'tallied' ? '#3fb950' : '#d29922' }}>
                    [{feat.status.toUpperCase()}]
                  </span> - {feat.intent}
                </li>
              ))}
            </ul>
          </section>
        </div>

        {/* Right Column */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
          <section style={{ height: '400px', border: '1px solid #30363d', borderRadius: '8px', overflow: 'hidden' }}>
            <iframe src="http://localhost:3001" style={{ width: '100%', height: '100%', border: 'none' }} title="Telemetry Engine" />
          </section>

          <section style={{ border: '1px solid #30363d', padding: '1.5rem', borderRadius: '8px' }}>
            <h2 style={{ borderBottom: '1px solid #30363d', paddingBottom: '0.5rem' }}>Visual V&V Gallery</h2>
            <VisualGallery />
          </section>
        </div>

      </div>
    </div>
  );
}

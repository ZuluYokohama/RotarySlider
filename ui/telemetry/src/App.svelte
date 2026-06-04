<script>
  import { onMount } from 'svelte';
  
  let telemetryData = { epoch: 0, cpu_allocated: 0, vram_status: 'Idle', message: 'Connecting...' };
  
  onMount(() => {
    const ws = new WebSocket('ws://localhost:8000/telemetry');
    ws.onmessage = (event) => {
      telemetryData = JSON.parse(event.data);
    };
    return () => ws.close();
  });
</script>

<main style="background: #0d1117; color: #3fb950; font-family: monospace; padding: 1rem; border: 1px solid #30363d; border-radius: 8px;">
  <h2>Matrix Telemetry (Zero-Latency)</h2>
  <p><strong>Epoch:</strong> {telemetryData.epoch}</p>
  <p><strong>CPU Leased:</strong> {telemetryData.cpu_allocated} Cores</p>
  <p><strong>VRAM:</strong> {telemetryData.vram_status}</p>
  <p><strong>System Log:</strong> {telemetryData.message}</p>
</main>

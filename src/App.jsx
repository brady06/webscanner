import React, { useState } from 'react';
import { invoke } from '@tauri-apps/api/tauri';

function App() {
  const [url, setUrl] = useState('');
  const [scanResult, setScanResult] = useState('');

  const runScanner = async () => {
    try {
      const result = await invoke("run_scan", { url });
      setScanResult(result);
    } catch (error) {
      console.error("Scan failed:", error);
      setScanResult("Error running scan.");
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Web Security Scanner</h1>
      <input
        type="text"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        placeholder="Enter URL to scan"
        style={{ width: '300px', marginRight: '10px' }}
      />
      <button onClick={runScanner}>Scan</button>
      <pre style={{ marginTop: '20px' }}>{scanResult}</pre>
    </div>
  );
}

export default App;

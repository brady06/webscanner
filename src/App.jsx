import React, { useState } from 'react';
import { invoke } from '@tauri-apps/api/core';


function App() {
  const [url, setUrl] = useState('');
  const [scanResult, setScanResult] = useState('');

  const runScanner = async () => {
    console.log("Method Activated")
    try {
      const result = await invoke("run_scan", { url });
      console.log("Method Passed 1")
      setScanResult(result);
      console.log("Method Passed 2")
      console.log("Result: " + result);
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

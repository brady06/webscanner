import React, { useState } from 'react';
import { invoke } from '@tauri-apps/api/core';


function App() {
  const [url, setUrl] = useState('');
  const [issues, setIssues] = useState([]);

  const runScanner = async () => {
    try {
      const result = await invoke("run_scan", { url });
      setIssues(result);
    } catch (error) {
      console.error("Scan failed:", error);
      setIssues([]);
    }
  };

  const high = issues.filter((i) => i.severity === "HIGH");
  const medium = issues.filter((i) => i.severity === "MEDIUM");
  const low = issues.filter((i) => i.severity === "LOW");

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
      <div style={{ marginTop: '20px' }}>
        <h2>High Severity</h2>
        <ul>
          {high.map((i, idx) => (
            <li key={`h-${idx}`}>{i.issue} - {i.url}</li>
          ))}
        </ul>
        <h2>Medium Severity</h2>
        <ul>
          {medium.map((i, idx) => (
            <li key={`m-${idx}`}>{i.issue} - {i.url}</li>
          ))}
        </ul>
        <h2>Low Severity</h2>
        <ul>
          {low.map((i, idx) => (
            <li key={`l-${idx}`}>{i.issue} - {i.url}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default App;

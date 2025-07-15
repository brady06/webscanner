import React, { useState } from 'react';
import { invoke } from '@tauri-apps/api/core';
import './App.css'

function App() {
  const [url, setUrl] = useState('');
  const [issues, setIssues] = useState([]);
  const [errorMsg, setErrorMsg] = useState('');

  const runScanner = async () => {
    try {
      const result = await invoke("run_scan", { url });
      if (result.error) {
        setErrorMsg(result.error);
        setIssues([]);
      } else {
        setErrorMsg('');
        setIssues(result);
      }
    } catch (error) {
      console.error("Scan failed:", error);
      setErrorMsg('URL not found');
      setIssues([]);
    }
  };

  const high = issues.filter((i) => i.severity === "HIGH");
  const medium = issues.filter((i) => i.severity === "MEDIUM");
  const low = issues.filter((i) => i.severity === "LOW");

  const groupByUrl = (list) =>
    list.reduce((acc, item) => {
      if (!acc[item.url]) acc[item.url] = [];
      acc[item.url].push(item.issue);
      return acc;
    }, {});

  const renderGroupedIssues = (grouped, prefix) =>
    Object.entries(grouped).map(([url, items]) => (
      <div key={`${prefix}-${url}`}>
        <h3>{url}</h3>
        <ul>
          {items.map((issue, idx) => (
            <li key={`${prefix}-${url}-${idx}`}>{issue}</li>
          ))}
        </ul>
      </div>
    ));

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
      {errorMsg ? (
        <p style={{ color: 'red', marginTop: '20px' }}>{errorMsg}</p>
      ) : (
        <div style={{ marginTop: '20px' }}>
          <h2>High Severity</h2>
          {high.length === 0 ? (
            <p>No high severity issues found.</p>
          ) : (
            renderGroupedIssues(groupByUrl(high), 'h')
          )}

          <h2>Medium Severity</h2>
          {medium.length === 0 ? (
            <p>No medium severity issues found.</p>
          ) : (
            renderGroupedIssues(groupByUrl(medium), 'm')
          )}

          <h2>Low Severity</h2>
          {low.length === 0 ? (
            <p>No low severity issues found.</p>
          ) : (
            renderGroupedIssues(groupByUrl(low), 'l')
          )}
        </div>
      )}
    </div>
  );
}

export default App;

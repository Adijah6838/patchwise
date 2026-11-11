import { useState, useEffect } from 'react';
import Editor from '@monaco-editor/react';
import { fetchApi } from '../lib/api';

export default function Submit() {
  const [code, setCode] = useState("def add(a, b):\n    return a + b\n");
  const [status, setStatus] = useState('');
  const [logs, setLogs] = useState<string[]>([]);
  const [wsStatus, setWsStatus] = useState('🔴 Disconnected');

  // Connect to WebSocket
  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws/');
    ws.onopen = () => setWsStatus('🟢 Live Connection Established');
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setStatus(`Status: ${data.status.toUpperCase()}`);
      setLogs((prev) => [`[${new Date().toLocaleTimeString()}] ${data.message}`, ...prev].slice(0, 10));
    };

    return () => { ws.onclose = null; ws.close(); }
  }, []);

  const handleSubmit = async () => {
    setStatus('Submitting...');
    setLogs([]);
    try {
      await fetchApi('/submissions/', {
        method: 'POST',
        body: JSON.stringify({
          challenge_id: "13623bb9-d518-4de1-9686-d7d24870e0a7",
          code_patch: code
        })
      });
    } catch (err: any) {
      setStatus(`❌ Error: ${err.message}`);
    }
  };

  return (
    <div className="container">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1>Submit Patch</h1>
        <span style={{ color: wsStatus.includes('🟢') ? 'var(--success)' : 'var(--danger)' }}>{wsStatus}</span>
      </div>
      
      <div className="grid">
        <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
          <Editor
            height="400px"
            defaultLanguage="python"
            theme="vs-dark"
            value={code}
            onChange={(val) => setCode(val || '')}
            options={{ minimap: { enabled: false }, fontSize: 14 }}
          />
        </div>
        
        <div className="card">
          <h3>Evaluation Status</h3>
          <div style={{ 
            padding: 15, 
            background: 'var(--bg-main)', 
            borderRadius: 6, 
            border: '1px solid var(--border)',
            color: status.includes('PASSED') ? 'var(--success)' : status.includes('FAILED') ? 'var(--danger)' : 'var(--accent)',
            fontWeight: 'bold',
            marginBottom: 15
          }}>
            {status || 'Waiting for submission...'}
          </div>
          
          <h4>Live Logs</h4>
          <div style={{ background: '#000', padding: 10, borderRadius: 6, fontFamily: 'monospace', fontSize: 12, minHeight: 150 }}>
            {logs.map((log, i) => <div key={i} style={{ color: '#00ff00' }}>{log}</div>)}
          </div>
        </div>
      </div>
      
      <button className="btn" onClick={handleSubmit} style={{ width: '100%', marginTop: 20 }}>Execute Evaluation</button>
    </div>
  );
}
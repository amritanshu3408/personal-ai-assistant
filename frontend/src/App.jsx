import React, { useState, useEffect, useRef } from 'react';

const WS_URL = 'ws://127.0.0.1:8000/ws';

export default function App() {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hi! I am your personal AI assistant. How can I help?' },
  ]);
  const [input, setInput] = useState('');
  const [connected, setConnected] = useState(false);
  const [status, setStatus] = useState('');
  const wsRef = useRef(null);
  const bottomRef = useRef(null);

  useEffect(() => {
    const ws = new WebSocket(WS_URL);
    wsRef.current = ws;

    ws.onopen = () => {
      setConnected(true);
      setStatus('Connected');
    };
    ws.onclose = () => {
      setConnected(false);
      setStatus('Disconnected – is the backend running?');
    };
    ws.onerror = () => setStatus('WebSocket error');
    ws.onmessage = (ev) => {
      try {
        const data = JSON.parse(ev.data);
        if (data.type === 'final') {
          setMessages((m) => [...m, { role: 'assistant', content: data.content }]);
          setStatus('');
        } else if (data.type === 'tool_call') {
          setStatus(`Calling tool: ${data.name}...`);
        } else if (data.type === 'tool_result') {
          setStatus(`Tool ${data.name} finished`);
        } else if (data.type === 'error') {
          setMessages((m) => [...m, { role: 'assistant', content: `Error: ${data.message}` }]);
          setStatus('');
        } else if (data.type === 'intent') {
          setStatus(`Intent: ${data.intent}`);
        }
      } catch (e) {
        console.error(e);
      }
    };

    return () => ws.close();
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const send = () => {
    if (!input.trim() || !wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) return;
    const text = input.trim();
    setMessages((m) => [...m, { role: 'user', content: text }]);
    wsRef.current.send(JSON.stringify({ type: 'text', content: text }));
    setInput('');
    setStatus('Thinking...');
  };

  return (
    <div className="app">
      <header className="header">
        <h1>Personal AI Assistant</h1>
        <span className={`badge ${connected ? 'on' : 'off'}`}>
          {connected ? 'Online' : 'Offline'}
        </span>
      </header>

      <div className="chat">
        {messages.map((m, i) => (
          <div key={i} className={`bubble ${m.role}`}>
            {m.content}
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      {status && <div className="status">{status}</div>}

      <div className="input-row">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && send()}
          placeholder="Type a message or ask me to open apps, search, remember..."
          disabled={!connected}
        />
        <button onClick={send} disabled={!connected || !input.trim()}>
          Send
        </button>
      </div>
    </div>
  );
}

import { useState, useRef, useEffect } from 'react'
import { Activity, Cpu, Database, Network, Shield, Zap, Send, Terminal } from 'lucide-react'
import './index.css'

function App() {
  const [messages, setMessages] = useState([
    { sender: 'jarvis', text: 'J.A.R.V.I.S. Online. Systems nominal. Awaiting command.' }
  ])
  const [input, setInput] = useState('')
  const [isProcessing, setIsProcessing] = useState(false)
  const [executionLog, setExecutionLog] = useState([])
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSend = async () => {
    if (!input.trim() || isProcessing) return
    
    const userPrompt = input.trim()
    setMessages(prev => [...prev, { sender: 'user', text: userPrompt }])
    setInput('')
    setIsProcessing(true)

    try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/chat/process', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt: userPrompt }),
      })
      
      const data = await response.json()
      
      setMessages(prev => [...prev, { sender: 'jarvis', text: data.response }])
      
      if (data.execution_log && data.execution_log.length > 0) {
        setExecutionLog(prev => [...prev, ...data.execution_log])
      }
    } catch (error) {
      setMessages(prev => [...prev, { sender: 'jarvis', text: `System Error: ${error.message}` }])
    } finally {
      setIsProcessing(false)
    }
  }

  return (
    <div className="hud-container">
      <header className="hud-header glass-panel">
        <h1 className="glow-text" style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <Shield size={32} /> J.A.R.V.I.S. Core Interface
        </h1>
        <div className="status-indicator">
          <div className={`dot ${isProcessing ? 'processing' : 'online'}`}></div>
          {isProcessing ? 'PROCESSING...' : 'SYSTEMS ONLINE'}
        </div>
      </header>

      <aside className="hud-sidebar-left">
        <div className="glass-panel" style={{ flex: 1 }}>
          <h3 className="glow-text" style={{ marginBottom: '15px', fontSize: '16px' }}>
            <Activity size={18} style={{ marginRight: '8px', verticalAlign: 'text-bottom' }} /> 
            System Telemetry
          </h3>
          <ul style={{ listStyle: 'none', lineHeight: '2', fontSize: '14px', color: 'var(--text-muted)' }}>
            <li>CPU LOAD: {isProcessing ? '89%' : '12%'}</li>
            <li>MEM ALLOC: {isProcessing ? '14.2 GB' : '4.1 GB'}</li>
            <li>NET UPLINK: STABLE</li>
            <li>CORE TEMP: {isProcessing ? '72°C' : '41°C'}</li>
          </ul>
        </div>
        
        <div className="glass-panel" style={{ flex: 1 }}>
           <h3 className="glow-text" style={{ marginBottom: '15px', fontSize: '16px' }}>
            <Terminal size={18} style={{ marginRight: '8px', verticalAlign: 'text-bottom' }} /> 
            Execution Log
          </h3>
          <div style={{ height: '250px', overflowY: 'auto' }}>
            {executionLog.length === 0 ? (
              <div style={{ color: 'var(--text-muted)', fontStyle: 'italic', fontSize: '14px' }}>Awaiting operational telemetry...</div>
            ) : (
              executionLog.map((log, idx) => (
                <div key={idx} className="log-entry">
                  <div className="log-tool">[{log.tool}]</div>
                  <div>{log.result?.status === 'success' ? 'EXECUTED SUCCESSFULLY' : 'EXECUTION FAILED'}</div>
                  {log.result?.data && <div style={{ opacity: 0.7, marginTop: '4px' }}>{JSON.stringify(log.result.data).substring(0, 100)}...</div>}
                </div>
              ))
            )}
          </div>
        </div>
      </aside>

      <main className="hud-main glass-panel" style={{ display: 'flex', flexDirection: 'column' }}>
        <div className="arc-reactor" style={{ marginBottom: '20px', flexShrink: 0 }}>
          <div className="arc-reactor-core"></div>
          <div className="arc-reactor-rings" style={{ animationDuration: isProcessing ? '2s' : '10s' }}></div>
        </div>

        <div className="message-list">
          {messages.map((msg, idx) => (
            <div key={idx} className={`message ${msg.sender}`}>
              <div className="message-sender">{msg.sender === 'jarvis' ? 'J.A.R.V.I.S.' : 'USER'}</div>
              <div>{msg.text}</div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>

        <div className="chat-input-container">
          <input 
            type="text" 
            className="chat-input" 
            placeholder="Awaiting command..." 
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            disabled={isProcessing}
          />
          <button className="chat-button" onClick={handleSend} disabled={isProcessing || !input.trim()}>
            <Send size={20} />
          </button>
        </div>
      </main>

      <aside className="hud-sidebar-right">
        <div className="glass-panel" style={{ flex: 1 }}>
          <h3 className="glow-text" style={{ marginBottom: '15px', fontSize: '16px' }}>
            <Network size={18} style={{ marginRight: '8px', verticalAlign: 'text-bottom' }} /> 
            Active Modules
          </h3>
          <ul style={{ listStyle: 'none', lineHeight: '2.5', fontSize: '14px' }}>
            <li style={{ color: 'var(--success-green)' }}><Zap size={14} /> Local LLM Engine</li>
            <li style={{ color: 'var(--success-green)' }}><Database size={14} /> File Forensics</li>
            <li style={{ color: 'var(--success-green)' }}><Network size={14} /> Web Search</li>
            <li style={{ color: 'var(--success-green)' }}><Cpu size={14} /> Web Scraper</li>
          </ul>
        </div>
      </aside>
    </div>
  )
}

export default App

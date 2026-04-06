import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Link, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { Home, MessageSquare, LayoutDashboard, LogOut, Send, Cpu, Activity, Clock, Mic } from 'lucide-react';
import axios from 'axios';

const API_BASE = 'http://localhost:5001/api';

// --- Components ---

const AssistantAnimation = ({ status }) => {
  const [angle, setAngle] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setAngle(prev => (prev + 3) % 360);
    }, 30);
    return () => clearInterval(interval);
  }, []);

  const getStatusConfig = () => {
    const s = status?.toLowerCase() || '';
    if (s.includes('listening')) return { color: '#E056FD', speed: 2.5, glow: '0 0 30px #E056FD' };
    if (s.includes('thinking')) return { color: '#F9CA24', speed: 4, glow: '0 0 30px #F9CA24' };
    if (s.includes('answering')) return { color: '#6AB04C', speed: 1.8, glow: '0 0 30px #6AB04C' };
    return { color: '#00ADB5', speed: 1, glow: '0 0 20px #00ADB5' };
  };

  const config = getStatusConfig();

  return (
    <div style={{ position: 'relative', width: '220px', height: '220px', margin: '20px auto', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      {/* Outer Glow Ring */}
      <motion.div
        animate={{ scale: [1, 1.15, 1], opacity: [0.3, 0.6, 0.3] }}
        transition={{ duration: 3, repeat: Infinity }}
        style={{
          position: 'absolute',
          width: '200px',
          height: '200px',
          borderRadius: '50%',
          background: `radial-gradient(circle, ${config.color}44 0%, transparent 70%)`,
          boxShadow: config.glow,
        }}
      />
      
      {/* Rotating Ring 1 */}
      <div style={{
        position: 'absolute',
        width: '160px',
        height: '160px',
        border: `2px dashed ${config.color}88`,
        borderRadius: '50%',
        transform: `rotate(${angle}deg)`,
        transition: 'border-color 0.5s ease',
      }} />

      {/* Rotating Ring 2 (Counter) */}
      <div style={{
        position: 'absolute',
        width: '130px',
        height: '130px',
        border: `3px solid ${config.color}`,
        borderRadius: '50%',
        borderTopColor: 'transparent',
        borderBottomColor: 'transparent',
        transform: `rotate(${-angle * 1.5}deg)`,
        transition: 'border-color 0.5s ease',
      }} />

      {/* Core */}
      <motion.div 
        animate={{ scale: [1, 1.1, 1] }}
        transition={{ duration: 1.5, repeat: Infinity }}
        style={{
          position: 'absolute',
          width: '40px',
          height: '40px',
          backgroundColor: config.color,
          borderRadius: '50%',
          boxShadow: `0 0 25px ${config.color}`,
          zIndex: 2,
        }} 
      />

      {/* Hexagon Pattern Placeholder */}
      <div style={{
        position: 'absolute',
        width: '180px',
        height: '180px',
        opacity: 0.1,
        background: `repeating-linear-gradient(60deg, ${config.color}, ${config.color} 1px, transparent 1px, transparent 20px)`,
        borderRadius: '50%',
      }} />
    </div>
  );
};

// --- Pages ---

const LoginPage = ({ onLogin }) => {
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post(`${API_BASE}/login`, { password });
      if (res.data.status === 'success') {
        onLogin(res.data.token);
      }
    } catch (err) {
      setError('Invalid Password');
    }
  };

  return (
    <div style={{ display: 'flex', height: '100vh', alignItems: 'center', justifyContent: 'center', background: '#1e1e1e' }}>
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        style={{ background: '#222831', padding: '40px', borderRadius: '15px', width: '350px', boxShadow: '0 10px 30px rgba(0,0,0,0.5)' }}
      >
        <h2 style={{ color: '#00ADB5', textAlign: 'center', marginBottom: '30px' }}>JARVIS ACCESS</h2>
        <form onSubmit={handleSubmit}>
          <input
            type="password"
            placeholder="Enter Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={{ width: '100%', padding: '12px', borderRadius: '8px', border: '1px solid #393E46', background: '#1a1a1a', color: 'white', marginBottom: '20px' }}
          />
          {error && <p style={{ color: 'red', fontSize: '12px' }}>{error}</p>}
          <button type="submit" style={{ width: '100%', padding: '12px', borderRadius: '8px', background: '#00ADB5', color: 'white', border: 'none', fontWeight: 'bold', cursor: 'pointer' }}>
            AUTHENTICATE
          </button>
        </form>
      </motion.div>
    </div>
  );
};

const Dashboard = () => {
  const [stats, setStats] = useState({ 
    total_chats: 0, 
    system_status: 'Active',
    platform: 'N/A',
    cpu_usage: 'N/A',
    memory_usage: 'N/A',
    uptime: 'N/A',
    disk_usage: 'N/A',
    python_version: 'N/A'
  });

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await axios.get(`${API_BASE}/stats`);
        setStats(res.data);
      } catch (err) {}
    };
    fetchStats();
    const interval = setInterval(fetchStats, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ padding: '30px', color: 'white', height: '100%', overflowY: 'auto', background: 'radial-gradient(circle at top right, #1a1a1a, #0f0f0f)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '40px' }}>
        <div>
          <h2 style={{ color: '#00ADB5', margin: 0, letterSpacing: '4px', fontSize: '24px' }}>SYSTEM ANALYTICS</h2>
          <p style={{ color: '#8b949e', fontSize: '12px', marginTop: '5px' }}>REAL-TIME HARDWARE MONITORING</p>
        </div>
        <div style={{ background: '#161b22', padding: '10px 20px', borderRadius: '20px', border: '1px solid #30363d', fontSize: '12px' }}>
          UPTIME: <span style={{ color: '#00ADB5', fontWeight: 'bold' }}>{stats.uptime}</span>
        </div>
      </div>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '20px', marginBottom: '40px' }}>
        <StatCard icon={<MessageSquare size={20} />} title="INTERACTIONS" value={stats.total_chats} color="#00ADB5" />
        <StatCard icon={<Cpu size={20} />} title="CPU LOAD" value={stats.cpu_usage} color="#F9CA24" />
        <StatCard icon={<Activity size={20} />} title="RAM USAGE" value={stats.memory_usage} color="#6AB04C" />
        <StatCard icon={<Home size={20} />} title="DISK SPACE" value={stats.disk_usage} color="#E056FD" />
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginBottom: '20px' }}>
        <div style={{ background: '#161b22', padding: '25px', borderRadius: '15px', border: '1px solid #30363d' }}>
          <h3 style={{ color: '#00ADB5', marginTop: 0, fontSize: '16px', marginBottom: '20px', borderBottom: '1px solid #30363d', paddingBottom: '10px' }}>PROJECT OVERVIEW</h3>
          <p style={{ color: '#c9d1d9', fontSize: '13px', lineHeight: '1.6', margin: 0 }}>
            In this project, when I ask any question in the backend, the question is first sent to the model. 
            The model decides the type of question (real-time, chat, automation, image generation, etc.). 
            After that, it sends the request to the specific code module and executes it to generate the output. 
            Real-time search and chat are handled using APIs, and image generation also uses APIs. 
            This backend is currently working, and it is connected with the frontend to display all data on the desktop.
          </p>
        </div>

        <div style={{ background: '#161b22', padding: '25px', borderRadius: '15px', border: '1px solid #30363d' }}>
          <h3 style={{ color: '#6AB04C', marginTop: 0, fontSize: '16px', marginBottom: '20px', borderBottom: '1px solid #30363d', paddingBottom: '10px' }}>CHAT ACTIVITY</h3>
          <div style={{ display: 'grid', gridTemplateColumns: '120px 1fr', gap: '15px', fontSize: '13px' }}>
            <div style={{ color: '#8b949e' }}>User Messages:</div>
            <div style={{ color: '#c9d1d9' }}>{stats.user_messages}</div>
            <div style={{ color: '#8b949e' }}>Jarvis Replies:</div>
            <div style={{ color: '#c9d1d9' }}>{stats.assistant_messages}</div>
            <div style={{ color: '#8b949e' }}>Last Interaction:</div>
            <div style={{ color: '#c9d1d9', fontStyle: 'italic', fontSize: '11px' }}>{stats.last_activity}</div>
          </div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
        <div style={{ background: '#161b22', padding: '25px', borderRadius: '15px', border: '1px solid #30363d' }}>
          <h3 style={{ color: '#F9CA24', marginTop: 0, fontSize: '16px', marginBottom: '20px', borderBottom: '1px solid #30363d', paddingBottom: '10px' }}>HARDWARE SPECS</h3>
          <div style={{ display: 'grid', gridTemplateColumns: '120px 1fr', gap: '15px', fontSize: '13px' }}>
            <div style={{ color: '#8b949e' }}>OS Platform:</div>
            <div style={{ color: '#c9d1d9' }}>{stats.platform}</div>
            <div style={{ color: '#8b949e' }}>Processor:</div>
            <div style={{ color: '#c9d1d9', fontSize: '11px' }}>{stats.processor}</div>
            <div style={{ color: '#8b949e' }}>Python:</div>
            <div style={{ color: '#c9d1d9' }}>v{stats.python_version}</div>
          </div>
        </div>

        <div style={{ background: '#161b22', padding: '25px', borderRadius: '15px', border: '1px solid #30363d' }}>
          <h3 style={{ color: '#E056FD', marginTop: 0, fontSize: '16px', marginBottom: '20px', borderBottom: '1px solid #30363d', paddingBottom: '10px' }}>RECENT LOGS (JSON DATA)</h3>
          <div style={{ maxHeight: '200px', overflowY: 'auto' }}>
            {!stats.chat_history_preview || stats.chat_history_preview.length === 0 ? (
              <div style={{ color: '#8b949e', fontSize: '13px' }}>No recent logs found.</div>
            ) : (
              stats.chat_history_preview.map((chat, idx) => (
                <div key={idx} style={{ padding: '10px', borderBottom: '1px solid #21262d', fontSize: '12px' }}>
                  <span style={{ color: chat.role === 'user' ? '#00ADB5' : '#6AB04C', fontWeight: 'bold', marginRight: '10px' }}>
                    {chat.role.toUpperCase()}:
                  </span>
                  <span style={{ color: '#c9d1d9' }}>{chat.content}</span>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

const StatCard = ({ icon, title, value, color }) => (
  <motion.div 
    whileHover={{ y: -5 }}
    style={{ background: '#222831', padding: '25px', borderRadius: '15px', border: '1px solid #393E46', boxShadow: '0 4px 15px rgba(0,0,0,0.3)' }}
  >
    <div style={{ display: 'flex', alignItems: 'center', gap: '12px', color: color, marginBottom: '15px' }}>
      {icon}
      <span style={{ fontSize: '11px', fontWeight: 'bold', letterSpacing: '1px' }}>{title}</span>
    </div>
    <div style={{ fontSize: '28px', fontWeight: 'bold' }}>{value}</div>
  </motion.div>
);

const Assistant = () => {
  const [status, setStatus] = useState('Available...');
  const [history, setHistory] = useState([]);
  const [input, setInput] = useState('');
  const [isSending, setIsSending] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const chatEndRef = React.useRef(null);
  const recognitionRef = React.useRef(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const sRes = await axios.get(`${API_BASE}/status`);
        setStatus(sRes.data.status);
        const cRes = await axios.get(`${API_BASE}/chat`);
        setHistory(cRes.data.history || []);
      } catch (err) {}
    };
    fetchData();
    const interval = setInterval(fetchData, 1000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [history]);

  useEffect(() => {
    if (typeof window === 'undefined') return;
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) return;
    const recognition = new SR();
    recognition.lang = 'en-US';
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.onresult = event => {
      if (!event.results || !event.results[0] || !event.results[0][0]) return;
      const transcript = event.results[0][0].transcript;
      setInput(prev => (prev ? prev + ' ' + transcript : transcript));
    };
    recognition.onend = () => {
      setIsListening(false);
    };
    recognition.onerror = () => {
      setIsListening(false);
    };
    recognitionRef.current = recognition;
    return () => {
      try {
        recognition.stop();
      } catch (e) {}
      recognitionRef.current = null;
    };
  }, []);

  const handleSend = async () => {
    if (!input.trim() || isSending) return;
    setIsSending(true);
    try {
      await axios.post(`${API_BASE}/send`, { message: input });
      setInput('');
    } catch (err) {}
    setIsSending(false);
  };

  const handleVoiceToggle = () => {
    const recognition = recognitionRef.current;
    if (!recognition) return;
    if (isListening) {
      try {
        recognition.stop();
      } catch (e) {}
      setIsListening(false);
      return;
    }
    try {
      recognition.start();
      setIsListening(true);
    } catch (e) {}
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%', padding: '20px', color: 'white', background: '#0f0f0f' }}>
      {/* Messages Container */}
      <div style={{ 
        flex: 1, 
        overflowY: 'auto', 
        marginBottom: '20px', 
        padding: '20px', 
        background: '#161b22', 
        borderRadius: '15px', 
        border: '1px solid #30363d',
        boxShadow: 'inset 0 0 10px rgba(0,0,0,0.5)'
      }}>
        {history.length === 0 && (
          <div style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#8b949e', fontStyle: 'italic', fontSize: '14px' }}>
            Initialize sequence... Waiting for command.
          </div>
        )}
        {history.map((msg, i) => (
          <motion.div 
            initial={{ opacity: 0, x: msg.role === 'user' ? 20 : -20 }}
            animate={{ opacity: 1, x: 0 }}
            key={i} 
            style={{ 
              marginBottom: '20px', 
              textAlign: msg.role === 'user' ? 'right' : 'left',
              display: 'flex',
              flexDirection: 'column',
              alignItems: msg.role === 'user' ? 'flex-end' : 'flex-start'
            }}
          >
            <div style={{ 
              fontSize: '10px', 
              color: msg.role === 'user' ? '#00ADB5' : '#8b949e', 
              marginBottom: '6px', 
              fontWeight: 'bold',
              letterSpacing: '1px'
            }}>
              {msg.role.toUpperCase()}
            </div>
            <div style={{ 
              background: msg.role === 'user' ? '#00ADB5' : '#21262d', 
              color: msg.role === 'user' ? 'white' : '#c9d1d9',
              padding: '12px 18px', 
              borderRadius: msg.role === 'user' ? '18px 18px 2px 18px' : '18px 18px 18px 2px', 
              maxWidth: '75%',
              fontSize: '14px',
              lineHeight: '1.5',
              boxShadow: '0 4px 12px rgba(0,0,0,0.2)',
              border: msg.role === 'user' ? 'none' : '1px solid #30363d'
            }}>
              {msg.content}
            </div>
          </motion.div>
        ))}
        <div ref={chatEndRef} />
      </div>
      
      {/* Assistant Status & Animation */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '40px', marginBottom: '20px' }}>
        <div style={{ textAlign: 'right', flex: 1 }}>
          <div style={{ color: '#8b949e', fontSize: '10px', fontWeight: 'bold' }}>SYSTEM STATUS</div>
          <div style={{ color: '#00ADB5', fontSize: '16px', fontWeight: 'bold', letterSpacing: '2px' }}>{status.toUpperCase()}</div>
        </div>
        
        <AssistantAnimation status={status} />
        
        <div style={{ textAlign: 'left', flex: 1 }}>
          <div style={{ color: '#8b949e', fontSize: '10px', fontWeight: 'bold' }}>VOICE ENGINE</div>
          <div style={{ color: '#6AB04C', fontSize: '16px', fontWeight: 'bold', letterSpacing: '2px' }}>READY</div>
        </div>
      </div>

      {/* Input Area */}
      <div style={{ position: 'relative', display: 'flex', gap: '15px', alignItems: 'center' }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          placeholder="ENTER COMMAND..."
          disabled={isSending}
          style={{ 
            flex: 1, 
            padding: '16px 25px', 
            borderRadius: '30px', 
            border: '1px solid #30363d', 
            background: '#161b22', 
            color: 'white',
            outline: 'none',
            fontSize: '14px',
            letterSpacing: '1px',
            transition: 'border-color 0.3s',
            boxShadow: '0 4px 15px rgba(0,0,0,0.3)'
          }}
          onFocus={(e) => e.target.style.borderColor = '#00ADB5'}
          onBlur={(e) => e.target.style.borderColor = '#30363d'}
        />
        <motion.button 
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={handleVoiceToggle}
          disabled={!recognitionRef.current}
          style={{ 
            width: '50px', 
            height: '50px', 
            borderRadius: '50%', 
            background: isListening ? '#6AB04C' : '#30363d', 
            border: 'none', 
            color: 'white', 
            cursor: !recognitionRef.current ? 'not-allowed' : 'pointer', 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'center',
            boxShadow: isListening ? '0 0 18px rgba(106,176,76,0.6)' : '0 0 12px rgba(0,0,0,0.4)',
            transition: 'background 0.3s, box-shadow 0.3s'
          }}
        >
          <Mic size={22} />
        </motion.button>
        <motion.button 
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={handleSend} 
          disabled={isSending}
          style={{ 
            width: '55px', 
            height: '55px', 
            borderRadius: '50%', 
            background: isSending ? '#30363d' : '#00ADB5', 
            border: 'none', 
            color: 'white', 
            cursor: isSending ? 'not-allowed' : 'pointer', 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'center',
            boxShadow: '0 0 20px rgba(0,173,181,0.4)',
            transition: 'background 0.3s'
          }}
        >
          <Send size={24} />
        </motion.button>
      </div>
    </div>
  );
};

// --- Main App ---

const App = () => {
  const [token, setToken] = useState(localStorage.getItem('token'));

  const handleLogin = (t) => {
    setToken(t);
    localStorage.setItem('token', t);
  };

  const handleLogout = () => {
    setToken(null);
    localStorage.removeItem('token');
  };

  if (!token) return <LoginPage onLogin={handleLogin} />;

  return (
    <Router>
      <div style={{ display: 'flex', height: '100vh', background: '#0f0f0f', color: '#e0e0e0', fontFamily: '"Segoe UI", Roboto, sans-serif' }}>
        {/* Sidebar */}
        <div style={{ 
          width: '80px', 
          background: '#161b22', 
          borderRight: '1px solid #30363d', 
          display: 'flex', 
          flexDirection: 'column', 
          alignItems: 'center', 
          padding: '30px 0',
          boxShadow: '2px 0 10px rgba(0,0,0,0.5)',
          zIndex: 10
        }}>
          <div style={{ marginBottom: '40px', color: '#00ADB5' }}>
            <motion.div animate={{ rotate: 360 }} transition={{ duration: 10, repeat: Infinity, ease: "linear" }}>
              <Cpu size={32} />
            </motion.div>
          </div>
          
          <NavLink to="/assistant" icon={<MessageSquare />} label="CHAT" />
          <NavLink to="/dashboard" icon={<LayoutDashboard />} label="STATS" />
          
          <div style={{ marginTop: 'auto', cursor: 'pointer', color: '#8b949e', transition: 'color 0.3s' }} 
               onClick={handleLogout}
               onMouseEnter={(e) => e.currentTarget.style.color = '#ff7b72'}
               onMouseLeave={(e) => e.currentTarget.style.color = '#8b949e'}>
            <LogOut size={24} />
          </div>
        </div>

        {/* Content Area */}
        <div style={{ flex: 1, position: 'relative', overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
          {/* Top Bar */}
          <div style={{ 
            height: '60px', 
            background: '#161b22', 
            borderBottom: '1px solid #30363d', 
            display: 'flex', 
            alignItems: 'center', 
            padding: '0 30px',
            justifyContent: 'space-between'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: '#6AB04C', boxShadow: '0 0 10px #6AB04C' }}></div>
              <span style={{ fontSize: '12px', fontWeight: 'bold', letterSpacing: '2px', color: '#8b949e' }}>JARVIS OS v4.0.1</span>
            </div>
            <div style={{ fontSize: '12px', color: '#8b949e', fontStyle: 'italic' }}>
              {new Date().toLocaleTimeString()} | SYSTEM SECURE
            </div>
          </div>

          <div style={{ flex: 1, overflow: 'hidden' }}>
            <Routes>
              <Route path="/assistant" element={<Assistant />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="*" element={<Navigate to="/assistant" />} />
            </Routes>
          </div>
        </div>
      </div>
    </Router>
  );
};

const NavLink = ({ to, icon, label }) => {
  const navigate = useNavigate();
  const isActive = window.location.pathname === to;

  return (
    <div 
      onClick={() => navigate(to)}
      style={{ 
        display: 'flex', 
        flexDirection: 'column', 
        alignItems: 'center', 
        gap: '5px', 
        marginBottom: '25px', 
        cursor: 'pointer',
        color: isActive ? '#00ADB5' : '#8b949e',
        transition: 'all 0.3s'
      }}
      onMouseEnter={(e) => !isActive && (e.currentTarget.style.color = '#c9d1d9')}
      onMouseLeave={(e) => !isActive && (e.currentTarget.style.color = '#8b949e')}
    >
      {icon}
      <span style={{ fontSize: '9px', fontWeight: 'bold' }}>{label}</span>
      {isActive && <motion.div layoutId="active" style={{ width: '4px', height: '4px', borderRadius: '50%', background: '#00ADB5', marginTop: '2px' }} />}
    </div>
  );
};

export default App;

import React, { useState, useEffect } from 'react';
import './App.css';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  BarChart, Bar, Cell, AreaChart, Area
} from 'recharts';
import {
  TrendingUp, TrendingDown, BarChart3, Calendar, Filter, RefreshCw,
  DollarSign, Activity, Zap, Clock, Award, AlertCircle
} from 'lucide-react';

function App() {
  const [prices, setPrices] = useState([]);
  const [events, setEvents] = useState([]);
  const [categories, setCategories] = useState([]);
  const [impacts, setImpacts] = useState([]);
  const [changePoint, setChangePoint] = useState(null);
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [hoveredEvent, setHoveredEvent] = useState(null);

  useEffect(() => {
    fetchAllData();
  }, []);

  const fetchAllData = async () => {
    try {
      const [priceRes, eventRes, catRes, impactRes, cpRes] = await Promise.all([
        fetch('http://localhost:5000/api/prices').then(r => r.json()),
        fetch('http://localhost:5000/api/events').then(r => r.json()),
        fetch('http://localhost:5000/api/categories').then(r => r.json()),
        fetch('http://localhost:5000/api/impacts').then(r => r.json()),
        fetch('http://localhost:5000/api/change-point').then(r => r.json())
      ]);
      
      setPrices(Array.isArray(priceRes) ? priceRes : []);
      setEvents(Array.isArray(eventRes) ? eventRes : []);
      setCategories(Array.isArray(catRes) ? catRes : []);
      setImpacts(Array.isArray(impactRes) ? impactRes : []);
      setChangePoint(cpRes || null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const filterEvents = async (category) => {
    setSelectedCategory(category);
    try {
      const url = category === 'All' 
        ? 'http://localhost:5000/api/events'
        : `http://localhost:5000/api/events?category=${category}`;
      const response = await fetch(url);
      const data = await response.json();
      setEvents(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error('Error filtering events:', err);
    }
  };

  // Calculate statistics
  const validPrices = prices
    .map(d => d.Price)
    .filter(p => p !== undefined && p !== null && !isNaN(p));
  
  const currentPrice = validPrices[validPrices.length - 1] || 0;
  const avgPrice = validPrices.reduce((a, b) => a + b, 0) / validPrices.length;
  const minPrice = Math.min(...validPrices);
  const maxPrice = Math.max(...validPrices);
  
  // Calculate price change (1 day)
  const priceChange = validPrices.length > 1 ? currentPrice - validPrices[validPrices.length - 2] : 0;
  const priceChangePercent = validPrices.length > 1 ? (priceChange / validPrices[validPrices.length - 2]) * 100 : 0;

  // Prepare chart data (sample every 10th point)
  const chartData = prices
    .filter((_, i) => i % 10 === 0)
    .map(item => ({
      date: item.Date ? new Date(item.Date).toLocaleDateString() : '',
      price: item.Price || 0
    }));

  // Impact chart data
  const impactData = impacts
    .sort((a, b) => Math.abs(b.impact) - Math.abs(a.impact))
    .slice(0, 10)
    .map(item => ({
      name: item.event?.length > 20 ? item.event.substring(0, 20) + '...' : item.event || 'Unknown',
      impact: item.impact || 0,
      category: item.category || 'Other',
      fullName: item.event || 'Unknown'
    }));

  const getColor = (value) => {
    if (value > 5) return '#10b981';
    if (value > 0) return '#34d399';
    if (value > -5) return '#f59e0b';
    return '#ef4444';
  };

  const categoryColors = {
    'Conflict': '#ef4444',
    'OPEC': '#3b82f6',
    'Economic': '#f59e0b',
    'Sanctions': '#8b5cf6',
    'Health': '#10b981',
    'Geopolitical': '#ec4899',
    'Political': '#14b8a6'
  };

  if (loading) {
    return (
      <div className="loader-container">
        <div className="loader-spinner"></div>
        <h2>Loading Dashboard...</h2>
        <p>Fetching Brent Oil Price Data</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-container">
        <AlertCircle size={48} />
        <h2>Something went wrong</h2>
        <p>{error}</p>
        <button onClick={() => window.location.reload()}>Try Again</button>
      </div>
    );
  }

  return (
    <div className="dashboard">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="logo">
          <div className="logo-icon">🛢️</div>
          <span>Oil<span>Dash</span></span>
        </div>
        <nav className="nav-menu">
          <a href="#" className="nav-item active">
            <Activity size={20} />
            <span>Dashboard</span>
          </a>
          <a href="#" className="nav-item">
            <BarChart3 size={20} />
            <span>Analysis</span>
          </a>
          <a href="#" className="nav-item">
            <Calendar size={20} />
            <span>Events</span>
          </a>
          <a href="#" className="nav-item">
            <Zap size={20} />
            <span>Insights</span>
          </a>
        </nav>
        <div className="sidebar-footer">
          <div className="status-dot"></div>
          <span>Live</span>
        </div>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        {/* Header */}
        <header className="top-header">
          <div className="header-left">
            <h1>Brent Oil Dashboard</h1>
            <p>Real-time market analysis & insights</p>
          </div>
          <div className="header-right">
            <span className="live-badge">● Live</span>
            <button className="refresh-btn" onClick={() => window.location.reload()}>
              <RefreshCw size={18} />
            </button>
          </div>
        </header>

        {/* Stats Grid */}
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-icon blue">
              <DollarSign size={24} />
            </div>
            <div className="stat-info">
              <span className="stat-label">Current Price</span>
              <div className="stat-value">${currentPrice.toFixed(2)}</div>
              <span className={`stat-change ${priceChange >= 0 ? 'positive' : 'negative'}`}>
                {priceChange >= 0 ? '▲' : '▼'} ${Math.abs(priceChange).toFixed(2)} ({priceChangePercent.toFixed(2)}%)
              </span>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon green">
              <TrendingUp size={24} />
            </div>
            <div className="stat-info">
              <span className="stat-label">Average Price</span>
              <div className="stat-value">${avgPrice.toFixed(2)}</div>
              <span className="stat-sub">All-time average</span>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon orange">
              <BarChart3 size={24} />
            </div>
            <div className="stat-info">
              <span className="stat-label">Price Range</span>
              <div className="stat-value">${minPrice.toFixed(2)} - ${maxPrice.toFixed(2)}</div>
              <span className="stat-sub">Min / Max</span>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon purple">
              <Award size={24} />
            </div>
            <div className="stat-info">
              <span className="stat-label">Total Records</span>
              <div className="stat-value">{prices.length.toLocaleString()}</div>
              <span className="stat-sub">Data points</span>
            </div>
          </div>
        </div>

        {/* Chart Section */}
        <div className="chart-section">
          <div className="section-header">
            <h2>Price History</h2>
            <div className="section-actions">
              <span className="badge">{chartData.length} data points</span>
            </div>
          </div>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height={350}>
              <AreaChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                <defs>
                  <linearGradient id="priceGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" opacity={0.1} />
                <XAxis dataKey="date" tick={{ fontSize: 10 }} interval="preserveEnd" minTickGap={50} />
                <YAxis tick={{ fontSize: 10 }} tickFormatter={(value) => `$${value}`} />
                <Tooltip
                  contentStyle={{ background: 'white', border: 'none', borderRadius: '12px', boxShadow: '0 10px 40px rgba(0,0,0,0.1)' }}
                />
                <Legend />
                <Area type="monotone" dataKey="price" stroke="#3b82f6" strokeWidth={2} fill="url(#priceGradient)" name="Brent Oil Price" />
              </AreaChart>
            </ResponsiveContainer>
            {changePoint && (
              <div className="change-point-banner">
                <Zap size={16} />
                <span>Biggest change detected: ${changePoint.change?.toFixed(2)} ({changePoint.percentage?.toFixed(1)}%) on {changePoint.date ? new Date(changePoint.date).toLocaleDateString() : ''}</span>
              </div>
            )}
          </div>
        </div>

        {/* Two Column Layout */}
        <div className="two-column">
          {/* Events Column */}
          <div className="events-section">
            <div className="section-header">
              <h2>📋 Events Timeline</h2>
              <span className="badge">{events.length}</span>
            </div>
            
            <div className="filter-bar">
              <Filter size={16} />
              <select
                value={selectedCategory}
                onChange={(e) => filterEvents(e.target.value)}
                className="filter-select"
              >
                <option value="All">All Categories</option>
                {categories.map((cat) => (
                  <option key={cat} value={cat}>{cat}</option>
                ))}
              </select>
            </div>

            <div className="events-list">
              {events.length > 0 ? (
                events.map((event, index) => (
                  <div 
                    key={index} 
                    className={`event-item ${hoveredEvent === index ? 'hovered' : ''}`}
                    onMouseEnter={() => setHoveredEvent(index)}
                    onMouseLeave={() => setHoveredEvent(null)}
                  >
                    <div className="event-dot" style={{ background: categoryColors[event.Category] || '#6b7280' }}></div>
                    <div className="event-content">
                      <span className="event-name">{event.Event}</span>
                      <span className="event-date">{event.Date ? new Date(event.Date).toLocaleDateString() : ''}</span>
                    </div>
                    <span className={`category-tag ${event.Category?.toLowerCase() || 'other'}`}>
                      {event.Category || 'Other'}
                    </span>
                  </div>
                ))
              ) : (
                <p className="empty-state">No events found</p>
              )}
            </div>
          </div>

          {/* Impact Column */}
          <div className="impact-section">
            <div className="section-header">
              <h2>📊 Event Impact</h2>
              <span className="badge">Top 10</span>
            </div>
            <div className="impact-chart-container">
              {impactData.length > 0 ? (
                <ResponsiveContainer width="100%" height={400}>
                  <BarChart data={impactData} layout="vertical" margin={{ top: 5, right: 20, left: 80, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" opacity={0.1} />
                    <XAxis type="number" tickFormatter={(value) => `$${value?.toFixed(0) || '0'}`} />
                    <YAxis type="category" dataKey="name" tick={{ fontSize: 10 }} width={80} />
                    <Tooltip
                      contentStyle={{ background: 'white', border: 'none', borderRadius: '12px', boxShadow: '0 10px 40px rgba(0,0,0,0.1)' }}
                    />
                    <Bar dataKey="impact" radius={[0, 4, 4, 0]}>
                      {impactData.map((entry, index) => (
                        <Cell key={index} fill={getColor(entry.impact)} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              ) : (
                <p className="empty-state">No impact data available</p>
              )}
              <div className="impact-legend">
                <span><span className="legend-dot green"></span> Positive</span>
                <span><span className="legend-dot yellow"></span> Moderate</span>
                <span><span className="legend-dot red"></span> Negative</span>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <footer className="dashboard-footer">
          <p>© 2026 Brent Oil Dashboard | Data sourced from historical oil prices</p>
          <p className="footer-stats">{prices.length} records • {events.length} events • {categories.length} categories</p>
        </footer>
      </main>
    </div>
  );
}

export default App;
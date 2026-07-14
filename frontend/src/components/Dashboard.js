import React, { useState, useEffect } from 'react';
import PriceChart from './PriceChart';
import Controls from './Controls';
import Metrics from './Metrics';
import ImpactChart from './ImpactChart';
import { getPrices, getEvents, getCategories, getImpacts, getChangePoint } from '../services/api';

const Dashboard = ({ stats }) => {
  const [prices, setPrices] = useState([]);
  const [events, setEvents] = useState([]);
  const [categories, setCategories] = useState([]);
  const [impacts, setImpacts] = useState([]);
  const [changePoint, setChangePoint] = useState(null);
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      console.log('Fetching data...');
      
      const [priceRes, eventRes, catRes, impactRes, cpRes] = await Promise.all([
        getPrices().catch(e => {
          console.error('Price fetch error:', e);
          return { data: [] };
        }),
        getEvents().catch(e => {
          console.error('Events fetch error:', e);
          return { data: [] };
        }),
        getCategories().catch(e => {
          console.error('Categories fetch error:', e);
          return { data: [] };
        }),
        getImpacts().catch(e => {
          console.error('Impacts fetch error:', e);
          return { data: [] };
        }),
        getChangePoint().catch(e => {
          console.error('Change point fetch error:', e);
          return { data: null };
        })
      ]);
      
      console.log('Price data received:', priceRes.data?.length || 0, 'records');
      console.log('Events received:', eventRes.data?.length || 0, 'records');
      console.log('Categories received:', catRes.data?.length || 0, 'categories');
      
      setPrices(Array.isArray(priceRes.data) ? priceRes.data : []);
      setEvents(Array.isArray(eventRes.data) ? eventRes.data : []);
      setCategories(Array.isArray(catRes.data) ? catRes.data : []);
      setImpacts(Array.isArray(impactRes.data) ? impactRes.data : []);
      setChangePoint(cpRes.data || null);
      
    } catch (error) {
      console.error('Error fetching data:', error);
      setError('Failed to load data. Please check the backend.');
    } finally {
      setLoading(false);
    }
  };

  const handleCategoryChange = async (category) => {
    setSelectedCategory(category);
    try {
      const response = await getEvents({ category: category === 'All' ? undefined : category });
      setEvents(Array.isArray(response.data) ? response.data : []);
    } catch (error) {
      console.error('Error filtering events:', error);
    }
  };

  const handleDateChange = async (start, end) => {
    try {
      const response = await getPrices({ start_date: start, end_date: end });
      setPrices(Array.isArray(response.data) ? response.data : []);
    } catch (error) {
      console.error('Error filtering prices:', error);
    }
  };

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '400px' }}>
        <div className="loader"></div>
        <p style={{ marginTop: '20px', color: '#666' }}>Loading dashboard data...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ textAlign: 'center', padding: '40px' }}>
        <h3>⚠️ Error Loading Data</h3>
        <p>{error}</p>
        <button onClick={fetchData} style={{ marginTop: '20px', padding: '10px 20px' }}>
          Retry
        </button>
      </div>
    );
  }

  // Show data count for debugging
  console.log('Rendering dashboard with:', {
    prices: prices.length,
    events: events.length,
    categories: categories.length,
    impacts: impacts.length
  });

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div>
          <h1>🛢️ <span>Brent Oil</span> Price Dashboard</h1>
          <p>Interactive analysis of oil prices and geopolitical events</p>
        </div>
        <div className="date">
          Updated: {new Date().toLocaleDateString()}
          <span style={{ marginLeft: '15px', fontSize: '0.8rem', color: '#666' }}>
            ({prices.length} records loaded)
          </span>
        </div>
      </header>

      <Metrics stats={stats} changePoint={changePoint} />

      <div className="dashboard-grid">
        <div className="chart-container">
          <h3>📈 Price History</h3>
          <PriceChart 
            data={prices} 
            events={events} 
            changePoint={changePoint} 
          />
        </div>
        <Controls
          categories={categories}
          selectedCategory={selectedCategory}
          onCategoryChange={handleCategoryChange}
          onDateChange={handleDateChange}
        />
      </div>

      <div className="events-list">
        <h3>📋 Events Timeline ({events.length})</h3>
        {events.length > 0 ? (
          events.map((event, index) => (
            <div key={index} className="event-item">
              <div className="event-info">
                <div className="event-name">{event.Event || 'Unknown Event'}</div>
                <div className="event-date">{event.Date ? new Date(event.Date).toLocaleDateString() : 'Unknown Date'}</div>
              </div>
              <span className={`event-category ${event.Category ? event.Category.toLowerCase() : 'other'}`}>
                {event.Category || 'Other'}
              </span>
            </div>
          ))
        ) : (
          <p style={{ textAlign: 'center', color: '#7f8c8d', padding: '20px' }}>
            No events found. Please check your key_events.csv file.
          </p>
        )}
      </div>

      <ImpactChart data={impacts} />
    </div>
  );
};

export default Dashboard;
import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Cell
} from 'recharts';

const ImpactChart = ({ data = [] }) => {
  // Ensure data is an array
  const safeData = Array.isArray(data) ? data : [];
  
  if (safeData.length === 0) {
    return (
      <div className="impact-chart">
        <h3>📊 Event Impact Analysis</h3>
        <div style={{ textAlign: 'center', padding: '40px', color: '#7f8c8d' }}>
          No impact data available
        </div>
      </div>
    );
  }

  const sortedData = [...safeData]
    .sort((a, b) => (b.impact || 0) - (a.impact || 0))
    .slice(0, 10);

  const chartData = sortedData.map(item => ({
    name: item.event?.length > 20 ? item.event.substring(0, 20) + '...' : item.event || 'Unknown',
    impact: item.impact || 0,
    percentage: item.percentage || 0,
    category: item.category || 'Other',
    fullName: item.event || 'Unknown'
  }));

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div style={{
          background: 'white',
          padding: '12px 16px',
          border: '1px solid #ddd',
          borderRadius: '8px',
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
          maxWidth: '300px'
        }}>
          <p style={{ fontWeight: 'bold', marginBottom: '5px' }}>{data.fullName}</p>
          <p style={{ color: '#7f8c8d', fontSize: '0.85rem' }}>Category: {data.category}</p>
          <p style={{ color: data.impact > 0 ? '#27ae60' : '#e74c3c' }}>
            Impact: ${data.impact?.toFixed(2) || '0'} ({data.percentage?.toFixed(2) || '0'}%)
          </p>
        </div>
      );
    }
    return null;
  };

  const getColor = (value) => {
    if (value > 5) return '#27ae60';
    if (value > 0) return '#2ecc71';
    if (value > -5) return '#f39c12';
    return '#e74c3c';
  };

  return (
    <div className="impact-chart">
      <h3>📊 Event Impact Analysis</h3>
      <p className="subtitle">
        Top 10 events by price impact (positive = price increase)
      </p>
      <ResponsiveContainer width="100%" height={350}>
        <BarChart
          data={chartData}
          layout="vertical"
          margin={{ top: 10, right: 30, left: 80, bottom: 10 }}
        >
          <CartesianGrid strokeDasharray="3 3" opacity={0.3} />
          <XAxis type="number" tickFormatter={(value) => `$${value?.toFixed(0) || '0'}`} />
          <YAxis type="category" dataKey="name" width={80} tick={{ fontSize: 10 }} />
          <Tooltip content={<CustomTooltip />} />
          <Legend wrapperStyle={{ fontSize: '12px' }} />
          <Bar dataKey="impact" name="Price Impact (USD)">
            {chartData.map((entry, index) => (
              <Cell key={index} fill={getColor(entry.impact)} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
      <div style={{ marginTop: '10px', fontSize: '0.8rem', color: '#7f8c8d' }}>
        <span>🟢 Positive impact  |  🟡 Moderate  |  🔴 Negative impact</span>
      </div>
    </div>
  );
};

export default ImpactChart;
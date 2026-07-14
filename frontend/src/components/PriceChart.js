import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ReferenceLine,
  ReferenceDot
} from 'recharts';

const PriceChart = ({ data = [], events = [], changePoint = null }) => {
  // Ensure data is an array
  const safeData = Array.isArray(data) ? data : [];
  
  console.log('PriceChart data length:', safeData.length);
  
  if (safeData.length === 0) {
    return (
      <div style={{ textAlign: 'center', padding: '40px', color: '#7f8c8d' }}>
        No price data available. Please check your data file.
      </div>
    );
  }

  // Take a sample for performance (show every 5th data point)
  const sampledData = safeData.filter((_, index) => index % 5 === 0);
  
  // Format data
  const chartData = sampledData.map(item => ({
    date: item.Date ? new Date(item.Date).toLocaleDateString() : '',
    price: item.Price || 0,
    ...item
  }));

  // Custom tooltip
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div style={{
          background: 'white',
          padding: '12px 16px',
          border: '1px solid #ddd',
          borderRadius: '8px',
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
        }}>
          <p style={{ fontWeight: 'bold', marginBottom: '5px' }}>{label}</p>
          <p style={{ color: '#2563eb' }}>
            Price: ${payload[0]?.value?.toFixed(2) || 'N/A'}
          </p>
        </div>
      );
    }
    return null;
  };

  // Find events in range
  const safeEvents = Array.isArray(events) ? events : [];
  const eventsInRange = safeEvents.filter(event => {
    try {
      const eventDate = new Date(event.Date);
      const firstDate = new Date(safeData[0]?.Date);
      const lastDate = new Date(safeData[safeData.length - 1]?.Date);
      return eventDate >= firstDate && eventDate <= lastDate;
    } catch {
      return false;
    }
  });

  return (
    <div style={{ height: 380 }}>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart
          data={chartData}
          margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
        >
          <CartesianGrid strokeDasharray="3 3" opacity={0.3} />
          <XAxis
            dataKey="date"
            tick={{ fontSize: 10 }}
            interval="preserveEnd"
            minTickGap={50}
          />
          <YAxis
            domain={['auto', 'auto']}
            tick={{ fontSize: 10 }}
            tickFormatter={(value) => `$${value}`}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend wrapperStyle={{ fontSize: '12px' }} />

          <Line
            type="monotone"
            dataKey="price"
            stroke="#2563eb"
            strokeWidth={2}
            dot={false}
            name="Brent Oil Price"
          />

          {changePoint && changePoint.date && (
            <ReferenceLine
              x={new Date(changePoint.date).toLocaleDateString()}
              stroke="#ef4444"
              strokeDasharray="5 5"
              label={{
                value: 'Change Point',
                position: 'top',
                fill: '#ef4444',
                fontSize: 10
              }}
            />
          )}

          {eventsInRange.slice(0, 20).map((event, index) => {
            try {
              const eventDate = new Date(event.Date).toLocaleDateString();
              const dataPoint = chartData.find(d => d.date === eventDate);
              if (!dataPoint) return null;

              return (
                <ReferenceDot
                  key={index}
                  x={eventDate}
                  y={dataPoint.price}
                  r={5}
                  fill="#ef4444"
                  stroke="white"
                  strokeWidth={2}
                />
              );
            } catch {
              return null;
            }
          })}
        </LineChart>
      </ResponsiveContainer>
      <div style={{ marginTop: '8px', fontSize: '0.8rem', color: '#7f8c8d' }}>
        <span>● Red dots: Events</span>
        {changePoint && changePoint.date && (
          <span style={{ marginLeft: '15px' }}>
            ● Red dashed line: Change Point
          </span>
        )}
        <span style={{ marginLeft: '15px' }}>
          📊 Showing {chartData.length} data points
        </span>
      </div>
    </div>
  );
};

export default PriceChart;
import React from 'react';

const Metrics = ({ stats = {}, changePoint = null }) => {
  // Ensure stats is an object
  const safeStats = stats || {};
  
  console.log('Metrics stats:', safeStats);
  
  const metrics = [
    { 
      label: 'Current Price', 
      value: safeStats.current_price ? `$${safeStats.current_price.toFixed(2)}` : '$N/A' 
    },
    { 
      label: 'Average Price', 
      value: safeStats.avg_price ? `$${safeStats.avg_price.toFixed(2)}` : '$N/A' 
    },
    { 
      label: 'Min Price', 
      value: safeStats.min_price ? `$${safeStats.min_price.toFixed(2)}` : '$N/A' 
    },
    { 
      label: 'Max Price', 
      value: safeStats.max_price ? `$${safeStats.max_price.toFixed(2)}` : '$N/A' 
    },
  ];

  if (changePoint && changePoint.change !== undefined) {
    metrics.push({ 
      label: 'Biggest Change', 
      value: `$${changePoint.change?.toFixed(2) || '0'}`,
      change: `${changePoint.percentage?.toFixed(2) || '0'}%`
    });
  }

  return (
    <div className="metrics-grid">
      {metrics.map((metric, index) => (
        <div key={index} className="metric-card">
          <div className="label">{metric.label}</div>
          <div className="value">{metric.value}</div>
          {metric.change && (
            <div className={`change ${metric.change.startsWith('-') ? 'negative' : 'positive'}`}>
              {metric.change}
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export default Metrics;
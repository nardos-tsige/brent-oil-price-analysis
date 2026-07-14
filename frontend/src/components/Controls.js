import React, { useState } from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';

const Controls = ({ 
  categories = [], 
  selectedCategory = 'All', 
  onCategoryChange = () => {}, 
  onDateChange = () => {} 
}) => {
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);

  const handleApplyFilter = () => {
    if (startDate && endDate) {
      onDateChange(
        startDate.toISOString().split('T')[0],
        endDate.toISOString().split('T')[0]
      );
    }
  };

  const handleClearFilter = () => {
    setStartDate(null);
    setEndDate(null);
    onDateChange(null, null);
  };

  // Ensure categories is an array
  const safeCategories = Array.isArray(categories) ? categories : [];

  return (
    <div className="controls-container">
      <h3>🎛️ Controls</h3>

      <div className="control-group">
        <label>Event Category</label>
        <select
          value={selectedCategory}
          onChange={(e) => onCategoryChange(e.target.value)}
        >
          <option value="All">All Categories</option>
          {safeCategories.map((category, index) => (
            <option key={index} value={category}>{category}</option>
          ))}
        </select>
      </div>

      <div className="control-group">
        <label>Date Range</label>
        <div style={{ display: 'flex', gap: '8px' }}>
          <DatePicker
            selected={startDate}
            onChange={(date) => setStartDate(date)}
            placeholderText="Start Date"
            className="date-picker"
            style={{ flex: 1, padding: '8px', border: '1px solid #ddd', borderRadius: '6px' }}
          />
          <DatePicker
            selected={endDate}
            onChange={(date) => setEndDate(date)}
            placeholderText="End Date"
            className="date-picker"
            style={{ flex: 1, padding: '8px', border: '1px solid #ddd', borderRadius: '6px' }}
          />
        </div>
        <div className="btn-group" style={{ marginTop: '8px' }}>
          <button className="btn btn-primary" onClick={handleApplyFilter}>
            Apply Filter
          </button>
          <button className="btn btn-secondary" onClick={handleClearFilter}>
            Clear
          </button>
        </div>
      </div>

      <div className="control-group">
        <button className="btn btn-success" onClick={() => window.location.reload()}>
          🔄 Refresh Data
        </button>
      </div>

      <div className="info-box">
        <p>📊 {safeCategories.length} event categories</p>
        <p>💡 Click events to highlight on chart</p>
      </div>
    </div>
  );
};

export default Controls;
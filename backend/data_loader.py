import pandas as pd
import numpy as np
import os
import json
from datetime import datetime

class DataLoader:
    def __init__(self):
        self.df = None
        self.events_df = None
        self.load_data()
    
    def convert_nan_to_none(self, value):
        """Convert NaN to None for JSON serialization"""
        if isinstance(value, float) and np.isnan(value):
            return None
        return value
    
    def find_file(self, filename):
        """Search for a file in multiple locations"""
        search_paths = [
            os.path.join('data', filename),
            os.path.join('../data', filename),
            filename,
            os.path.join('../', filename),
            os.path.join('../../data', filename),
        ]
        
        for path in search_paths:
            if os.path.exists(path):
                print(f"✓ Found file: {path}")
                return path
        
        print(f"✗ File not found: {filename}")
        return None
    
    def load_data(self):
        """Load all data files"""
        print("=" * 60)
        print("LOADING DATA")
        print("=" * 60)
        print(f"Current directory: {os.getcwd()}")
        
        # Load price data
        price_path = self.find_file('cleaned_brent_oil_prices.csv')
        if price_path:
            try:
                self.df = pd.read_csv(price_path)
                self.df['Date'] = pd.to_datetime(self.df['Date'])
                print(f"✓ Loaded price data: {len(self.df)} records")
                print(f"  Date range: {self.df['Date'].min()} to {self.df['Date'].max()}")
                print(f"  Price range: ${self.df['Price'].min():.2f} to ${self.df['Price'].max():.2f}")
                
                # Calculate returns if not present
                if 'Log_Returns' not in self.df.columns:
                    self.df['Log_Returns'] = np.log(self.df['Price'] / self.df['Price'].shift(1))
                    self.df['Returns'] = self.df['Price'].pct_change()
                    self.df['Volatility_30d'] = self.df['Returns'].rolling(window=30).std() * np.sqrt(252)
                    print("✓ Calculated returns and volatility")
            except Exception as e:
                print(f"✗ Error loading price data: {e}")
                self.df = None
        else:
            print("✗ Price data file not found!")
            self.df = None
        
        # Load events data
        event_path = self.find_file('key_events.csv')
        if event_path:
            try:
                self.events_df = pd.read_csv(event_path)
                self.events_df['Date'] = pd.to_datetime(self.events_df['Date'])
                print(f"✓ Loaded events data: {len(self.events_df)} records")
                print(f"  Date range: {self.events_df['Date'].min()} to {self.events_df['Date'].max()}")
                print(f"  Categories: {', '.join(self.events_df['Category'].unique())}")
            except Exception as e:
                print(f"✗ Error loading events data: {e}")
                self.events_df = None
        else:
            print("✗ Events data file not found!")
            self.events_df = None
        
        # Summary
        print("\n" + "=" * 60)
        print("LOADING SUMMARY")
        print("=" * 60)
        print(f"Price data: {'✓ Loaded' if self.df is not None else '✗ Not loaded'}")
        print(f"Events data: {'✓ Loaded' if self.events_df is not None else '✗ Not loaded'}")
        print("=" * 60)
        
        return self.df is not None
    
    def get_price_data(self, start_date=None, end_date=None):
        """Get price data with optional date filter - converts NaN to None"""
        if self.df is None:
            print("Warning: No price data available")
            return []
        
        df_filtered = self.df.copy()
        
        if start_date:
            try:
                df_filtered = df_filtered[df_filtered['Date'] >= pd.to_datetime(start_date)]
            except:
                pass
        if end_date:
            try:
                df_filtered = df_filtered[df_filtered['Date'] <= pd.to_datetime(end_date)]
            except:
                pass
        
        # Convert to records and handle NaN values
        records = df_filtered.to_dict('records')
        for record in records:
            # Convert NaN to None for JSON
            for key, value in record.items():
                if isinstance(value, float) and np.isnan(value):
                    record[key] = None
            # Format date
            if 'Date' in record:
                record['Date'] = record['Date'].isoformat()
        
        return records
    
    def get_events(self, category=None):
        """Get events with optional category filter"""
        if self.events_df is None:
            return []
        
        df_filtered = self.events_df.copy()
        
        if category and category != 'All':
            df_filtered = df_filtered[df_filtered['Category'] == category]
        
        records = df_filtered.to_dict('records')
        for record in records:
            if 'Date' in record:
                record['Date'] = record['Date'].isoformat()
        
        return records
    
    def get_categories(self):
        """Get all event categories"""
        if self.events_df is None:
            return []
        return self.events_df['Category'].unique().tolist()
    
    def get_statistics(self):
        """Get basic statistics"""
        if self.df is None:
            return {}
        
        return {
            'current_price': float(self.df['Price'].iloc[-1]) if len(self.df) > 0 else 0,
            'avg_price': float(self.df['Price'].mean()),
            'min_price': float(self.df['Price'].min()),
            'max_price': float(self.df['Price'].max()),
            'total_records': len(self.df),
            'date_min': self.df['Date'].min().isoformat(),
            'date_max': self.df['Date'].max().isoformat()
        }
    
    def get_event_impacts(self, window=10):
        """Calculate event impacts"""
        if self.df is None or self.events_df is None:
            return []
        
        impacts = []
        for _, event in self.events_df.iterrows():
            try:
                event_date = event['Date']
                idx = self.df[self.df['Date'] >= event_date].index
                
                if len(idx) > 0:
                    idx = idx[0]
                    before = self.df['Price'].iloc[max(0, idx-window):idx].mean()
                    after = self.df['Price'].iloc[idx:min(len(self.df), idx+window)].mean()
                    impact = float(after - before)
                    pct = float((impact / before) * 100) if before > 0 else 0
                    
                    impacts.append({
                        'event': str(event['Event']),
                        'date': event['Date'].isoformat(),
                        'category': str(event['Category']),
                        'impact': impact,
                        'percentage': pct,
                        'price_before': float(before),
                        'price_after': float(after)
                    })
            except Exception as e:
                print(f"Error calculating impact for {event['Event']}: {e}")
                continue
        
        return impacts
    
    def detect_change_point(self):
        """Find the biggest price change"""
        if self.df is None:
            return None
        
        try:
            prices = self.df['Price'].values
            changes = np.diff(prices)
            max_idx = np.argmax(np.abs(changes))
            
            return {
                'date': self.df['Date'].iloc[max_idx + 1].isoformat(),
                'price_before': float(prices[max_idx]),
                'price_after': float(prices[max_idx + 1]),
                'change': float(prices[max_idx + 1] - prices[max_idx]),
                'percentage': float(((prices[max_idx + 1] - prices[max_idx]) / prices[max_idx]) * 100)
            }
        except Exception as e:
            print(f"Error detecting change point: {e}")
            return None
"""
Data loading and preprocessing module for Brent Oil Price Analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Optional, Tuple, Dict, List
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BrentOilDataLoader:
    """
    Class to handle loading and preprocessing of Brent oil price data
    """
    
    def __init__(self, data_path: str):
        """
        Initialize the data loader with path to data
        
        Parameters:
        -----------
        data_path : str
            Path to the CSV file containing Brent oil price data
        
        Raises:
        -------
        ValueError: If data_path is empty or None
        """
        if not data_path:
            raise ValueError("data_path cannot be empty or None")
        
        self.data_path = data_path
        self.df = None
        logger.info(f"DataLoader initialized with path: {data_path}")
        
    def load_data(self) -> pd.DataFrame:
        """
        Load Brent oil price data from CSV with comprehensive error handling
        
        Returns:
        --------
        pd.DataFrame: Loaded dataframe with processed date column
        
        Raises:
        -------
        FileNotFoundError: If the CSV file does not exist
        ValueError: If the data is empty or missing required columns
        Exception: For any other unexpected errors
        """
        try:
            logger.info(f"Loading data from {self.data_path}")
            
            # Check if file exists
            if not os.path.exists(self.data_path):
                raise FileNotFoundError(f"Data file not found: {self.data_path}")
            
            # Load CSV
            try:
                self.df = pd.read_csv(self.data_path)
                logger.info(f"Successfully loaded CSV with {len(self.df)} rows")
            except pd.errors.EmptyDataError:
                raise ValueError(f"CSV file is empty: {self.data_path}")
            except pd.errors.ParserError as e:
                raise ValueError(f"Error parsing CSV file: {e}")
            
            # Check if dataframe is empty
            if self.df.empty:
                raise ValueError("Dataframe is empty after loading")
            
            # Check required columns
            required_columns = ['Date', 'Price']
            missing_columns = [col for col in required_columns if col not in self.df.columns]
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")
            
            # Convert Date column to datetime
            try:
                # Try the specific format first
                self.df['Date'] = pd.to_datetime(self.df['Date'], format='%d-%b-%y')
                logger.info("Date column parsed using format '%d-%b-%y'")
            except (ValueError, TypeError) as e:
                logger.warning(f"Failed to parse dates with '%d-%b-%y' format: {e}")
                try:
                    # Try alternative parsing
                    self.df['Date'] = pd.to_datetime(self.df['Date'], errors='coerce')
                    logger.info("Date column parsed using automatic format detection")
                except Exception as e2:
                    logger.error(f"Failed to parse dates: {e2}")
                    raise ValueError(f"Unable to parse Date column: {e2}")
            
            # Check for invalid dates
            invalid_dates = self.df['Date'].isna().sum()
            if invalid_dates > 0:
                logger.warning(f"Found {invalid_dates} invalid dates, removing them")
                self.df = self.df.dropna(subset=['Date'])
            
            # Sort by date
            self.df = self.df.sort_values('Date').reset_index(drop=True)
            logger.info(f"Data sorted by date, {len(self.df)} records remaining")
            
            # Ensure Price is numeric
            try:
                self.df['Price'] = pd.to_numeric(self.df['Price'], errors='coerce')
            except Exception as e:
                raise ValueError(f"Unable to convert Price to numeric: {e}")
            
            # Check for invalid prices
            invalid_prices = self.df['Price'].isna().sum()
            if invalid_prices > 0:
                logger.warning(f"Found {invalid_prices} invalid prices, removing them")
                self.df = self.df.dropna(subset=['Price'])
            
            # Check if we have any data left
            if self.df.empty:
                raise ValueError("No valid data remaining after cleaning")
            
            # Check for negative prices (invalid)
            negative_prices = (self.df['Price'] < 0).sum()
            if negative_prices > 0:
                logger.warning(f"Found {negative_prices} negative prices, removing them")
                self.df = self.df[self.df['Price'] >= 0]
            
            logger.info(f"Data loaded successfully. Shape: {self.df.shape}")
            logger.info(f"Date range: {self.df['Date'].min()} to {self.df['Date'].max()}")
            logger.info(f"Price range: ${self.df['Price'].min():.2f} to ${self.df['Price'].max():.2f}")
            
            return self.df
            
        except FileNotFoundError:
            logger.error(f"File not found: {self.data_path}")
            raise
        except ValueError as e:
            logger.error(f"Data validation error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error loading data: {e}")
            raise
    
    def calculate_returns(self) -> pd.DataFrame:
        """
        Calculate log returns from price data with error handling
        
        Returns:
        --------
        pd.DataFrame: Dataframe with added returns columns
        
        Raises:
        -------
        ValueError: If data is not loaded or no valid prices exist
        """
        try:
            if self.df is None:
                raise ValueError("Data not loaded. Call load_data() first.")
            
            if self.df.empty:
                raise ValueError("Dataframe is empty, cannot calculate returns")
            
            if 'Price' not in self.df.columns:
                raise ValueError("Price column not found in data")
            
            # Calculate log returns
            try:
                self.df['Log_Returns'] = np.log(self.df['Price'] / self.df['Price'].shift(1))
                logger.info("Log returns calculated successfully")
            except Exception as e:
                logger.error(f"Error calculating log returns: {e}")
                raise
            
            # Calculate simple returns
            try:
                self.df['Returns'] = self.df['Price'].pct_change()
                logger.info("Simple returns calculated successfully")
            except Exception as e:
                logger.error(f"Error calculating simple returns: {e}")
                raise
            
            # Calculate rolling volatility (30-day)
            try:
                self.df['Volatility_30d'] = self.df['Returns'].rolling(window=30).std() * np.sqrt(252)
                logger.info("Rolling volatility calculated successfully")
            except Exception as e:
                logger.error(f"Error calculating rolling volatility: {e}")
                raise
            
            logger.info("Returns and volatility calculated successfully")
            return self.df
            
        except ValueError as e:
            logger.error(f"Validation error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error calculating returns: {e}")
            raise
    
    def calculate_moving_averages(self, windows: List[int] = [50, 200]) -> pd.DataFrame:
        """
        Calculate moving averages for specified windows
        
        Parameters:
        -----------
        windows : List[int]
            List of window sizes for moving averages
            
        Returns:
        --------
        pd.DataFrame: Dataframe with added moving average columns
        """
        try:
            if self.df is None:
                raise ValueError("Data not loaded. Call load_data() first.")
            
            if self.df.empty:
                raise ValueError("Dataframe is empty")
            
            for window in windows:
                try:
                    col_name = f'MA_{window}'
                    self.df[col_name] = self.df['Price'].rolling(window=window).mean()
                    logger.info(f"Calculated {window}-day moving average")
                except Exception as e:
                    logger.error(f"Error calculating {window}-day MA: {e}")
                    raise
            
            return self.df
            
        except Exception as e:
            logger.error(f"Error calculating moving averages: {e}")
            raise
    
    def get_data_summary(self) -> Dict:
        """
        Get summary statistics of the data with error handling
        
        Returns:
        --------
        dict: Dictionary containing summary statistics
        """
        try:
            if self.df is None:
                raise ValueError("Data not loaded. Call load_data() first.")
            
            if self.df.empty:
                return {'error': 'Dataframe is empty'}
            
            summary = {
                'total_records': len(self.df),
                'min_price': float(self.df['Price'].min()),
                'max_price': float(self.df['Price'].max()),
                'mean_price': float(self.df['Price'].mean()),
                'std_price': float(self.df['Price'].std()),
                'start_date': self.df['Date'].min().isoformat(),
                'end_date': self.df['Date'].max().isoformat()
            }
            
            if 'Log_Returns' in self.df.columns:
                summary['mean_returns'] = float(self.df['Log_Returns'].mean())
                summary['std_returns'] = float(self.df['Log_Returns'].std())
            
            if 'Volatility_30d' in self.df.columns:
                summary['mean_volatility'] = float(self.df['Volatility_30d'].mean() * 100)
            
            return summary
            
        except Exception as e:
            logger.error(f"Error getting data summary: {e}")
            return {'error': str(e)}
    
    def validate_data(self) -> Tuple[bool, List[str]]:
        """
        Validate data quality and integrity
        
        Returns:
        --------
        Tuple[bool, List[str]]: (is_valid, list_of_issues)
        """
        issues = []
        
        try:
            if self.df is None:
                issues.append("Data not loaded")
                return False, issues
            
            if self.df.empty:
                issues.append("Dataframe is empty")
                return False, issues
            
            # Check for missing values
            missing = self.df.isnull().sum()
            if missing.sum() > 0:
                issues.append(f"Missing values found: {missing.to_dict()}")
            
            # Check for duplicates
            duplicates = self.df.duplicated(subset=['Date']).sum()
            if duplicates > 0:
                issues.append(f"Duplicate dates found: {duplicates}")
            
            # Check for negative prices
            negative = (self.df['Price'] < 0).sum()
            if negative > 0:
                issues.append(f"Negative prices found: {negative}")
            
            # Check for extreme outliers
            q1 = self.df['Price'].quantile(0.25)
            q3 = self.df['Price'].quantile(0.75)
            iqr = q3 - q1
            outliers = ((self.df['Price'] < q1 - 3 * iqr) | (self.df['Price'] > q3 + 3 * iqr)).sum()
            if outliers > 0:
                issues.append(f"Potential outliers found: {outliers}")
            
            is_valid = len(issues) == 0
            return is_valid, issues
            
        except Exception as e:
            issues.append(f"Validation error: {str(e)}")
            return False, issues


class EventDataLoader:
    """
    Class to handle loading and preprocessing of event data
    """
    
    def __init__(self, events_path: Optional[str] = None):
        """
        Initialize event data loader
        
        Parameters:
        -----------
        events_path : str, optional
            Path to CSV file containing event data
        """
        self.events_path = events_path
        self.events_df = None
        logger.info(f"EventDataLoader initialized with path: {events_path}")
    
    def load_events(self) -> pd.DataFrame:
        """
        Load events from CSV file with error handling
        
        Returns:
        --------
        pd.DataFrame: Loaded events data
        
        Raises:
        -------
        FileNotFoundError: If the CSV file does not exist
        ValueError: If data is invalid or empty
        """
        try:
            if not self.events_path:
                logger.warning("No events path provided, using default events")
                return self.create_events_data()
            
            if not os.path.exists(self.events_path):
                logger.warning(f"Events file not found: {self.events_path}, using default events")
                return self.create_events_data()
            
            try:
                self.events_df = pd.read_csv(self.events_path)
                logger.info(f"Loaded events from {self.events_path}: {len(self.events_df)} records")
            except Exception as e:
                logger.error(f"Error reading events file: {e}")
                return self.create_events_data()
            
            # Check required columns
            required = ['Date', 'Event']
            missing = [col for col in required if col not in self.events_df.columns]
            if missing:
                logger.warning(f"Missing columns: {missing}, using default events")
                return self.create_events_data()
            
            # Convert dates
            try:
                self.events_df['Date'] = pd.to_datetime(self.events_df['Date'])
            except Exception as e:
                logger.error(f"Error parsing event dates: {e}")
                return self.create_events_data()
            
            self.events_df = self.events_df.sort_values('Date').reset_index(drop=True)
            return self.events_df
            
        except Exception as e:
            logger.error(f"Unexpected error loading events: {e}")
            return self.create_events_data()
    
    def create_events_data(self) -> pd.DataFrame:
        """
        Create a structured dataset of key events affecting oil prices
        
        Returns:
        --------
        pd.DataFrame: DataFrame with event dates and descriptions
        """
        try:
            events_data = [
                # Geopolitical Events
                {'Date': '1990-08-02', 'Event': 'Iraq Invades Kuwait', 'Category': 'Conflict'},
                {'Date': '2003-03-20', 'Event': 'US Invasion of Iraq', 'Category': 'Conflict'},
                {'Date': '2011-02-15', 'Event': 'Arab Spring Begins', 'Category': 'Political Unrest'},
                {'Date': '2014-06-10', 'Event': 'ISIS Advances in Iraq', 'Category': 'Conflict'},
                {'Date': '2020-01-03', 'Event': 'US-Iran Tensions Escalate', 'Category': 'Geopolitical'},
                {'Date': '2022-02-24', 'Event': 'Russia-Ukraine War', 'Category': 'Conflict'},
                
                # OPEC Decisions
                {'Date': '1998-03-01', 'Event': 'OPEC Production Cuts', 'Category': 'OPEC Policy'},
                {'Date': '2008-09-10', 'Event': 'OPEC Cuts Production', 'Category': 'OPEC Policy'},
                {'Date': '2014-11-27', 'Event': 'OPEC Maintains Production', 'Category': 'OPEC Policy'},
                {'Date': '2016-11-30', 'Event': 'OPEC+ Production Cut Deal', 'Category': 'OPEC Policy'},
                {'Date': '2020-04-12', 'Event': 'Historic OPEC+ Deal', 'Category': 'OPEC Policy'},
                {'Date': '2021-07-18', 'Event': 'OPEC+ Production Increase', 'Category': 'OPEC Policy'},
                
                # Economic Events
                {'Date': '1997-07-02', 'Event': 'Asian Financial Crisis', 'Category': 'Economic Crisis'},
                {'Date': '2008-09-15', 'Event': 'Global Financial Crisis', 'Category': 'Economic Crisis'},
                {'Date': '2020-03-11', 'Event': 'COVID-19 Pandemic', 'Category': 'Health Crisis'},
                
                # International Sanctions
                {'Date': '2012-07-01', 'Event': 'EU Sanctions on Iran', 'Category': 'Sanctions'},
                {'Date': '2018-11-05', 'Event': 'US Sanctions on Iran', 'Category': 'Sanctions'},
                {'Date': '2019-04-22', 'Event': 'US Ends Iran Sanction Waivers', 'Category': 'Sanctions'},
                {'Date': '2022-03-08', 'Event': 'US Bans Russian Oil Imports', 'Category': 'Sanctions'}
            ]
            
            self.events_df = pd.DataFrame(events_data)
            self.events_df['Date'] = pd.to_datetime(self.events_df['Date'])
            self.events_df = self.events_df.sort_values('Date').reset_index(drop=True)
            
            logger.info(f"Created {len(self.events_df)} default events")
            return self.events_df
            
        except Exception as e:
            logger.error(f"Error creating events data: {e}")
            return pd.DataFrame()
    
    def get_events_by_category(self, category: str) -> pd.DataFrame:
        """
        Filter events by category
        
        Parameters:
        -----------
        category : str
            Category to filter by
            
        Returns:
        --------
        pd.DataFrame: Filtered events
        """
        try:
            if self.events_df is None or self.events_df.empty:
                return pd.DataFrame()
            
            if 'Category' not in self.events_df.columns:
                return self.events_df
            
            return self.events_df[self.events_df['Category'] == category]
            
        except Exception as e:
            logger.error(f"Error filtering events by category: {e}")
            return pd.DataFrame()
    
    def save_events(self, filepath: str) -> bool:
        """
        Save events data to CSV
        
        Parameters:
        -----------
        filepath : str
            Path where to save the events CSV
            
        Returns:
        --------
        bool: True if successful, False otherwise
        """
        try:
            if self.events_df is None or self.events_df.empty:
                logger.warning("No events data to save")
                return False
            
            self.events_df.to_csv(filepath, index=False)
            logger.info(f"Events data saved to {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving events data: {e}")
            return False
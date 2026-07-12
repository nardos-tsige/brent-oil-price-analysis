"""
Data loading and preprocessing module for Brent Oil Price Analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Optional, Tuple
import logging

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
        """
        self.data_path = data_path
        self.df = None
        
    def load_data(self) -> pd.DataFrame:
        """
        Load Brent oil price data from CSV
        
        Returns:
        --------
        pd.DataFrame: Loaded dataframe with processed date column
        """
        try:
            logger.info(f"Loading data from {self.data_path}")
            self.df = pd.read_csv(self.data_path)
            
            # Convert Date column to datetime
            # The date format is 'day-month-year' (e.g., '20-May-87')
            self.df['Date'] = pd.to_datetime(self.df['Date'], format='%d-%b-%y')
            
            # Sort by date
            self.df = self.df.sort_values('Date').reset_index(drop=True)
            
            # Ensure Price is numeric
            self.df['Price'] = pd.to_numeric(self.df['Price'], errors='coerce')
            
            # Remove any rows with missing values
            self.df = self.df.dropna()
            
            logger.info(f"Data loaded successfully. Shape: {self.df.shape}")
            logger.info(f"Date range: {self.df['Date'].min()} to {self.df['Date'].max()}")
            
            return self.df
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def calculate_returns(self) -> pd.DataFrame:
        """
        Calculate log returns from price data
        
        Returns:
        --------
        pd.DataFrame: Dataframe with added returns columns
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        # Calculate log returns
        self.df['Log_Returns'] = np.log(self.df['Price'] / self.df['Price'].shift(1))
        
        # Calculate simple returns
        self.df['Returns'] = self.df['Price'].pct_change()
        
        # Calculate rolling volatility (30-day)
        self.df['Volatility_30d'] = self.df['Returns'].rolling(window=30).std() * np.sqrt(252)
        
        logger.info("Returns and volatility calculated successfully")
        return self.df
    
    def get_data_summary(self) -> dict:
        """
        Get summary statistics of the data
        
        Returns:
        --------
        dict: Dictionary containing summary statistics
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        summary = {
            'total_days': len(self.df),
            'min_price': self.df['Price'].min(),
            'max_price': self.df['Price'].max(),
            'mean_price': self.df['Price'].mean(),
            'std_price': self.df['Price'].std(),
            'start_date': self.df['Date'].min(),
            'end_date': self.df['Date'].max()
        }
        
        if 'Log_Returns' in self.df.columns:
            summary['mean_returns'] = self.df['Log_Returns'].mean()
            summary['std_returns'] = self.df['Log_Returns'].std()
        
        return summary

class EventDataLoader:
    """
    Class to handle loading and preprocessing of event data
    """
    
    def __init__(self, events_path: str = None):
        """
        Initialize event data loader
        
        Parameters:
        -----------
        events_path : str, optional
            Path to CSV file containing event data
        """
        self.events_path = events_path
        self.events_df = None
        
    def create_events_data(self) -> pd.DataFrame:
        """
        Create a structured dataset of key events affecting oil prices
        
        Returns:
        --------
        pd.DataFrame: DataFrame with event dates and descriptions
        """
        events_data = [
            # Geopolitical Events
            {
                'Date': '1990-08-02',
                'Event': 'Iraq Invades Kuwait',
                'Category': 'Conflict',
                'Description': 'Start of Gulf War, Iraqi invasion of Kuwait leading to UN sanctions and military intervention'
            },
            {
                'Date': '2003-03-20',
                'Event': 'US Invasion of Iraq',
                'Category': 'Conflict',
                'Description': 'Second Gulf War begins with US-led invasion of Iraq'
            },
            {
                'Date': '2011-02-15',
                'Event': 'Arab Spring Begins',
                'Category': 'Political Unrest',
                'Description': 'Widespread protests across Middle East and North Africa, affecting oil-producing countries'
            },
            {
                'Date': '2014-06-10',
                'Event': 'ISIS Advances in Iraq',
                'Category': 'Conflict',
                'Description': 'ISIS captures Mosul and advances through Iraq, threatening oil infrastructure'
            },
            {
                'Date': '2020-01-03',
                'Event': 'US-Iran Tensions Escalate',
                'Category': 'Geopolitical',
                'Description': 'US drone strike kills Iranian General Soleimani, escalating tensions in the Gulf'
            },
            {
                'Date': '2022-02-24',
                'Event': 'Russia-Ukraine War',
                'Category': 'Conflict',
                'Description': 'Russia invades Ukraine, triggering massive supply disruption fears and sanctions'
            },
            
            # OPEC Decisions
            {
                'Date': '1998-03-01',
                'Event': 'OPEC Production Cuts',
                'Category': 'OPEC Policy',
                'Description': 'OPEC announces production cuts to address low oil prices'
            },
            {
                'Date': '2008-09-10',
                'Event': 'OPEC Cuts Production',
                'Category': 'OPEC Policy',
                'Description': 'OPEC cuts production by 520,000 barrels per day to stabilize prices'
            },
            {
                'Date': '2014-11-27',
                'Event': 'OPEC Maintains Production',
                'Category': 'OPEC Policy',
                'Description': 'OPEC decides to maintain production levels despite falling prices, leading to price collapse'
            },
            {
                'Date': '2016-11-30',
                'Event': 'OPEC+ Production Cut Deal',
                'Category': 'OPEC Policy',
                'Description': 'OPEC and non-OPEC producers agree to cut production by 1.2 million barrels per day'
            },
            {
                'Date': '2020-04-12',
                'Event': 'Historic OPEC+ Deal',
                'Category': 'OPEC Policy',
                'Description': 'OPEC+ agrees to historic 9.7 million barrel per day production cut'
            },
            {
                'Date': '2021-07-18',
                'Event': 'OPEC+ Production Increase',
                'Category': 'OPEC Policy',
                'Description': 'OPEC+ agrees to gradually increase production by 400,000 barrels per day'
            },
            
            # Economic Events
            {
                'Date': '1997-07-02',
                'Event': 'Asian Financial Crisis',
                'Category': 'Economic Crisis',
                'Description': 'Asian financial crisis begins, affecting global oil demand'
            },
            {
                'Date': '2008-09-15',
                'Event': 'Global Financial Crisis',
                'Category': 'Economic Crisis',
                'Description': 'Lehman Brothers collapses, triggering global financial crisis and oil demand destruction'
            },
            {
                'Date': '2020-03-11',
                'Event': 'COVID-19 Pandemic',
                'Category': 'Health Crisis',
                'Description': 'WHO declares COVID-19 a pandemic, leading to global lockdowns and oil demand collapse'
            },
            
            # International Sanctions
            {
                'Date': '2012-07-01',
                'Event': 'EU Sanctions on Iran',
                'Category': 'Sanctions',
                'Description': 'EU imposes oil embargo on Iran, removing 1.5 million barrels per day from the market'
            },
            {
                'Date': '2018-11-05',
                'Event': 'US Sanctions on Iran',
                'Category': 'Sanctions',
                'Description': 'US reinstates sanctions on Iran\'s oil exports after withdrawing from JCPOA'
            },
            {
                'Date': '2019-04-22',
                'Event': 'US Ends Iran Sanction Waivers',
                'Category': 'Sanctions',
                'Description': 'US ends waivers for countries importing Iranian oil, tightening global supply'
            },
            {
                'Date': '2022-03-08',
                'Event': 'US Bans Russian Oil Imports',
                'Category': 'Sanctions',
                'Description': 'US announces ban on Russian oil imports in response to Ukraine invasion'
            }
        ]
        
        self.events_df = pd.DataFrame(events_data)
        self.events_df['Date'] = pd.to_datetime(self.events_df['Date'])
        self.events_df = self.events_df.sort_values('Date').reset_index(drop=True)
        
        return self.events_df
    
    def save_events(self, filepath: str):
        """
        Save events data to CSV
        
        Parameters:
        -----------
        filepath : str
            Path where to save the events CSV
        """
        if self.events_df is None:
            self.create_events_data()
        self.events_df.to_csv(filepath, index=False)
        print(f"Events data saved to {filepath}")
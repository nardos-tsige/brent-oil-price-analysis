import pytest
import pandas as pd
import numpy as np
from src.data_loader import BrentOilDataLoader
import os

def test_load_data_success():
    """Test successful data loading"""
    # Create sample data
    test_file = 'test_data.csv'
    df = pd.DataFrame({
        'Date': ['20-May-87', '21-May-87'],
        'Price': [18.63, 18.45]
    })
    df.to_csv(test_file, index=False)
    
    loader = BrentOilDataLoader(test_file)
    result = loader.load_data()
    
    assert len(result) == 2
    assert 'Date' in result.columns
    assert 'Price' in result.columns
    
    os.remove(test_file)

def test_load_data_file_not_found():
    """Test file not found error"""
    loader = BrentOilDataLoader('nonexistent.csv')
    with pytest.raises(FileNotFoundError):
        loader.load_data()

def test_calculate_returns():
    """Test returns calculation"""
    loader = BrentOilDataLoader('test_data.csv')
    df = pd.DataFrame({
        'Date': pd.to_datetime(['2020-01-01', '2020-01-02']),
        'Price': [100, 110]
    })
    loader.df = df
    result = loader.calculate_returns()
    
    assert 'Log_Returns' in result.columns
    assert 'Returns' in result.columns
    assert 'Volatility_30d' in result.columns
import pytest
import pandas as pd
import sdmx

from gingado.utils import codelists

def test_codelists_single_dataflow():
    """Test codelists function with a single dataflow"""
    test_dflow = {"ECB": "EXR"}  # Exchange rates dataflow from ECB
    result = codelists(test_dflow)
    
    assert isinstance(result, dict)
    assert "ECB" in result
    assert isinstance(result["ECB"], pd.DataFrame)

@pytest.mark.skip(reason="Test temporarily disabled")
def test_codelists_multiple_dataflows():
    """Test codelists function with multiple dataflows"""
    test_dflow = {"ECB": ["EXR", "ICP"]}  # Exchange rates and consumer prices
    result = codelists(test_dflow)
    
    assert isinstance(result, dict)
    assert "ECB" in result
    assert isinstance(result["ECB"], dict)
    assert "EXR" in result["ECB"]
    assert "ICP" in result["ECB"]
    assert all(isinstance(df, pd.DataFrame) for df in result["ECB"].values())

@pytest.mark.skip(reason="Test temporarily disabled")
def test_codelists_multiple_sources():
    """Test codelists function with multiple sources"""
    test_dflow = {
        "ECB": "EXR",
        "OECD": "MEI"
    }
    result = codelists(test_dflow)
    
    assert isinstance(result, dict)
    assert "ECB" in result
    assert "OECD" in result
    assert all(isinstance(df, pd.DataFrame) for df in result.values())

@pytest.mark.skip(reason="Test temporarily disabled")
def test_codelists_invalid_source():
    """Test codelists function with invalid source"""
    test_dflow = {"INVALID_SOURCE": "EXR"}
    
    with pytest.raises(Exception):
        codelists(test_dflow)

@pytest.mark.skip(reason="Test temporarily disabled")
def test_codelists_invalid_dataflow():
    """Test codelists function with invalid dataflow"""
    test_dflow = {"ECB": "INVALID_DATAFLOW"}
    
    with pytest.raises(Exception):
        codelists(test_dflow)

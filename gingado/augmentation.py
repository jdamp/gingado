# AUTOGENERATED! DO NOT EDIT! File to edit: 00_augmentation.ipynb (unless otherwise specified).

__all__ = ['augm_with_sdmx']

# Cell
from simpledmx import *

# Cell
import pandas as pd

def augm_with_sdmx(df, start_date, end_date, time_col, freq, sources=None):
    """Downloads relevant data from SDMX sources to complement the original dataset

    Arguments:
      df: a pandas DataFrame
      start_date, end_date: the dates limiting the time period of the desired data from SDMX sources
      time_col: the name of the column in the original dataset that corresponds to time
      freq: the frequency of the desired data from SDMX; for example, 'A' is annual
      sources: the list of SDMX sources or None; a list of possible sources can be obtained by running the function list_sdmx_sources()
    """
    if start_date is None:
        start_date = df[time_col].min()
    if end_date is None:
        end_date=df[time_col].max()

    sdmx_data = get_sdmx_data(
        start_date=start_date,
        end_date=end_date,
        freq=freq,
        sources=sources
        )
    sdmx_data = sdmx_data.dropna(axis=1).sort_index()
    sdmx_data.reset_index(inplace=True)
    sdmx_data['TIME_PERIOD'] = pd.to_datetime(sdmx_data['TIME_PERIOD'])
    if df is None:
        return sdmx_data
    df = df.merge(sdmx_data, how='left', left_on=time_col, right_on='TIME_PERIOD')
    return df
# AUTOGENERATED! DO NOT EDIT! File to edit: 00_utils.ipynb (unless otherwise specified).

__all__ = ['get_username', 'get_datetime', 'Lag', 'list_SDMX_sources', 'list_all_dataflows', 'load_SDMX_data',
           'load_EURFX_data']

# Cell
#export
import datetime
import os
import pwd

# Cell
#export
def get_username():
    "Returns the active username in the computer"
    return pwd.getpwuid(os.getuid()).pw_name

# Cell
#export
def get_datetime():
    "Returns the time now"
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z")

# Cell
#export
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_is_fitted

class Lag(BaseEstimator, TransformerMixin):
    def __init__(self, lags=1, jump=0, keep_contemporaneous_X=False):
        self.lags = lags
        self.jump = jump
        self.keep_contemporaneous_X = keep_contemporaneous_X

    def fit(self, X, y=None):
        self.index = None
        if hasattr(X, "index"):
            self.index = X.index
        else:
            if y is not None and hasattr(y, "index"):
                self.index = y.index
        X = self._validate_data(X)

        self.effective_lags_ = self.lags + self.jump
        return self

    def transform(self, X):
        X_forlag = X

        X = self._validate_data(X)
        check_is_fitted(self)
        X_lags = []
        X_colnames = list(self.feature_names_in_) if self.keep_contemporaneous_X else []
        for lag in range(self.effective_lags_):
            if lag < self.jump:
                continue
            lag_count = lag+1
            lag_X = np.roll(X_forlag, lag_count, axis=0)
            X_lags.append(lag_X)
            if hasattr(self, "feature_names_in_"):
                X_colnames = X_colnames + [col+"_lag_"+str(lag+1) for col in list(self.feature_names_in_)]
        X = np.concatenate(X_lags, axis=1)
        if self.keep_contemporaneous_X:
            X = np.concatenate([X_forlag, X], axis=1)
        X = X[self.effective_lags_:, :]
        if hasattr(self, "index") and self.index is not None:
            new_index = self.index[self.effective_lags_:]
            X = pd.DataFrame(X, index=new_index, columns=X_colnames)
        else:
            X = pd.DataFrame(X)
        return X

# Cell
#export
import pandasdmx as sdmx

def list_SDMX_sources():
    "Returns the list of codes representing the SDMX sources available for data download"
    return sdmx.list_sources()

# Cell
#export
import pandasdmx as sdmx

def list_all_dataflows(codes_only=False):
    "Returns a dictionary listing all available dataflows for all sources. When using as a parameter to an `AugmentSDMX` object or to the `load_SDMX_data` function, set `codes_only=True`"
    sources = sdmx.list_sources()
    dflows = {}
    for src in sources:
        try:
            dflows[src] = sdmx.to_pandas(sdmx.Request(src).dataflow().dataflow)
            dflows[src] = dflows[src].index if codes_only else dflows[src].index.reset_index()
        except:
            pass
    return dflows

# Cell
#export
def load_SDMX_data(sources, keys, params, verbose=True):
    "Loads datasets from SDMX."
    data_sdmx = {}
    for source in sources.keys():
        src_conn = sdmx.Request(source)
        src_dflows = src_conn.dataflow()
        if sources[source] == 'all':
            dflows = {k: v for k, v in src_dflows.dataflow.items()}
        else:
            dflows = {k: v for k, v in src_dflows.dataflow.items() if k in sources[source]}
        for dflow in dflows.keys():
            if verbose: print(f"Querying data from {source}'s dataflow '{dflow}' - {dflows[dflow].dict()['name']}...")
            try:
                data = sdmx.to_pandas(src_conn.data(dflow, key=keys, params=params), datetime='TIME_PERIOD')
            except:
                if verbose: print("this dataflow does not have data in the desired frequency and time period.")
                continue
            data.columns = ['__'.join(col) for col in data.columns.to_flat_index()]
            data_sdmx[source+"__"+dflow] = data

    if len(data_sdmx.keys()) is None:
        return

    df = pd.concat(data_sdmx, axis=1)
    df.columns = ['_'.join(col) for col in df.columns.to_flat_index()]
    return df

# Cell
#export
import pandasdmx as sdmx
import warnings

def load_EURFX_data(startYear=2003, lags=1, jump=0, keep_contemporaneous_X=True):
    "Loads a real-life dataset for testing use cases."
    warnings.warn(message="Function 'load_EURFX_data' will no longer be present after gingado v0.0.2. Use 'load_SDMX_data(source={'ECB': 'EXR'}) instead.", category=DeprecationWarning, stacklevel=2)
    ecb = sdmx.Request('ECB')
    exr_msg = ecb.dataflow('EXR')
    exr_flow = exr_msg.dataflow.EXR
    dsd = exr_flow.structure
    key = {
    "CURRENCY": ['EUR', 'AUD', 'BRL', 'CAD', 'CHF', 'GBP', 'JPY', 'SGD', 'USD'],
    "FREQ": 'D'
    }
    params = {"startPeriod": startYear}
    data_msg = ecb.data('EXR', key=key, params=params, dsd=dsd)
    df = sdmx.to_pandas(data_msg.data[0], datetime='TIME_PERIOD')
    df = df.droplevel(['FREQ', 'CURRENCY_DENOM', 'EXR_TYPE', 'EXR_SUFFIX'], axis=1).dropna(how='all')

    if lags or jump:
        df = Lag(lags=lags, jump=jump, keep_contemporaneous_X=keep_contemporaneous_X).fit_transform(df)
    return df
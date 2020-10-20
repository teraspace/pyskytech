import pandas as pd
import numpy as np

from histdata import download_hist_data as dl
from histdata.api import Platform as P, TimeFrame as TF

dl(year='2019', month=None, pair='eurusd', platform=P.META_TRADER, time_frame=TF.TICK_DATA)


data_frame = pd.read_csv('DAT_ASCII_EURUSD_T_201906.csv', names=['Symbol', 'Date_Time', 'Bid', 'Ask'],

index_col=1, parse_dates=True)


data_frame
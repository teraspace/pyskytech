import pandas as pd
import numpy as np

from histdata import download_hist_data as dl
from histdata.api import Platform as P, TimeFrame as TF

dl(year='2019', month='6', pair='eurusd', platform=P.GENERIC_ASCII, time_frame=TF.TICK_DATA)



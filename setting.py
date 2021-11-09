import os
from datetime import datetime
import numpy as np
import pandas as pd

PWD = os.getcwd()
TODAY = ''.join(str(datetime.today())[:10].split('-'))

DIR_KOSPI_DAILY = PWD + '\\data\\kospi_daily'
DIR_KOSDAQ_DAILY = PWD + '\\data\\kosdaq_daily'
DIR_KOSPI_MINUTELY = PWD + '\\data\\kospi_minutely'
DIR_KOSDAQ_MINUTELY = PWD + '\\data\\kosdaq_minutely'

CSV_DAILY_CHECKLIST = PWD + '\\data\\daily_checklist.csv'
CSV_LASTEST_CHECKLIST = PWD + f'\\data\\past_check\\daily_checklist_{TODAY}.csv'

CHECKLIST_DTYPE ={

}

TRADEDATA_DTYPE = {
    '종목코드' : 'category',
    '종목명' : 'category',
    '시가' : np.uint32,
    '고가' : np.uint32,
    '저가' : np.uint32,
    '종가' : np.uint32,
    '거래량' : np.uint32
}
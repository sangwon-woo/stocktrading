import os
from datetime import datetime
import numpy as np
import pandas as pd

PWD = os.getcwd()
TODAY = datetime.today().date().strftime('%Y%m%d')

DIR_KOSPI_DAILY = PWD + '\\data\\kospi_daily'
DIR_KOSDAQ_DAILY = PWD + '\\data\\kosdaq_daily'
DIR_KOSPI_MINUTELY = PWD + '\\data\\kospi_minutely'
DIR_KOSDAQ_MINUTELY = PWD + '\\data\\kosdaq_minutely'

CSV_DAILY_CHECKLIST = PWD + '\\data\\daily_checklist.csv'
CSV_LASTEST_CHECKLIST = PWD + f'\\data\\past_check\\daily_checklist_{TODAY}.csv'

CHECKLIST_DTYPE ={
    '시장명' : 'category',
    '종목명' : 'category',
    '종목코드' : 'category',
    '감리구분' : 'category',
    '체크최종수정일' : 'category',
    '일봉관리여부' : bool,
    '일봉최종수정일' : 'category',
    '일봉최초일' : 'category',
    '일봉최말일' : 'category',
    '분봉관리여부' : bool,
    '분봉최종수정일' : 'category'
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
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

CSV_TODAY_CHECKLIST = PWD + f'\\data\\past_checklist\\daily_checklist_{TODAY}.csv'
csv_lastest_checklist = sorted(os.listdir(PWD + '\\data\\past_checklist'))[-1]
CSV_LASTEST_CHECKLIST = PWD + f'\\data\\past_checklist\\{csv_lastest_checklist}'
CSV_TODAY_TREND_ANALYSIS = PWD + f'\\data\\trend_analysis\\trend_analysis_{TODAY}.csv'


CHECKLIST_DTYPE ={
    '시장명' : 'category',
    '종목명' : 'category',
    '종목코드' : 'category',
    '감리구분' : 'category',
    '체크최종수정일' : 'category',
    '일봉관리여부' : bool,
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

STOCK_ITEM_DTYPE = {
    '현재가' : '종가',
    '일자' : '날짜'
}

TIMESPAN = {
    '1개주' : 5,
    '2개주' : 10,
    '3개주' : 15,
    '1개월' : 20,
    '2개월' : 40,
    '3개월' : 60,
    '6개월' : 120,
    '1개년' : 240
}

API_COUNT = 0

kospi_code_list_we_have = [i[:-4] for i in os.listdir(DIR_KOSPI_DAILY) if i.endswith('.csv')]
kosdaq_code_list_we_have = [i[:-4] for i in os.listdir(DIR_KOSDAQ_DAILY) if i.endswith('.csv')]
total_code_list_we_have = kospi_code_list_we_have + kosdaq_code_list_we_have
kospi_cnt_we_have = len(kospi_code_list_we_have)
kosdaq_cnt_we_have = len(kosdaq_code_list_we_have)
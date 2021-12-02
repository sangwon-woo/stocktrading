import os
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import configparser

config = configparser.ConfigParser()
config.read('config/config.ini', encoding='utf-8')
USER_ID = config.get('KIWOOM', 'USER_ID')
USER_NAME = config.get('KIWOOM', 'USER_NAME')
REAL_ACCOUNT = config.get('KIWOOM', 'REAL_ACCOUNT')
SIMULATED_ACCOUNT = config.get('KIWOOM', 'SIMULATED_ACCOUNT')
PASSWORD = config.get('KIWOOM', 'PASSWORD')

def get_today(today):
    today_weekday = today.weekday()
    today_hour = today.hour

    if today_weekday == 5:
        return (today - timedelta(days=1)).date().strftime("%Y%m%d")
    elif today_weekday == 6:
        return (today - timedelta(days=2)).date().strftime("%Y%m%d")

    if today_hour >= 16 and today_hour < 24:
        return today.date().strftime('%Y%m%d')
    else:
        return (today - timedelta(days=1)).date().strftime("%Y%m%d")


PWD = os.getcwd()
TODAY = get_today(datetime.today())


DIR_KOSPI_DAILY = PWD + '\\data\\kospi_daily'
DIR_KOSDAQ_DAILY = PWD + '\\data\\kosdaq_daily'
DIR_KOSPI_MINUTELY = PWD + '\\data\\kospi_minutely'
DIR_KOSDAQ_MINUTELY = PWD + '\\data\\kosdaq_minutely'

CSV_TODAY_CHECKLIST = PWD + f'\\data\\past_checklist\\daily_checklist_{TODAY}.csv'
csv_lastest_checklist = sorted(os.listdir(PWD + '\\data\\past_checklist'))[-1]
CSV_LASTEST_CHECKLIST = PWD + f'\\data\\past_checklist\\{csv_lastest_checklist}'

CSV_KOSPI_TREND_ANALYSIS = PWD + f'\\data\\trend_analysis\\kospi_trend_analysis_{TODAY}.csv'
CSV_KOSDAQ_TREND_ANALYSIS = PWD + f'\\data\\trend_analysis\\kosdaq_trend_analysis_{TODAY}.csv'

ARR_KOSPI_TOTAL_DATA = PWD + f'\\data\\total_kospi_data_{TODAY}.arrx'
ARR_KOSDAQ_TOTAL_DATA = PWD + f'\\data\\total_kosdaq_data_{TODAY}.arrx'

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

kospi_code_list_we_have = [i[:-4] for i in os.listdir(DIR_KOSPI_DAILY) if i.endswith('.csv')]
kosdaq_code_list_we_have = [i[:-4] for i in os.listdir(DIR_KOSDAQ_DAILY) if i.endswith('.csv')]
total_code_list_we_have = kospi_code_list_we_have + kosdaq_code_list_we_have
kospi_cnt_we_have = len(kospi_code_list_we_have)
kosdaq_cnt_we_have = len(kosdaq_code_list_we_have)


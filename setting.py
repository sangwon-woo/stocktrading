import os
from datetime import datetime

PWD = os.getcwd()
TODAY = str(datetime.today())[:10]

DIR_KOSPI_DAILY = PWD + '\\data\\kospi_daily'
DIR_KOSDAQ_DAILY = PWD + '\\data\\kosdaq_daily'
DIR_KOSPI_MINUTELY = PWD + '\\data\\kospi_minutely'
DIR_KOSDAQ_MINUTELY = PWD + '\\data\\kosdaq_minutely'

CSV_DAILY_CHECKLIST = PWD + '\\data\\daily_checklist.csv'
CSV_LASTEST_CHECKLIST = PWD + f'\\data\\past_check\\daily_checklist_{TODAY}.csv'

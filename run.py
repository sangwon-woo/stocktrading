import argparse
import os
import time

from collector.update_checklist import *
from collector.update_daily_data import CollectDailyData
from pykiwoom.kiwoom import Kiwoom
from config.api_count import API_COUNT as api


def login_success(kiwoom):
    state = kiwoom.GetConnectState()
    if state == 0:
        print("미연결")
    elif state == 1:
        print("연결완료")

def init_kiwoom():
    kiwoom = Kiwoom()
    kiwoom.CommConnect(block=True)
    login_success(kiwoom)

    return kiwoom


parser = argparse.ArgumentParser()
parser.add_argument('--update-checklist', '-c', type=bool, default=False, help='run update_checklist.py')
parser.add_argument('--update-daily-data', '-d', type=bool, default=False, help='run update_daily_data.py')
parser.add_argument('--trend-analysis', '-t', type=bool, default=False, help='run trend_analysis.py')

args = parser.parse_args()

update_checklist_flag = args.update_checklist
update_daily_data_flag = args.update_daily_data
trend_analysis_flag = args.trend_analysis

if update_checklist_flag:

    kiwoom = init_kiwoom()
    checklist = CheckList(kiwoom)
    checklist.update_checklist()
    del kiwoom
    

if update_daily_data_flag:
    lastest_checklist = pd.read_csv(CSV_LASTEST_CHECKLIST, encoding='utf-8', dtype=CHECKLIST_DTYPE)
    today_candidates = lastest_checklist[lastest_checklist['일봉최종수정일'] != int(TODAY)]
    today_candidates = today_candidates[['시장명', '종목명', '종목코드']]
    kospi_not_yet = list(today_candidates[today_candidates['시장명'] == 'kospi']['종목코드'].values)
    kosdaq_not_yet = list(today_candidates[today_candidates['시장명'] == 'kosdaq']['종목코드'].values)
    kospi_cnt_not_yet = len(kospi_not_yet)
    kosdaq_cnt_not_yet = len(kosdaq_not_yet)

    kiwoom = init_kiwoom()
    collect_daily_data = CollectDailyData(kiwoom)
    collect_daily_data.iter_daily_data()
    del kiwoom
    
if trend_analysis_flag:
    start = time.time()
    os.system('C:\\Users\\pacific\\miniconda3\\envs\\py39_64bits\\python.exe -c "import technical_analysis.trend_analysis as t; t.run_trend_analysis()"')
    end = time.time()
    print(f'총 걸린 시간 : {(end-start) / 60:.2f}분')
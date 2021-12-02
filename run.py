import argparse
import os
import time

from collector.update_checklist import *
from collector.update_daily_data import CollectDailyData
from pykiwoom.kiwoom import Kiwoom
from config.setting import *

API_COUNT = 0

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
    checklist = CheckList(kiwoom, API_COUNT)
    API_COUNT = checklist.update_checklist()

    del kiwoom

    print(f'checklist 업데이트 완료 및 API COUNT: {API_COUNT}')
    

if update_daily_data_flag:
    kospi_flag = False
    kosdaq_flag = False

    while True:
        while True:
            lastest_checklist = pd.read_csv(CSV_LASTEST_CHECKLIST, encoding='utf-8', dtype=CHECKLIST_DTYPE)
            today_candidates = lastest_checklist[lastest_checklist['일봉최종수정일'] != int(TODAY)]
            today_candidates = today_candidates[['시장명', '종목명', '종목코드']]
            kospi_not_yet = list(today_candidates[today_candidates['시장명'] == 'kospi']['종목코드'].values)
            kosdaq_not_yet = list(today_candidates[today_candidates['시장명'] == 'kosdaq']['종목코드'].values)
            kospi_cnt_not_yet = len(kospi_not_yet)
            kosdaq_cnt_not_yet = len(kosdaq_not_yet)

            today_checklist = pd.read_csv(CSV_TODAY_CHECKLIST, encoding='utf-8', dtype=CHECKLIST_DTYPE)
            today_checklist['일봉최근날짜'] = today_checklist['일봉최근날짜'].astype('object')
            
            kiwoom = init_kiwoom()

            kospi_code_list_until_now = kiwoom.GetCodeListByMarket('0')
            kosdaq_code_list_until_now = kiwoom.GetCodeListByMarket('10')

            collect_daily_data = CollectDailyData(kiwoom,
                                                API_COUNT,
                                                kospi_not_yet,
                                                kosdaq_not_yet,
                                                kospi_cnt_not_yet,
                                                kosdaq_cnt_not_yet)


            ret, today_checklist = collect_daily_data.iter_kospi(today_checklist, kospi_code_list_until_now)
            today_checklist.to_csv(CSV_TODAY_CHECKLIST, encoding='utf-8', index=None)

            if ret == 'api_limit':
                print('API LIMIT!')
                API_COUNT = 0
                del kiwoom
                break
            elif ret == 'kospi_complete':
                print('코스피 목록 완료')
                kospi_flag = True


            ret, today_checklist = collect_daily_data.iter_kosdaq(today_checklist, kosdaq_code_list_until_now)
            today_checklist.to_csv(CSV_TODAY_CHECKLIST, encoding='utf-8', index=None)

            if ret == 'api_limit':
                print('API LIMIT!')
                API_COUNT = 0
                del kiwoom
                break
            elif ret == 'kosdaq_complete':
                print('코스닥 목록 완료')   
                kosdaq_flag == True
        
        if kospi_flag and kosdaq_flag:
            break




if trend_analysis_flag:
    start = time.time()
    os.system('C:\\Users\\pacific\\miniconda3\\envs\\py39_64bits\\python.exe -c "import technical_analysis.trend_analysis as t; t.run_trend_analysis()"')
    end = time.time()
    print(f'총 걸린 시간 : {(end-start) / 60:.2f}분')
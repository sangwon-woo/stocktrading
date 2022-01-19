import argparse
import os
import time
import multiprocessing as mp

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

def set_checklist(API_COUNT):
    kiwoom = init_kiwoom()
    checklist = CheckList(kiwoom, API_COUNT)
    API_COUNT = checklist.update_checklist()

    print(mp.Process.__name__, '=>', end=' ')
    print(f'checklist 업데이트 완료 및 API COUNT: {API_COUNT}')

def update_daily_data(API_COUNT):
    lastest_checklist = pd.read_csv(CSV_LASTEST_CHECKLIST, encoding='utf-8', dtype=CHECKLIST_DTYPE)
    today_candidates = lastest_checklist[lastest_checklist['일봉최종수정일'] != int(TODAY)]
    today_candidates = today_candidates[['시장명', '종목명', '종목코드']]
    kospi_not_yet = list(today_candidates[today_candidates['시장명'] == 'kospi']['종목코드'].values)
    kosdaq_not_yet = list(today_candidates[today_candidates['시장명'] == 'kosdaq']['종목코드'].values)
    kospi_cnt_not_yet = len(kospi_not_yet)
    kosdaq_cnt_not_yet = len(kosdaq_not_yet)

    today_checklist = pd.read_csv(CSV_TODAY_CHECKLIST, encoding='utf-8', dtype=CHECKLIST_DTYPE)
    today_checklist['일봉최근날짜'] = today_checklist['일봉최근날짜'].astype('object')

    print(f'남은 코스피 종목 갯수: {kospi_cnt_not_yet}')
    print(f'남은 코스닥 종목 갯수: {kosdaq_cnt_not_yet}')

    kiwoom = init_kiwoom()


    collect_daily_data = CollectDailyData(kiwoom,
                                        API_COUNT,
                                        kospi_not_yet,
                                        kosdaq_not_yet,
                                        kospi_cnt_not_yet,
                                        kosdaq_cnt_not_yet)

    kospi_code_list_until_now = collect_daily_data.kiwoom.GetCodeListByMarket('0')
    kosdaq_code_list_until_now = collect_daily_data.kiwoom.GetCodeListByMarket('10')

    ret, today_checklist = collect_daily_data.iter_kospi(today_checklist, kospi_code_list_until_now)
    today_checklist.to_csv(CSV_TODAY_CHECKLIST, encoding='utf-8', index=None)

    if ret == 'api_limit':
        print('API LIMIT!')
        return
        
    elif ret == 'kospi_complete':
        print('코스피 목록 완료')


    ret, today_checklist = collect_daily_data.iter_kosdaq(today_checklist, kosdaq_code_list_until_now)
    today_checklist.to_csv(CSV_TODAY_CHECKLIST, encoding='utf-8', index=None)

    if ret == 'api_limit':
        print('API LIMIT!')
        return

    elif ret == 'kosdaq_complete':
        print('코스닥 목록 완료')   

if __name__ == '__main__':
    s = time.time()
    if update_checklist_flag:
        proc = mp.Process(target=set_checklist, args=(API_COUNT,), name='UPDATE_CHECKLIST')
        proc.start()
        proc.join()

    if update_daily_data_flag:
        kospi_flag = False
        kosdaq_flag = False

        for iter_count in range(4):
            API_COUNT = 0
            proc = mp.Process(target=update_daily_data, args=(API_COUNT,), name='UPDATE_DAILY_DATA')
            proc.start()
            proc.join()




    if trend_analysis_flag:
        start = time.time()
        os.system('C:\\Users\\pacific\\miniconda3\\envs\\pandas\\python.exe -m technical_analysis.trend_analysis')
        end = time.time()
        print(f'총 걸린 시간 : {(end-start) / 60:.2f}분') 
    e = time.time()
    print(e-s)
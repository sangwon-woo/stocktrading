import argparse
import os
from collector.update_checklist import *
from collector.update_daily_data import CollectDailyData
from pykiwoom.kiwoom import Kiwoom



def login_success(kiwoom):
    state = kiwoom.GetConnectState()
    if state == 0:
        print("미연결")
    elif state == 1:
        print("연결완료")



parser = argparse.ArgumentParser()
parser.add_argument('--update-checklist', '-c', type=bool, default=False, help='run update_checklist.py')
parser.add_argument('--update-daily-data', '-d', type=bool, default=False, help='run update_daily_data.py')
parser.add_argument('--trend-analysis', '-t', type=bool, default=False, help='run trend_analysis.py')

args = parser.parse_args()

update_checklist_flag = args.update_checklist
update_daily_data_flag = args.update_daily_data
trend_analysis_flag = args.trend_analysis

if trend_analysis_flag:
    os.system('C:\\Users\\pacific\\miniconda3\\envs\\py39_64bits\\python.exe technical_analysis\\trend_analysis.py')

def init_kiwoom():
    kiwoom = Kiwoom()
    kiwoom.CommConnect(block=True)
    login_success(kiwoom)

if update_checklist_flag:
    init_kiwoom()
    checklist = CheckList(kiwoom)
    checklist.update_checklist()

if update_daily_data_flag:
    init_kiwoom()
    collect_daily_data = CollectDailyData(kiwoom)
    collect_daily_data.iter_daily_data()
    
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('--update-checklist', '-c', type=bool, default=False, help='run update_checklist.py')
parser.add_argument('--update-daily-data', '-d', type=bool, default=False, help='run update_daily_data.py')
parser.add_argument('--trend-analysis', '-t', type=bool, default=False, help='run trend_analysis.py')

args = parser.parse_args()

update_checklist_flag = args.update_checklist
update_daily_data_flag = args.update_daily_data
trend_analysis_flag = args.trend_analysis

if update_checklist_flag:
    os.system('C:\\Users\\pacific\\miniconda3\\envs\\py32bits\\python.exe update_checklist.py')

if update_daily_data_flag:
    os.system('C:\\Users\\pacific\\miniconda3\\envs\\py32bits\\python.exe update_daily_data.py')

if trend_analysis_flag:
    os.system('C:\\Users\\pacific\\miniconda3\\envs\\py39_64bits\\python.exe trend_analysis.py')
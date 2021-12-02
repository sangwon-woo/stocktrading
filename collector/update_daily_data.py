import time
import pandas as pd
from pykiwoom.kiwoom import *
from config.setting import *
from config.api_count import API_COUNT as api
from datetime import datetime
import shutil

def get_stock_trade_data_until_now(kiwoom, code, name, today, STOCK_ITEM_DTYPE, TRADEDATA_DTYPE, next=0):
    
    recent_df = kiwoom.block_request('opt10081', 
                                    종목코드=code, 
                                    기준일자=today, 
                                    수정주가구분=1, 
                                    output='주식일봉차트조회',
                                    next=next)

    if recent_df.sum().sum() == code:
        return None

    recent_df = recent_df.rename(columns=STOCK_ITEM_DTYPE)
    recent_df['날짜'] = pd.to_datetime(recent_df['날짜'])
    recent_df['종목코드'] = code
    recent_df = recent_df[recent_df.columns[:8]]
    recent_df = recent_df[['종목코드', '날짜', '시가', '고가', '저가', '종가', '거래량']]
    recent_df.insert(1, '종목명', name)
    recent_df = recent_df.astype(TRADEDATA_DTYPE)
    
    return recent_df
class CollectDailyData:
    def __init__(self,
                kiwoom,
                API_COUNT,
                kospi_not_yet,
                kosdaq_not_yet,
                kospi_cnt_not_yet,
                kosdaq_cnt_not_yet):

        self.kiwoom = kiwoom
        self.api_count = API_COUNT
        self.kospi_not_yet = kospi_not_yet
        self.kosdaq_not_yet = kosdaq_not_yet
        self.kospi_cnt_not_yet = kospi_cnt_not_yet
        self.kosdaq_cnt_not_yet = kosdaq_cnt_not_yet


    def check_df(self, old, new):
        old_rows = old.shape[0]
        new_rows = new.shape[0]
        old_max = old['날짜'].max()
        old_min = old['날짜'].min()
        new_max = new['날짜'].max()
        new_min = new['날짜'].min()

        if new_rows > old_rows:
            if (new[ (new['날짜'] >= old_min ) & (new['날짜'] < old_max) ]
                .reset_index(drop=True)
                .equals(old[ old['날짜'] < old_max]
                        .reset_index(drop=True))
                ):

                return False

        elif new_rows == old_rows:
            if (new[(new['날짜'] > old_min ) & (new['날짜'] < old_max)]
                .reset_index(drop=True)
                .equals(old[(old['날짜'] > old_min) & (old['날짜'] < old_max)]
                        .reset_index(drop=True))
                ):

                return False

        else:
            if (new[new['날짜'] < old_max]
                .reset_index(drop=True)
                .equals(old[ (old['날짜'] >= new_min) & (old['날짜'] < old_max)]
                        .reset_index(drop=True))
                ):

                return False
                
        return True

    def move_stock_data_to_delisting(self, code, file_dir):
        to_dir = PWD + f'\\data\\delisting\\'

        if os.path.isfile(file_dir):
            shutil.copy2(file_dir, to_dir)
            os.remove(file_dir)
            print(f'{code} 제거 완료')

    def get_total_trade_data_kospi(self, code, recent_df, today_checklist, i):
        print('기존 데이터와 신규 데이터가 달라서 다시 다운받기 시작')
        while self.kiwoom.tr_remained:

            temp_df = get_stock_trade_data_until_now(self.kiwoom, 
                                                    code,
                                                    self.kiwoom.GetMasterCodeName(code), 
                                                    TODAY, 
                                                    STOCK_ITEM_DTYPE, 
                                                    TRADEDATA_DTYPE, 
                                                    next=2)
            time.sleep(1)
            self.api_count += 1

            if temp_df['날짜'].min() < pd.Timestamp('20100101'):
                temp_df = temp_df[temp_df['날짜'] > pd.Timestamp('20100101')]
                recent_df = recent_df.append(temp_df, ignore_index=True)
                break

            recent_df = recent_df.append(temp_df, ignore_index=True)

            print("API_COUNT :", self.api_count)

            if self.api_count >= 999:
                return 'api_limit', today_checklist

        recent_df.to_csv(DIR_KOSPI_DAILY + f'\\{code}.csv', encoding='utf-8', index=None)
        print('업데이트 및 저장 완료', end=' ')

        max_date = recent_df['날짜'].max()

        today_checklist.loc[today_checklist['종목코드'] == code, '일봉관리여부'] = True
        today_checklist.loc[today_checklist['종목코드'] == code, '일봉최종수정일'] = TODAY
        today_checklist.loc[today_checklist['종목코드'] == code, '일봉최근날짜'] = max_date.strftime("%Y%m%d")

        print(f'today_checklist에 업데이트 완료 {i+1}/{self.kospi_cnt_not_yet} ({api})')

        return 'complete', today_checklist

    def get_total_trade_data_kosdaq(self, code, recent_df, today_checklist, i):
        print('기존 데이터와 신규 데이터가 달라서 다시 다운받기 시작')
        while self.kiwoom.tr_remained:

            temp_df = get_stock_trade_data_until_now(self.kiwoom, 
                                                    code,
                                                    self.kiwoom.GetMasterCodeName(code), 
                                                    TODAY, 
                                                    STOCK_ITEM_DTYPE, 
                                                    TRADEDATA_DTYPE, 
                                                    next=2)
            time.sleep(1)
            self.api_count += 1

            if temp_df['날짜'].min() < pd.Timestamp('20100101'):
                temp_df = temp_df[temp_df['날짜'] > pd.Timestamp('20100101')]
                recent_df = recent_df.append(temp_df, ignore_index=True)
                break

            recent_df = recent_df.append(temp_df, ignore_index=True)

            print("API_COUNT :", self.api_count)

            if self.api_count == 999:
                return 'api_limit', today_checklist

        recent_df.to_csv(DIR_KOSDAQ_DAILY + f'\\{code}.csv', encoding='utf-8', index=None)
        print('업데이트 및 저장 완료', end=' ')

        max_date = recent_df['날짜'].max()

        today_checklist.loc[today_checklist['종목코드'] == code, '일봉관리여부'] = True
        today_checklist.loc[today_checklist['종목코드'] == code, '일봉최종수정일'] = TODAY
        today_checklist.loc[today_checklist['종목코드'] == code, '일봉최근날짜'] = max_date.strftime("%Y%m%d")

        print(f'today_checklist에 업데이트 완료 {i+1}/{self.kosdaq_cnt_not_yet} ({self.api_count})')

        return 'complete', today_checklist

            
        
    def iter_kospi(self, today_checklist, kospi_code_list_until_now):
        for i, kcwh in enumerate(self.kospi_not_yet):

            code = kcwh
            name = self.kiwoom.GetMasterCodeName(code)
            print(f'{name}({code}) => 처리시작', end=' ')

            file_dir = DIR_KOSPI_DAILY + f'\\{code}.csv'
            
            if os.path.isfile(file_dir):
                pre_df = pd.read_csv(file_dir, encoding='utf-8', dtype=TRADEDATA_DTYPE, parse_dates=['날짜'])
            else:
                print('상장폐지된 종목이므로 종료')
                continue
            
            max_date = pre_df['날짜'].max()
            min_date = pre_df['날짜'].min()
                
            if max_date == pd.Timestamp(TODAY):
                print(f'오늘 날짜까지 업데이트 완료된 상태', end=' ')
                today_checklist.loc[today_checklist['종목코드'] == code, '일봉관리여부'] = True
                today_checklist.loc[today_checklist['종목코드'] == code, '일봉최종수정일'] = TODAY
                today_checklist.loc[today_checklist['종목코드'] == code, '일봉최근날짜'] = max_date.strftime("%Y%m%d")

                print(f'today_checklist에 업데이트 완료 {i+1}/{self.kospi_cnt_not_yet} ({self.api_count})')
                continue
            
            if min_date < datetime(2010, 1, 1):
                pre_df = pre_df[pre_df['날짜'] > '2010-01-01']
                min_date = pre_df['날짜'].min()
            
            print(f"기존 데이터는 {str(min_date)[:10]}부터 {str(max_date)[:10]}까지 존재", end=' ')
            
            recent_df = get_stock_trade_data_until_now(self.kiwoom,
                                                        code, 
                                                        name, 
                                                        TODAY, 
                                                        STOCK_ITEM_DTYPE, 
                                                        TRADEDATA_DTYPE)
            time.sleep(0.7)
            self.api_count += 1

            if type(recent_df) == type(None):
                if code in kospi_code_list_until_now:
                    print(f'현재까지 코스피에서 거래중이지만 새로운 데이터가 없으므로 상장폐지 폴더로 이동', end=' ')
                    self.move_stock_data_to_delisting(code, file_dir)
                else:
                    print(f'현재 코스피에서 거래 안되므로 상장폐지 폴더로 이동', end=' ')
                    self.move_stock_data_to_delisting(code, file_dir)

                    continue

            if self.check_df(pre_df, recent_df):
                ret, today_checklist = self.get_total_trade_data_kospi(code, recent_df, today_checklist, i)
                if ret == 'api_limit':
                    return 'api_limit', today_checklist
                elif ret == 'complete':
                    continue

            lastest_df = recent_df[recent_df['날짜'] >= max_date]

            if lastest_df.shape[0]:
                print(f'오늘까지의 데이터에 비해 {lastest_df.shape[0]-1}일치 부족', end=' ')

                pre_df = (pre_df.iloc[1:, :].append(lastest_df, ignore_index=True)
                                .sort_values(by=['날짜'], ascending=False)
                                .reset_index(drop=True))

                pre_df.to_csv(file_dir, encoding='utf-8', index=None)
                print('업데이트 및 저장 완료', end=' ')

                today_checklist.loc[today_checklist['종목코드'] == code, '일봉관리여부'] = True
                today_checklist.loc[today_checklist['종목코드'] == code, '일봉최종수정일'] = TODAY
                today_checklist.loc[today_checklist['종목코드'] == code, '일봉최근날짜'] = pre_df['날짜'].max().strftime("%Y%m%d")

                print(f'today_checklist에 업데이트 완료 {i+1}/{self.kospi_cnt_not_yet} ({self.api_count})')

            if self.api_count == 999:
                return 'api_limit', today_checklist
        
        return 'kospi_complete', today_checklist

    def iter_kosdaq(self, today_checklist, kosdaq_code_list_until_now):
        for i, kcwh in enumerate(self.kosdaq_not_yet):
            code = kcwh
            name = self.kiwoom.GetMasterCodeName(code)
            print(f'{name}({code}) => 처리시작', end=' ')
            
            file_dir = DIR_KOSDAQ_DAILY + f'\\{code}.csv'
            
            if os.path.isfile(file_dir):
                pre_df = pd.read_csv(file_dir, encoding='utf-8', dtype=TRADEDATA_DTYPE, parse_dates=['날짜'])
            else:
                print('상장폐지된 종목이므로 종료')
                continue

            max_date = pre_df['날짜'].max()
            min_date = pre_df['날짜'].min()
                
            if max_date == pd.Timestamp(TODAY):
                print(f'오늘 날짜까지 업데이트 완료된 상태', end=' ')
                today_checklist.loc[today_checklist['종목코드'] == code, '일봉관리여부'] = True
                today_checklist.loc[today_checklist['종목코드'] == code, '일봉최종수정일'] = TODAY
                today_checklist.loc[today_checklist['종목코드'] == code, '일봉최근날짜'] = max_date.strftime("%Y%m%d")

                print(f'today_checklist에 업데이트 완료 {i+1}/{self.kosdaq_cnt_not_yet} ({self.api_count})')
                continue
            
            if min_date < datetime(2010, 1, 1):
                
                pre_df = pre_df[pre_df['날짜'] > '2010-01-01']
                min_date = pre_df['날짜'].min()
            
            print(f"기존 데이터는 {str(min_date)[:10]}부터 {str(max_date)[:10]}까지 존재", end=' ')
            
            recent_df = get_stock_trade_data_until_now(self.kiwoom,
                                                        code, 
                                                        name, 
                                                        TODAY, 
                                                        STOCK_ITEM_DTYPE, 
                                                        TRADEDATA_DTYPE)
            time.sleep(0.7)
            self.api_count += 1

            if type(recent_df) == type(None):
                if code in kosdaq_code_list_until_now:
                    print(f'현재까지 코스닥에서 거래중이지만 새로운 데이터가 없으므로 상장폐지 폴더로 이동', end=' ')
                    self.move_stock_data_to_delisting(code, file_dir)
                else:
                    print(f'현재 코스닥에서 거래 안되므로 상장폐지 폴더로 이동', end=' ')
                    self.move_stock_data_to_delisting(code, file_dir)

                    continue
            
            if self.check_df(pre_df, recent_df):
                ret, today_checklist = self.get_total_trade_data_kosdaq(code, recent_df, today_checklist, i)
                if ret == 'api_limit':
                    return 'api_limit', today_checklist
                elif ret == 'complete':
                    continue

            lastest_df = recent_df[recent_df['날짜'] >= max_date]

            if lastest_df.shape[0]:
                print(f'오늘까지의 데이터에 비해 {lastest_df.shape[0]-1}일치 부족', end=' ')

                pre_df = (pre_df.iloc[1:, :].append(lastest_df, ignore_index=True)
                                .sort_values(by=['날짜'], ascending=False)
                                .reset_index(drop=True))
                pre_df.to_csv(file_dir, encoding='utf-8', index=None)
                print('업데이트 및 저장 완료', end=' ')

                today_checklist.loc[today_checklist['종목코드'] == code, '일봉관리여부'] = True
                today_checklist.loc[today_checklist['종목코드'] == code, '일봉최종수정일'] = TODAY
                today_checklist.loc[today_checklist['종목코드'] == code, '일봉최근날짜'] = pre_df['날짜'].max().strftime("%Y%m%d")

                print(f'today_checklist에 업데이트 완료 {i+1}/{self.kosdaq_cnt_not_yet} ({self.api_count})')
                
            if self.api_count == 999:
                return 'api_limit', today_checklist
        
        return 'kosdaq_complete', today_checklist
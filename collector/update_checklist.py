import pandas as pd
from pykiwoom.kiwoom import *
from config.setting import *
from collector.update_daily_data import get_stock_trade_data_until_now

class CheckList:
    def __init__(self, kiwoom, API_COUNT):
        self.api_count = API_COUNT
        self.kiwoom = kiwoom
        self.today_checklist = {
            '시장명':[], 
            '종목명':[], 
            '종목코드':[], 
            '감리구분':[], 
            '상장일자':[], 
            '종목상태':[], 
            '체크최종수정일':[]
        }

        self.kospi = self.kiwoom.GetCodeListByMarket('0')
        self.kosdaq = self.kiwoom.GetCodeListByMarket('10')


        for code in self.kospi:
            
            self.today_checklist['시장명'].append('kospi')
            self.today_checklist['종목명'].append(self.kiwoom.GetMasterCodeName(code))
            self.today_checklist['종목코드'].append(code)
            self.today_checklist['감리구분'].append(self.kiwoom.GetMasterConstruction(code))
            self.today_checklist['상장일자'].append(self.kiwoom.GetMasterListedStockDate(code))
            self.today_checklist['종목상태'].append(self.kiwoom.GetMasterStockState(code))
            self.today_checklist['체크최종수정일'].append(TODAY)
            
        for code in self.kosdaq:
            self.today_checklist['시장명'].append('kosdaq')
            self.today_checklist['종목명'].append(self.kiwoom.GetMasterCodeName(code))
            self.today_checklist['종목코드'].append(code)
            self.today_checklist['감리구분'].append(self.kiwoom.GetMasterConstruction(code))
            self.today_checklist['상장일자'].append(self.kiwoom.GetMasterListedStockDate(code))
            self.today_checklist['종목상태'].append(self.kiwoom.GetMasterStockState(code))
            self.today_checklist['체크최종수정일'].append(TODAY)
            
        self.today_checklist = pd.DataFrame(self.today_checklist)
        self.today_checklist = self.today_checklist.assign(일봉관리여부=False)
        self.today_checklist = self.today_checklist.assign(일봉최종수정일=0)
        self.today_checklist = self.today_checklist.assign(일봉최초날짜=0)
        self.today_checklist = self.today_checklist.assign(일봉최근날짜=0)
        # self.today_checklist = self.today_checklist.assign(분봉관리여부=False)
        # self.today_checklist = self.today_checklist.assign(분봉최종수정일=0)
        # self.today_checklist = self.today_checklist.assign(분봉최초날짜=0)
        # self.today_checklist = self.today_checklist.assign(분봉최근날짜=0)


    def iter_checklist(self):

        kospi_idx = 1
        kosdaq_idx = 1

        for code in total_code_list_we_have:
            if code in kospi_code_list_we_have:
                stock_df = pd.read_csv(DIR_KOSPI_DAILY + f'\\{code}.csv', encoding='utf-8', dtype=TRADEDATA_DTYPE, parse_dates=['날짜'])
                min_date = stock_df['날짜'].min().strftime('%Y%m%d')
                max_date = stock_df['날짜'].max().strftime('%Y%m%d')
                self.today_checklist.loc[self.today_checklist['종목코드'] == code, '일봉관리여부'] = True
                self.today_checklist.loc[self.today_checklist['종목코드'] == code, '일봉최초날짜'] = min_date
                self.today_checklist.loc[self.today_checklist['종목코드'] == code, '일봉최근날짜'] = max_date

                print(f'{code}완료 ({kospi_idx} / {kospi_cnt_we_have})')
                kospi_idx += 1
            else:
                stock_df = pd.read_csv(DIR_KOSDAQ_DAILY + f'\\{code}.csv', encoding='utf-8', dtype=TRADEDATA_DTYPE, parse_dates=['날짜'])
                min_date = stock_df['날짜'].min().strftime('%Y%m%d')
                max_date = stock_df['날짜'].max().strftime('%Y%m%d')
                self.today_checklist.loc[self.today_checklist['종목코드'] == code, '일봉관리여부'] = True
                self.today_checklist.loc[self.today_checklist['종목코드'] == code, '일봉최초날짜'] = min_date
                self.today_checklist.loc[self.today_checklist['종목코드'] == code, '일봉최근날짜'] = max_date

                print(f'{code}완료 ({kosdaq_idx} / {kosdaq_cnt_we_have})')
                kosdaq_idx += 1


    def save_new_stock_data(self, not_tracked_list):
        
        for code in not_tracked_list['종목코드'].values:
            print(f'신규 종목코드 : {code} 데이터 다운로드 시작', end=' ')
            first_df = get_stock_trade_data_until_now(self.kiwoom,
                                                        code, 
                                                        self.kiwoom.GetMasterCodeName(code), 
                                                        TODAY, STOCK_ITEM_DTYPE, 
                                                        TRADEDATA_DTYPE)
            time.sleep(0.7)
            self.api_count += 1
            market = not_tracked_list[not_tracked_list['종목코드'] == code].values[0][0]

            if type(first_df) == type(None):
                return

            while self.kiwoom.tr_remained:

                temp_df = get_stock_trade_data_until_now(self.kiwoom, 
                                                        code,
                                                        self.kiwoom.GetMasterCodeName(code), 
                                                        TODAY, 
                                                        STOCK_ITEM_DTYPE, 
                                                        TRADEDATA_DTYPE, 
                                                        next=2)
                time.sleep(2)
                self.api_count += 1

                if temp_df['날짜'].min() < pd.Timestamp('20100101'):
                    temp_df = temp_df[temp_df['날짜'] > pd.Timestamp('20100101')]
                    first_df = first_df.append(temp_df, ignore_index=True)
                    break

                first_df = first_df.append(temp_df, ignore_index=True)

                print("API_COUNT :", self.api_count)
            else:
                print("API_COUNT :", self.api_count)

            if market == 'kospi':
                first_df.to_csv(DIR_KOSPI_DAILY + f'\\{code}.csv', encoding='utf-8', index=None)
            else:
                first_df.to_csv(DIR_KOSDAQ_DAILY + f'\\{code}.csv', encoding='utf-8', index=None)

            print('업데이트 및 저장 완료')


    def update_checklist(self):
        self.iter_checklist()
        
        not_tracked_list = self.today_checklist[self.today_checklist['일봉관리여부'] == False]

        if not_tracked_list.shape[0]:
            print(not_tracked_list)

            self.save_new_stock_data(not_tracked_list)

        self.today_checklist.to_csv(CSV_TODAY_CHECKLIST, index=None, encoding='utf-8')
        print('update checklist 완료')

        return self.api_count

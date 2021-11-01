import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
import time
import pandas as pd

TR_REQ_TIME_INTERVAL = 0.4 # 초당 5회 제한

class Kiwoom(QAxWidget):
    """
    QAxWidget은 QWidget과 QAxBase를 상속받은 클래스
    """
    
    total_cnt = 0
    present_cnt = 0
    
    def __init__(self):
        super().__init__()
        # self.ohlcv = {'stock_code': [], 'stock_name': [], 'date': [], 'open_price' : [], 'high_price' : [], 'low_price' : [], 'close_price' : [], 'volume' : []}
        self._create_kiwoom_instance()
        self._set_signal_slots()
        self.stock_code = ''
        self.stock_name = ''
        
    def _create_kiwoom_instance(self):
        self.setControl('KHOPENAPI.KHOpenAPICtrl.1')
    
    def _set_signal_slots(self):
        self.OnEventConnect.connect(self._event_connect)
        self.OnReceiveTrData.connect(self._receive_tr_data)
        
    def comm_connect(self):
        self.dynamicCall("CommConnect()")
        self.login_event_loop = QEventLoop()
        self.login_event_loop.exec_()
    
    def _event_connect(self, err_code):
        if err_code == 0:
            print('connected')
        else:
            print('disconnected')
        self.login_event_loop.exit()
        
    def get_code_list_by_market(self, market):
        code_list = self.dynamicCall("GetCodeListByMarket(QString)", market).split(';')
        return code_list[:-1]
    
    def get_master_code_name(self, code):
        code_name = self.dynamicCall("GetMasterCodeName(QString)", code)
        
        return code_name
        
    def set_input_value(self, item_name, input_value):
        """
        item_name : 아이템명. ex)"종목코드", "기준일자", "수정주가구분" 등
        input_value : 입력 값. ex)"034940", "20170224", 1 등
        """
        
        if item_name == '종목코드':
            self.stock_code = input_value
            self.stock_name = self.get_master_code_name(self.stock_code)
            
        self.dynamicCall("SetInputValue(QString, QString)", item_name, input_value)
    
    def comm_rq_data(self, request_name, transaction_code, prev_next, screen_no):
        """
        request_name : 사용자구분명. ex)"opt10081_request"
        transaction_code : transaction 명 ex)"opt10081"
        prev_next : 0(조회), 2(연속)
        screen_no : 4자리의 화면번호 ex)"0101"
        """
        
        self.dynamicCall("CommRqData(QString, QString, int, QString)", request_name, transaction_code, prev_next, screen_no)
        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()
        
    def _comm_get_data(self, code, real_type, field_name, index, item_name):
        """
        실제 데이터를 가져오는 메서드
        """
        
        ret = self.dynamicCall("CommGetData(QString, QString, QString, int, QString)", code, real_type, field_name, index, item_name)
        
        return ret.strip()
    
    def _get_repeat_cnt(self, request_name, transaction_code):
        """
        총 몇 개의 데이터가 왔는지 확인
        """
        
        ret = self.dynamicCall("GetRepeatCnt(QString, QString)", transaction_code, request_name)
        
        return ret
        
    def _receive_tr_data(self, screen_no, request_name, transaction_code, record_name, prev_next, a, b, c, d):
        """
        트랜젝션 이벤트가 발생했을 때 처리하는 메서드
        """
        if prev_next == '2':
            self.remained_data = True
        else:
            self.remained_data = False
            
        if request_name == 'opt10081_request':
            self._opt10081(request_name, transaction_code)
            
        try:
            self.tr_event_loop.exit()
        except AttributeError:
            pass
        
    def _opt10081(self, request_name, transaction_code):
        """
        opt10081을 통해 일봉 데이터 요청
        약 600개의 데이터(거래일 기준)가 반환
        """
        
        data_cnt = self._get_repeat_cnt(request_name, transaction_code)
        self.total_cnt += data_cnt
        self.present_cnt += data_cnt
        for i in range(data_cnt):
            date = self._comm_get_data(transaction_code, '', request_name, i, '일자')
            open_price = self._comm_get_data(transaction_code, '', request_name, i, '시가')
            high_price = self._comm_get_data(transaction_code, '', request_name, i, '고가')
            low_price = self._comm_get_data(transaction_code, '', request_name, i, '저가')
            close_price = self._comm_get_data(transaction_code, '', request_name, i, '현재가')
            volume = self._comm_get_data(transaction_code, '', request_name, i, '거래량')
            
            self.ohlcv['stock_code'].append(self.stock_code)
            self.ohlcv['stock_name'].append(self.stock_name)
            self.ohlcv['date'].append(date)
            self.ohlcv['open_price'].append(int(open_price))
            self.ohlcv['high_price'].append(int(high_price))
            self.ohlcv['low_price'].append(int(low_price))
            self.ohlcv['close_price'].append(int(close_price))
            self.ohlcv['volume'].append(int(volume))
            
        print(f'{self.stock_name}({self.stock_code}) 데이터 받기 진행중')

app = QApplication(sys.argv)
kiwoom = Kiwoom()
kiwoom.comm_connect()

code_list = kiwoom.get_code_list_by_market('10')
code_cnt = len(code_list)
cnt = 0



for stock_code in code_list:
    stock_name = kiwoom.get_master_code_name(stock_code)

    check_list = pd.read_csv('check.csv')

    idx = check_list.index[check_list['stock_item_code'] == stock_code].tolist()[0]
    if check_list.iloc[idx, 2] == 1:
        cnt += 1
        print(f'{stock_name}은 이미 다운받음.')
        continue

    cnt +=1
    kiwoom.ohlcv = {'stock_code': [], 'stock_name': [], 'date': [], 'open_price' : [], 'high_price' : [], 'low_price' : [], 'close_price' : [], 'volume' : []}
    print(f'{stock_name}({stock_code}) 데이터 받기 시작')
    
    kiwoom.set_input_value('종목코드', stock_code)
    kiwoom.set_input_value('기준일자', '20211101')
    kiwoom.set_input_value('수정주가구분', 1)
    kiwoom.comm_rq_data('opt10081_request', 'opt10081', 0, '0101')
    
    while kiwoom.remained_data: # remained_data 값이 True일 경우 연속조회 데이터가 존재한다는 것을 의미하므로 다시 한 번 동일한 TR을 요청
        time.sleep(1)
        kiwoom.set_input_value('종목코드', stock_code)
        kiwoom.set_input_value('기준일자', '20211101')
        kiwoom.set_input_value('수정주가구분', 1)
        kiwoom.comm_rq_data('opt10081_request', 'opt10081', 2, '0101') # 연속조회에선 3번째 인자를 2로 전달
    
    print(f'{stock_name}({stock_code}) 데이터 받기 끝({kiwoom.present_cnt}일 데이터)')

    df = pd.DataFrame(kiwoom.ohlcv)
    df.to_csv(f'./stock_data/{stock_code}.csv', index=None, encoding='utf-8')
    print(f'{stock_name}({stock_code}) 데이터 저장 끝')

    check_list.iloc[idx, 2] = 1
    check_list.to_csv('check.csv', index=None, encoding='utf-8')
    print('check 완료')

    print(f'지금까지 총 {kiwoom.total_cnt}줄의 데이터를 다운받음({cnt}/{code_cnt})')
    print()

    kiwoom.present_cnt = 0

    time.sleep(1)

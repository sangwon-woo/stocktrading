import sys
import time
import pythoncom
import datetime
import pandas as pd
from PyQt5.QAxContainer import *
from PyQt5.QtWidgets import *


if not QApplication.instance():
    app = QApplication(sys.argv)
    

class Kiwoom:
    def __init__(self) -> None:
        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.connected = False
        self.received = False
        self.transaction_items = None
        self.transaction_data = None
        self.transaction_remained = False
        self.condition_loaded = False

    def _on_event_connect(self, err_code):
        print(f"hander login {err_code}")
        if err_code == 0:
            self.connected = True


    def _on_receive_tr_data(self, screen_number, request_name, transaction_code, record, next):
        print(f"OnReceiveTrData {screen_number} {request_name} {transaction_code} {record} {next}")
        try:
            record = None
            items = None

            # remained data
            if next == '2':
                self.tr_remained = True
            else:
                self.tr_remained = False

            for output in self.tr_items['output']:
                record = list(output.keys())[0]
                items = list(output.values())[0]
                if record == self.tr_record:
                    break

            rows = self.GetRepeatCnt(transaction_code, request_name)
            if rows == 0:
                rows = 1

            data_list = []
            for row in range(rows):
                row_data = []
                for item in items:
                    data = self.GetCommData(transaction_code, request_name, row, item)
                    row_data.append(data)
                data_list.append(row_data)

            # data to DataFrame
            df = pd.DataFrame(data=data_list, columns=items)
            self.tr_data = df
            self.received = True
        except:
            pass

    def _on_receive_msg(self, screen_number, request_name, transaction_code, msg):
        print(f"OnReceiveMsg {screen_number} {request_name} {transaction_code} {msg}")

    def _on_receive_chejan_data(self, gubun, item_cnt, fid_list):
        print(f"OnReceiveChejanData {gubun} {item_cnt} {fid_list}")

    def _on_receive_condition_ver(self, ret, msg):
        if ret == 1:
            self.condition_loaded = True

    def _on_receive_tr_condition(self, screen_number, code_list, cond_name, cond_index, next):
        codes = code_list.split(';')[:-1]
        self.tr_condition_data = codes
        self.tr_condition_loaded= True

    def _set_signal_slots(self):
        self.ocx.OnEventConnect.connect(self._on_event_connect)
        self.ocx.OnReceiveTrData.connect(self._on_receive_tr_data)
        self.ocx.OnReceiveConditionVer.connect(self._on_receive_condition_ver)
        self.ocx.OnReceiveTrCondition.connect(self._on_receive_tr_condition)
        self.ocx.OnReceiveMsg.connect(self._on_receive_msg)
        self.ocx.OnReceiveChejanData.connect(self._on_receive_chejan_data)

login_event_loop = QEventLoop()
transaction_event_loop = QEventLoop()

def _on_event_connect(error_code):
    if error_code == 0:
        print('Login Success')
    login_event_loop.exit()

def _on_receive_tr_data(screen_number, 
                        request_name,
                        transaction_code,
                        record_name,
                        next,
                        data_length,
                        error_code,
                        message,
                        simple_message):
    if request_name == '주식기본정보요청':
        data = kiwoom.dynamicCall('GetCommData(QString, QString, int, QString)',
                                   transaction_code,
                                   record_name,
                                   0,
                                   '연중최고')
        if transaction_event_loop.isRunning():
            transaction_event_loop.exit()
        return data

def set_slots():
    kiwoom.OnEventConnect.connect(_on_event_connect)
    kiwoom.OnReceiveTrData.connect(_on_receive_tr_data)

def login():
    kiwoom.dynamicCall('CommConnect()')
    print('commconnect 실행')
    login_event_loop.exec_()

def opt10001(code):
    kiwoom.dynamicCall('SetInputValue(QString, QString)', '종목코드', code)
    kiwoom.dynamicCall('CommRqData(QString, QString QString, QString)', '주식기본정보요청', 'opt10001', '0', '0114')

    if not transaction_event_loop.isRunning():
        transaction_event_loop.exec_()
    time.sleep(0.2)
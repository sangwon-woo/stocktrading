import sys
import time
import pandas as pd
from PyQt5.QAxContainer import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from config.setting import *

if not QApplication.instance():
    app = QApplication(sys.argv)
    

class Kiwoom:
    def __init__(self) -> None:
        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.account_info = {}
        self.received = False
        self.transaction_items = None
        self.transaction_data = None
        self.transaction_remained = False
        self.condition_loaded = False
        self.login_event_loop = None
        self.transaction_event_loop = None
        self.real_data_event_loop = None
        self.chejan_event_loop = None
        self.msg_event_loop = None

        self._set_event_loop()
        self._set_signal_slots()

    def _set_signal_slots(self):
        self.ocx.OnEventConnect.connect(self._on_event_connect)
        self.ocx.OnReceiveTrData.connect(self._on_receive_tr_data)
        self.ocx.OnReceiveRealData.connect(self._on_receive_real_data)
        self.ocx.OnReceiveChejanData.connect(self._on_receive_chejan_data)
        self.ocx.OnReceiveMsg.connect(self._on_receive_msg)
        self.ocx.OnReceiveConditionVer.connect(self._on_receive_condition_ver)
        self.ocx.OnReceiveTrCondition.connect(self._on_receive_tr_condition)

    def _set_event_loop(self):
        self.login_event_loop = QEventLoop()
        self.transaction_event_loop = None
        self.real_data_event_loop = QEventLoop()
        self.chejan_event_loop = QEventLoop()
        self.msg_event_loop = QEventLoop()
        
#########################################################슬롯함수#########################################################################################################################
    def _on_event_connect(self, err_code):
        print(f"_on_event_connect. error code : {err_code}")
        if err_code == 0:
            print('Login Success')
            self.login_event_loop.exit()

    def _on_receive_tr_data(self, screen_number, request_name, transaction_code, record_name, next, data_length, error_code, message, simple_message):
        print(f"OnReceiveTrData\스크린번호: {screen_number}\n리퀘스트명: {request_name}\n트랜잭션코드: {transaction_code}\n레코드명: {record_name}\n다음페이지여부: {next}")
        if request_name == '주식기본정보요청':
            self.transaction_data = self.get_opt10001(transaction_code, record_name)

        elif request_name == '예수금상세현황요청':
            self.transaction_data = self.get_opw00001(transaction_code, request_name)

        elif request_name == '계좌평가잔고내역요청':
            self.transaction_data = self.get_opw00018(transaction_code, request_name)

    def _on_receive_real_data(self, stock_code, real_type, real_data):
        print(f"OnReceiveRealData\종목코드: {stock_code}\n실시간타입: {real_type}")
        if real_type == '장시작시간':
            pass
        elif real_type == '주식체결':
            pass

    def _on_receive_chejan_data(self, gubun, item_cnt, fid_list):
        print(f"OnReceiveChejanData {gubun} {item_cnt} {fid_list}")

    def _on_receive_msg(self, screen_number, request_name, transaction_code, msg):
        print(f"OnReceiveMsg {screen_number} {request_name} {transaction_code} {msg}")


    def _on_receive_condition_ver(self, ret, msg):
        if ret == 1:
            self.condition_loaded = True

    def _on_receive_tr_condition(self, screen_number, code_list, cond_name, cond_index, next):
        codes = code_list.split(';')[:-1]
        self.tr_condition_data = codes
        self.tr_condition_loaded= True
#####################################################################################################################################################################################
#####################################################################################################################################################################################
    def get_login_info(self):
        account_list = self.ocx.dynamicCall("GetLoginInfo(QString)", "ACCNO").rstrip(';')
        user_id = self.ocx.dynamicCall("GetLoginInfo(QString)", "USER_ID")
        user_name = self.ocx.dynamicCall("GetLoginInfo(QString)", "USER_NAME")
        server_type = self.ocx.dynamicCall("GetLoginInfo(QString)", "GetServerGubun")

        self.account_info['보유계좌목록'] = account_list
        self.account_info['사용자ID'] = user_id
        self.account_info['사용자이름'] = user_name
        self.account_info['서버구분'] = server_type

        print(self.account_info)

    def comm_connect(self):
        self.ocx.dynamicCall("CommConnect()")
        self.login_event_loop.exec_()

    def disconnect_real_data(self, screen_num = None):
        self.ocx.dynamicCall("DisconnectRealData(QString)", screen_num)

    def get_code_list_by_market(self, market_code):
        code_list = self.ocx.dynamicCall("GetCodeListByMarket(Qstring)", market_code)
        code_list = code_list.split(';')[:-1]

        return code_list
#####################################################################################################################################################################################
#####################################################################################################################################################################################
    def set_input_value(self, id, value):
        self.ocx.dynamicCall("SetInputValue(QString, QString)", id, value)

    def comm_rq_data(self, request_name, transaction_code, next, screen_number):
        error_code = self.ocx.dynamicCall("CommRqData(QString, QString, int, QString)", request_name, transaction_code, next, screen_number)
        self.transaction_event_loop = QEventLoop()
        self.transaction_event_loop.exec_()

        time.sleep(0.7)

        if error_code == 0:
            print('Request Success')

    def get_comm_data(self, transaction_code, record_name, index, item_name):
        data = self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)", transaction_code, record_name, index, item_name)

        return data
#####################################################################################################################################################################################
#####################################################################################################################################################################################
    def register_market_operation(self, screen_number, fid):
        pass

    def register_realtime_settlement(self, screen_number, stock_code, fid):
        pass
#####################################################################################################################################################################################
#####################################################################################################################################################################################
    def request_opt10001(self, stock_code):
        self.set_input_value("종목코드", stock_code)

        self.comm_rq_data("주식기본정보요청", 'opt10001', 0, '0114')

    def get_opt10001(self, transaction_code, record_name):
        ret = {}

        stock_code = self.get_comm_data(transaction_code, record_name, 0, "종목코드").strip()
        stock_name = self.get_comm_data(transaction_code, record_name, 0, "종목명").strip()
        settling_day = int(self.get_comm_data(transaction_code, record_name, 0, "결산월").strip())
        face_value = int(self.get_comm_data(transaction_code, record_name, 0, "액면가").strip())
        capital = int(self.get_comm_data(transaction_code, record_name, 0, "자본금").strip())
        quoted_share = int(self.get_comm_data(transaction_code, record_name, 0, "상장주식").strip())
        yearly_highest = int(self.get_comm_data(transaction_code, record_name, 0, "연중최고").strip().strip('+').strip('-'))
        credit_ratio = float(self.get_comm_data(transaction_code, record_name, 0, "신용비율").strip().strip('+').strip('-'))
        yearly_lowest = int(self.get_comm_data(transaction_code, record_name, 0, "연중최저").strip().strip('+').strip('-'))
        market_capital = int(self.get_comm_data(transaction_code, record_name, 0, "시가총액").strip())
        market_capital_ratio = self.get_comm_data(transaction_code, record_name, 0, "시가총액비중")
        market_capital_ratio = '' if market_capital_ratio.strip() == '' else float(market_capital_ratio).strip()
        foreign_exhaustion_rate = float(self.get_comm_data(transaction_code, record_name, 0, "외인소진률").strip().strip('+').strip('-'))
        substitute_price = int(self.get_comm_data(transaction_code, record_name, 0, "대용가").strip())
        per = float(self.get_comm_data(transaction_code, record_name, 0, "PER").strip())
        eps = float(self.get_comm_data(transaction_code, record_name, 0, "EPS").strip())
        roe = float(self.get_comm_data(transaction_code, record_name, 0, "ROE").strip())
        pbr = float(self.get_comm_data(transaction_code, record_name, 0, "PBR").strip())
        ev = float(self.get_comm_data(transaction_code, record_name, 0, "EV").strip())
        bps = float(self.get_comm_data(transaction_code, record_name, 0, "BPS").strip())
        sales = int(self.get_comm_data(transaction_code, record_name, 0, "매출액").strip())
        profit = int(self.get_comm_data(transaction_code, record_name, 0, "영업이익").strip())
        net_profit = int(self.get_comm_data(transaction_code, record_name, 0, "당기순이익").strip())
        highest_250 = int(self.get_comm_data(transaction_code, record_name, 0, "250최고").strip().strip('+').strip('-'))
        lowest_250 = int(self.get_comm_data(transaction_code, record_name, 0, "250최저").strip().strip('+').strip('-'))
        open_price = int(self.get_comm_data(transaction_code, record_name, 0, "시가").strip().strip('+').strip('-'))
        high_price = int(self.get_comm_data(transaction_code, record_name, 0, "고가").strip().strip('+').strip('-'))
        low_price = int(self.get_comm_data(transaction_code, record_name, 0, "저가").strip().strip('+').strip('-'))
        upper_limit_price = int(self.get_comm_data(transaction_code, record_name, 0, "상한가").strip().strip('+').strip('-'))
        lower_limit_price = int(self.get_comm_data(transaction_code, record_name, 0, "하한가").strip().strip('+').strip('-'))
        standard_price = int(self.get_comm_data(transaction_code, record_name, 0, "기준가").strip().strip('+').strip('-'))
        date_hightest_250 = int(self.get_comm_data(transaction_code, record_name, 0, "250최고가일").strip().strip('+').strip('-'))
        ratio_highest_250 = float(self.get_comm_data(transaction_code, record_name, 0, "250최고가대비율").strip().strip('+').strip('-'))
        date_lowest_250 = int(self.get_comm_data(transaction_code, record_name, 0, "250최저가일").strip().strip('+').strip('-'))
        ratio_lowest_250 = float(self.get_comm_data(transaction_code, record_name, 0, "250최저가대비율").strip().strip('+').strip('-'))
        current_price = int(self.get_comm_data(transaction_code, record_name, 0, "현재가").strip())
        volume = int(self.get_comm_data(transaction_code, record_name, 0, "거래량").strip())
        face_value_unit = str(self.get_comm_data(transaction_code, record_name, 0, "액면가단위").strip())
        distribution_stock = int(self.get_comm_data(transaction_code, record_name, 0, "유통주식").strip())
        distribution_ratio = float(self.get_comm_data(transaction_code, record_name, 0, "유통비율").strip())

        ret['종목코드'] = stock_code
        ret['종목명'] = stock_name
        ret['결산월'] = settling_day
        ret['액면가'] = face_value
        ret['자본금'] = capital
        ret['상장주식'] = quoted_share
        ret['신용비율'] = credit_ratio
        ret['연중최고'] = yearly_highest
        ret['연중최저'] = yearly_lowest
        ret['시가총액'] = market_capital
        ret['시가총액비중'] = market_capital_ratio
        ret['외인소진률'] = foreign_exhaustion_rate
        ret['대용가'] = substitute_price
        ret['PER'] = per
        ret['EPS'] = eps
        ret['roe'] = roe
        ret['PBR'] = pbr
        ret['EV'] = ev
        ret['BPS'] = bps
        ret['매출액'] = sales
        ret['영업이익'] = profit
        ret['당기순이익'] = net_profit
        ret['250최고'] = highest_250
        ret['250최저'] = lowest_250
        ret['시가'] = open_price
        ret['고가'] = high_price
        ret['저가'] = low_price
        ret['상한가'] = upper_limit_price
        ret['하한가'] = lower_limit_price
        ret['기준가'] = standard_price
        ret['250최고가일'] = date_hightest_250
        ret['250최고가대비율'] = ratio_highest_250
        ret['250최저가일'] = date_lowest_250
        ret['250최저가대비율'] = ratio_lowest_250
        ret['현재가'] = current_price
        ret['거래량'] = volume
        ret['액면가단위'] = face_value_unit
        ret['유통주식'] = distribution_stock
        ret['유통비율'] = distribution_ratio

        self.transaction_event_loop.exit()

        return ret

    def request_opw00001(self):
        self.set_input_value('계좌번호', REAL_ACCOUNT)
        self.set_input_value('비밀번호', PASSWORD)
        self.set_input_value('비밀번호입력매체구분', '00')
        self.set_input_value('조회구분', '1')

        self.comm_rq_data('예수금상세현황요청', 'opw00001', 0, '2000')

    def get_opw00001(self, transaction_code, request_name):
        ret = {}

        deposit = int(self.get_comm_data(transaction_code, request_name, 0, '예수금'))
        withdrawable_deposit = int(self.get_comm_data(transaction_code, request_name, 0, '출금가능금액'))

        ret['예수금'] = deposit
        ret['출금가능금액'] = withdrawable_deposit

        self.transaction_event_loop.exit()

        return ret

    def request_opw00018(self):
        self.set_input_value('계좌번호', REAL_ACCOUNT)
        self.set_input_value('비밀번호', PASSWORD)
        self.set_input_value('비밀번호입력매체구분', '00')
        self.set_input_value('조회구분', '1')

        self.comm_rq_data('계좌평가잔고내역요청', 'opw00018', 0, '2000')

    def get_opw00018(self, transaction_code, request_name):
        ret = {}

        total_buy_money = int(self.get_comm_data(transaction_code, request_name, 0, '총매입금액'))
        total_profit_loss_money = int(self.get_comm_data(transaction_code, request_name, 0, '총평가손익금액'))
        total_profit_loss_rate = int(self.get_comm_data(transaction_code, request_name, 0, '총수익률(%)'))

        ret['총매입금액'] = total_buy_money
        ret['총평가손익금액'] = total_profit_loss_money
        ret['총수익률(%)'] = total_profit_loss_rate

        self.transaction_event_loop.exit()

        return ret










#####################################################################################################################################################################################
#####################################################################################################################################################################################
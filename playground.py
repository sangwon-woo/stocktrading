# import pymysql
# from sqlalchemy import create_engine, MetaData, Table
# import time
# from DBconfig import base_addr

# pymysql.install_as_MySQLdb()

# engine = create_engine(base_addr + "/db_sqlstk", encoding='utf-8')

# with engine.connect() as conn:
#     sql_sa = """
#         SELECT STK_CD, COUNT(*) AS 로우수
#         FROM DB_SQLSTK.HISTORY_DT
#         GROUP BY STK_CD;
#     """

#     data = conn.execute(sql_sa).fetchall()
#     print(data)

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QAxContainer import *

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyStock")
        self.setGeometry(300, 300, 300, 150)

        # kiwoom login
        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.kiwoom.dynamicCall('CommConnect()')

        # OpenAPI+ Event
        self.kiwoom.OnEventConnect.connect(self.event_connect)
        self.kiwoom.OnReceiveTrData.connect(self.receive_trdata)
        """ 
        OnReceiveTrData 이벤트는 서버와 통신한 후 서버로부터 데이터를 전달받은 시점에 발생
        OnReceiveTrData 이벤트는 총 9개의 인자가 전달
        """

        label = QLabel('종목코드:', self)
        label.move(20, 20)

        self.code_edit = QLineEdit(self)
        self.code_edit.move(80, 20)
        self.code_edit.setText('039490')

        btn1 = QPushButton('조회', self)
        btn1.move(190, 20)
        btn1.clicked.connect(self.btn1_clicked)

        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(10, 60, 280, 80)
        self.text_edit.setEnabled(False)

    def event_connect(self, err_code):
        if err_code == 0:
            self.text_edit.append('Login finished')
    
    def btn1_clicked(self):
        code = self.code_edit.text()
        self.text_edit.append('종목코드: ', code)

        # SetInputValue('종목코드', '039490')
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "종목코드", code)

        # CommRqData => TR을 서버로 송신
        # opt10001 : 주식기본정보요청
        self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)", "opt10001_req", "opt10001", 0, "0101")

    def receive_trdata(self, screen_no, rqname, trcode, recordname, prev_next, data_len, err_code, msg1, msg2):
        """
        OnReceiveTrData 이벤트가 9개의 인자를 전달하므로 9개의 파라미터를 갖고옴
        screen_no : 화면번호
        rqname : 사용자구분 명
        trcode : transaction 명
        recordname : record 명
        prev_next : 연속조회 유무
        data_len : 더 이상 사용 안함
        err_code : 더 이상 사용 안함
        msg1 : 더 이상 사용 안함
        msg2 : 더 이상 사용 안함ㅊ
        """
        if rqname == 'opt10001_req':
            name = self.kiwoom.dynamicCall('CommGetData(QString, QString, QString, int, QString)', trcode, "", rqname, 0, '종목명')
            volume = self.kiwoom.dynamicCall('CommGetData(QString, QString, QString, int, QString)', trcode, "", rqname, 0, '거래량')

        self.text_edit.append('종목명: ', name.strip())
        self.text_edit.append('거래량: ', volume.strip())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    app.exec_()
    
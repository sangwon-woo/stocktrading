"""
키움 API
1. method : 호출하면 즉시 결과값이 리턴되는 방식으로 결과값이 리턴되기 전까지 다음 줄의 코드가 수행되지 않고 블록됨
2. TR     : 호출하면 임의 시간이 지난 후에 결과값이 콜백(callback)되는 방식으로 호출 후 다음 줄의 코드 수행 가능
3. 실시간 : 한 번 구독하면 구독 해지 전까지 이벤트가 발생할 때마다 결과값이 리턴되는 방식
"""


import sys 
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
import datetime


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RealTime")
        self.setGeometry(300, 300, 300, 400)

        btn = QPushButton("Register", self)
        btn.move(20, 20)
        btn.clicked.connect(self.btn_clicked)

        btn2 = QPushButton("DisConnect", self)
        btn2.move(20, 100)
        btn2.clicked.connect(self.btn2_clicked)

        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.OnEventConnect.connect(self._handler_login)
        self.ocx.OnReceiveRealData.connect(self._handler_real_data)
        self.CommmConnect()

    def btn_clicked(self):
        self.SetRealReg("1000", "005930", "20;10", 0)
        # self.SetRealReg("2000", "", "215;20;214", 0)
        print("called\n")

    def btn2_clicked(self):
        self.DisConnectRealData("1000")

    def CommmConnect(self):
        self.ocx.dynamicCall("CommConnect()")
        self.statusBar().showMessage("login 중 ...")

    def _handler_login(self, err_code):
        if err_code == 0:
            self.statusBar().showMessage("login 완료")


    def _handler_real_data(self, code, real_type, data):
        print(code, real_type, data)
        if real_type == "장시작시간":
            gubun =  self.GetCommRealData(code, 215)
            remained_time =  self.GetCommRealData(code, 214)
            print(gubun, remained_time)            


    def SetRealReg(self, screen_no, code_list, fid_list, real_type):
        self.ocx.dynamicCall("SetRealReg(QString, QString, QString, QString)", 
                              screen_no, code_list, fid_list, real_type)

    def DisConnectRealData(self, screen_no):
        self.ocx.dynamicCall("DisConnectRealData(QString)", screen_no)

    def GetCommRealData(self, code, fid):
        data = self.ocx.dynamicCall("GetCommRealData(QString, int)", code, fid) 
        return data


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()
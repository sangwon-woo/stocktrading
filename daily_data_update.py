
from setting import *
from pykiwoom.kiwoom import *
from update_daily_data import *
from update_checklist import *



def init_kiwoom():
    kiwoom = Kiwoom()
    kiwoom.CommConnect(block=True)

    state = kiwoom.GetConnectState()
    if state == 0:
        print("미연결")
    elif state == 1:
        print("연결완료")

    accounts = kiwoom.GetLoginInfo("ACCNO")[0]                 # 전체 계좌 리스트
    user_name = kiwoom.GetLoginInfo("USER_NAME")            # 사용자명

    print(f'{user_name}의 {accounts}계좌로 접속')






if __name__ == "__main__":
    init_kiwoom()
    update_checklist()



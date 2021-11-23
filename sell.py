'''
이 스크립트의 목적은 매도 주문을 넣는 것이다.
매도에는 두 가지 종류가 있다.
    손절
    익절
손절 및 익절 모두 자산관리가 필요하다. 
'''

from pykiwoom.kiwoom import Kiwoom
import pandas as pd
import numpy as np
import time





if __name__ == "__main__":
    kiwoom = Kiwoom()
    kiwoom.CommConnect(block=True)

    accounts = kiwoom.GetLoginInfo('ACCNO')
    account = accounts[0]

    ret = kiwoom.SendOrder('시장가매수', '0101', account, 1, '000900', 100, 0, '03', '') # 시장가 등록. 
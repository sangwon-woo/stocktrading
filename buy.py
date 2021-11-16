'''
이 스크립트의 목적은 매수 주문을 넣는 것이다.
매수에는 두 가지 종류가 있다.
    첫 진입
    애드업
첫 진입과 애드업 모두 위험관리 및 자산관리가 필요하다. 
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
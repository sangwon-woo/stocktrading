# Surfing : Automated Stock Trading System
<h2> # Algorithm Trading & System Trading </h2>

키움증권 API를 사용하여 코스피, 코스닥에서 거래되는 종목을 특정 거래 조건에 맞춰 매매하는 시스템

## # Base Class Architecture
![BaseClassArchitecture](BaseClassArchitecture.png)
- QApplication : 프로그램을 앱처럼 실행하거나 홈페이지처럼 실행할 수 있도록 그래픽적인 요소를 제어할 수 있는 기능을 포함
- QAxContainer : 마이크로소프트사에서 제공하는 프로세스를 가지고 화면을 구성하는 데 필요한 기능들이 담겨있음
- QAxWidget : 디자인 구성을 컨트롤하고 재사용하는 기능들을 포함
- QAxBase.setControl() : 설치된 API 모듈을 파이썬에서 쓸 수 있도록 함. 즉, .ocx 확장자도 파이썬에서 사용할 수 있게 함
- QAxBase.dynamicCall()
- OCX : OLE Custom eXtension의 약자. 마이크로소프트 윈도우 운영체제에서 실행할 수 있도록 만들어진 특수한 목적의 프로그램이며 확장자명이 ocx임.


## # Kiwoom OpenAPI Method
- 시그널(Signal) : 키움 서버에 요청하는 신호
- 슬롯(Slot) : 요청한 데이터의 결과값을 받을 공간
- 이벤트(Event) : 시그널이 발생하면 결과값을 어느 슬롯에서 받을 것인지 연결해주는 다리
### 1. 키움 API를 파이썬에서 사용(키움 API 레지스트리 제어 함수)
```python
self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")  
# 또는
kiwoom = self.setControl("KHOPENAPI.KHOpenAPICtrl.1")
```

### 2. QAxBase 클래스의 dynamicCall Method를 사용하는 함수
#### CommConnect()
"로그인 윈도우 실행"
```python
self.kiwoom.dynamicCall("CommConnect()")
```

#### GetConnectState()
"현재 접속상태 반환"
```python
self.kiwoom.dynamicCall("GetConnectState()")
```

#### SetInputValue()
"Transaction 입력 값을 서버통신 전에 입력"
```python
self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "종목코드", '039490')
```


#### CommRqData()
"TR을 서버로 전송"
```python
self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)", "opt10001_req", "opt10001", 0, "0101")
```
    참고! 여기서는 opt10001이라는 트랜젝션을 사용
    opt10001: 주식기본정보요청
    1. OpenAPI 조회 함수 입력값을 설정
        종목코드 = 전문 조회할 종목코드
        SetInputValue("종목코드", "입력값 1");
    2. OpenAPI 조회 함수를 호출해서 전문을 서버로 전송
        CommRqData("RQName", "opt10001", "0", "화면번호")

#### GetCommData(1, 2, 3, 4, 5)
"TR 데이터, 실시간 데이터, 체결잔고 데이터를 반환"
```python
item_name = self.kiwoom.dynamicCall("GetCommData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "종목명")
```
    참고! 파라미터는 다음과 같다.
    TR Data     : 1. TR명,      2. 사용안함,    3. 레코드명,    4. 반복인덱스,  5. 아이템명
    실시간 Data : 1. Key Code,  2. Real Type,   3. Item Index,  4. 사용안함     5. 사용안함
    체결 Data   : 1. 체결구분,  2. "-1",        3. 사용안함,    4. Item Index,  5. 사용안함

#### GetLoginInfo(QString)
"로그인 후 사용할 수 있으며 인자값에 대응하는 정보를 얻을 수 있음"
```python
account_num = self.kiwoom.dynamicCall("GetLoginInfo(QString)", ["ACCNO"]).rstrip(';')
```
    참고! 인자에 들어갈 수 있는 값은 아래와 같음
    * "ACCOUNT_CNT" : 전체 계좌 개수를 반환
    * "ACCNO" : 전체 계좌를 반환. 계좌별 구분은 ';'
    * "USER_ID" : 사용자 ID 반환
    * "USER_NAME" : 사용자명 반환
    * "KEY_BSECGB" : 키보드보안 해지여부. 0: 정상, 1: 해지
    * "FIREW_SECGB" : 방화벽 설정 여부. 0: 미설정, 1: 설정, 2: 해지
    * "GetServerGubun" : 접속서버 구분을 반환. 1: 모의투자, 나머지: 실서버

#### GetCodeListByMarket
"시장구분에 따른 종목코드를 반환"
```python
kospi_code_list = self.kiwoom.dynamicCall("GetCodeListByMarket(QString)", ["0"]).split(';')
```

    참고! 인자에 들어갈 수 있는 값은 아래와 같음
    * "0" : 장내
    * "3" : ELW
    * "4" : Mutual Fund
    * "5" : 신주인수권
    * "6" : 리츠
    * "8" : ETF
    * "9" : High Yield Fund 
    * "10" : KOSDAQ
    * "30" : 제3시장

#### GetMasterCodeName
"종목코드의 한글명을 반환"
```python
item_name = self.kiwoom.dynamicCall("GetMasterCodeName(QString)", ["005680"])
```

### 3. Event 처리 함수
#### OnEventConnect()
"로그인 이벤트 처리"
```python
self.kiwoom.OnEventConnect.connect(self.event_connect)

def event_connect(self, err_code):
    if err_code == 0: self.text_edit.append("로그인 성공")
```

#### OnReceiveTrData()
"서버통신 후 데이터를 받은 시점을 알려줌"
```python
self.kiwoom.OnReceiveTrData.connect(self.receive_trdata)

def receive_trdata(self, screen_no, rqname, trcode, recordname, prev_next, data_len, err_code, msg1, msg2):
    if rqname == 'opt10001_req':
        pass
```

* screen_no : 화면번호
* rqname : 사용자구분 명, CommRqData의 rqname과 매핑되는 이름
* trcode : transaction 명, CommRqData의 trcode와 매핑되는 이름
* recordname : record 명
* prev_next : 연속조회 유무
* data_len : 사용안함
* err_code : 사용안함
* msg1 : 사용안함
* msg2 : 사용안함


### 4. 트랜잭션
#### 예수금 정보 가져오기 => opw00001
```python
self.screen_my_info = 2000

def detail_account_info(self, sPrevNext="0"):
    self.dynamicCall("SetInputValue(QString, QString)", "계좌번호", self.account_num)
    self.dynamicCall("SetInputValue(QString, QString)", "비밀번호", "0000")
    self.dynamicCall("SetInputValue(QString, QString)", "비밀번호입력매체구분", "00")
    self.dynamicCall("SetInputValue(QString, QString)", "조회구분", "1")
    self.dynamicCall("CommRqData(QString, QString, int, QString)", "예수금상세현황요청", "opw00001", sPrevNext, self.screen_my_info)

self.OnReceiveTrData.connect(self.trdata_slot)

def trdata_slot(self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext):
    if sRQName == '예수금상세현황요청':
        deposit = self.dynamicCall('GetCommData(QString, QString, int, QString)', sTrCode, sRQName, 0, '예수금')
        output_deposit = self.dynamicCall('GetCommData(QString, QString, int, QString)', sTrCode, sRQName, 0, '출금가능금액')
        self.stop_screen_cancel(self.screen_my_info)

def stop_screen_cancel(self, sScrNo=None):
    self.dynamicCall('DisconnectRealData(QString)', sScrNo)
```

#### 계좌평가잔고내역 정보 가져오기 => opw00018
```python
self.screen_my_info = 2000

def detail_account_mystock(self, sPrevNext="0"):
    self.dynamicCall("SetInputValue(QString, QString)", "계좌번호", self.account_num)
    self.dynamicCall("SetInputValue(QString, QString)", "비밀번호", "0000")
    self.dynamicCall("SetInputValue(QString, QString)", "비밀번호입력매체구분", "00")
    self.dynamicCall("SetInputValue(QString, QString)", "조회구분", "1")
    self.dynamicCall("CommRqData(QString, QString, int, QString)", "계좌평가잔고내역요청", "opw00018", sPrevNext, self.screen_my_info)

self.OnReceiveTrData.connect(self.trdata_slot)
self.account_stock_dict = {}

def trdata_slot(self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext):
    if sRQName == "계좌평가잔고내역요청":
        total_buy_money = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "총매입금액") # 출력 : 000000000746100
        total_profit_loss_money = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "총평가손익금액") # 출력 : 000000000009761
        total_profit_loss_rate = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "총수익률(%)") # 출력 : 000000001.31


        rows = self.dynamicCall("GetRepeatCnt(QString, QString)", sTrCode, sRQName) # 최대 20종목

        for i in range(rows):
            code = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "종목번호")
            code = code.strip()[1:]

            code_nm = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "종목명")
            stock_quantity = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "보유수량")
            buy_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "매입가")
            learn_rate = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "수익률(%)")
            current_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "현재가")
            total_chegual_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "매입금액")
            possible_quantity = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "매매가능수량")


            if code in self.account_stock_dict:
                pass
            else:
                self.account_stock_dict[code] = {}

            code_nm = code_nm.strip()
            stock_quantity = int(stock_quantity.strip())
            buy_price = int(buy_price.strip())
            learn_rate = float(learn_rate.strip())
            current_price = int(current_price.strip())
            total_chegual_price = int(total_chegual_price.strip())
            possible_quantity = int(possible_quantity.strip())

            self.account_stock_dict[code].update({"종목명": code_nm})
            self.account_stock_dict[code].update({"보유수량": stock_quantity})
            self.account_stock_dict[code].update({"매입가": buy_price})
            self.account_stock_dict[code].update({"수익률(%)": learn_rate})
            self.account_stock_dict[code].update({"현재가": current_price})
            self.account_stock_dict[code].update({"매입금액": total_chegual_price})
            self.account_stock_dict[code].update({"매매가능수량": possible_quantity})

        if sPrevNext == "2":
            self.detail_account_mystock(sPrevNext="2")
        else:
            self.detail_account_info_event_loop.exit()


def stop_screen_cancel(self, sScrNo=None):
    self.dynamicCall('DisconnectRealData(QString)', sScrNo)
```


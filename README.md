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
### 1. 키움 API를 파이썬에서 사용(키움 API 레지스트리 제어 함수)
self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")  
또는   
kiwoom = self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

### 2. QAxBase 클래스의 dynamicCall Method를 사용하는 함수
#### CommConnect()
"로그인 윈도우 실행"
self.kiwoom.dynamicCall("CommConnect()")

#### GetConnectState()
"현재 접속상태 반환"
self.kiwoom.dynamicCall("GetConnectState()")

#### SetInputValue()
"Transaction 입력 값을 서버통신 전에 입력"
self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "종목코드", '039490')


#### CommRqData()
"TR을 서버로 전송"
self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)", "opt10001_req", "opt10001", 0, "0101")

    참고! 여기서는 opt10001이라는 트랜젝션을 사용
    opt10001: 주식기본정보요청
    1. OpenAPI 조회 함수 입력값을 설정
        종목코드 = 전문 조회할 종목코드
        SetInputValue("종목코드", "입력값 1");
    2. OpenAPI 조회 함수를 호출해서 전문을 서버로 전송
        CommRqData("RQName", "opt10001", "0", "화면번호")

## CommGetData(1, 2, 3, 4, 5)
"TR 데이터, 실시간 데이터, 체결잔고 데이터를 반환"
item_name = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "종목명")

    참고! 파라미터는 다음과 같다.
    TR Data     : 1. TR명,      2. 사용안함,    3. 레코드명,    4. 반복인덱스,  5. 아이템명
    실시간 Data : 1. Key Code,  2. Real Type,   3. Item Index,  4. 사용안함     5. 사용안함
    체결 Data   : 1. 체결구분,  2. "-1",        3. 사용안함,    4. Item Index,  5. 사용안함

## GetLoginInfo()
"로그인한 사용자 정보를 반환"
account_num = self.kiwoom.dynamicCall("GetLoginInfo(QString)", ["ACCNO"]).rstrip(';')

    참고! 인자에 들어갈 수 있는 값은 아래와 같음
    * "ACCOUNT_CNT" : 전체 계좌 개수를 반환
    * "ACCNO" : 전체 계좌를 반환. 계좌별 구분은 ';'
    * "USER_ID" : 사용자 ID 반환
    * "USER_NAME" : 사용자명 반환
    * "KEY_BSECGB" : 키보드보안 해지여부. 0: 정상, 1: 해지
    * "FIREW_SECGB" : 방화벽 설정 여부. 0: 미설정, 1: 설정, 2: 해지

## GetCodeListByMarket
"시장구분에 따른 종목코드를 반환"
kospi_code_list = self.kiwoom.dynamicCall("GetCodeListByMarket(QString)", ["0"]).split(';')

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

## GetMasterCodeName
"종목코드의 한글명을 반환"
item_name = self.kiwoom.dynamicCall("GetMasterCodeName(QString)", ["005680"])


# Event 처리 함수
## OnEventConnect()
"로그인 이벤트 처리"
self.kiwoom.OnEventConnect.connect(self.event_connect)

def event_connect(self, err_code):
    if err_code == 0: self.text_edit.append("로그인 성공")

## OnReceiveTrData()
"서버통신 후 데이터를 받은 시점을 알려줌"
self.kiwoom.OnReceiveTrData.connect(self.receive_trdata)

def receive_trdata(self, screen_no, rqname, trcode, recordname, prev_next, data_len, err_code, msg1, msg2):
    if rqname == 'opt10001_req':
        pass
* screen_no : 화면번호
* rqname : 사용자구분 명, CommRqData의 rqname과 매핑되는 이름
* trcode : transaction 명, CommRqData의 trcode와 매핑되는 이름
* recordname : record 명
* prev_next : 연속조회 유무
* data_len : 사용안함
* err_code : 사용안함
* msg1 : 사용안함
* msg2 : 사용안함
'''
이 스크립트의 목표는 매일 장 마감 이후 체크리스트를 업데이트 하는 것이다.
그럼 순서는 어떻게 될까?
우선 체크리스트를 연다. 
코스피, 코스닥 종목과 관련 정보를 키움 증권 api를 통해 받아온다. 
기존 체크리스트에서 달라진 것이 어디에 있는지 확인한다. 
달라진 것은 따로 문서를 만들어서 관리한다.
안 달라진 것은 최종 수정일만 당일 날짜로 업데이트 한다. 
그리고 다시 저장한다. 
'''
'''
이 스크립트의 목적은 위험관리다. 
위험 관리는 여러 방법이 존재한다.
나는 그 중에서 3% 룰을 따르겠다. 
이유는 없다. 그냥 2%는 너무 보수적인 것 같고
3이라는 숫자가 완벽한 숫자이기 때문이다.
위험관리가 들어가야 할 시점은 매수할 때다. 
그리고 매수할 때는 반드시 손절 포인트를 잡고 들어가야 한다. 
'''

class RiskManagement:
    def __init__(self) -> None:
        self.total_asset = 0
        self.risk_percentage = 0

    def set_total_asset(self, total_asset):
        self.total_asset = total_asset

    def set_risk_percentage(self, risk_percentage):
        self.risk_percentage = risk_percentage

    

from kiwoom_api import *

k = Kiwoom()

k.comm_connect()
k.get_login_info()
k.request_opt10001('000020')
print(k.transaction_data)

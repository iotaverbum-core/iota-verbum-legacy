from partner_sdk.client import IotaClient
c = IotaClient('http://127.0.0.1:8000')
print('token:', c.auth())
res = c.analyze_text('God is love; love acts; love bears fruit.')
print(res)
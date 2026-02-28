import requests, typing as t
class IotaClient:
    def __init__(self, host:str, secret:str='dev-shared-secret'):
        self.host=host; self.token=None; self.secret=secret
    def auth(self):
        r=requests.post(f'{self.host}/partner/auth/token', data={'shared_secret':self.secret})
        r.raise_for_status(); self.token=r.json().get('token')
        return self.token
    def analyze_text(self, text:str)->dict:
        assert self.token, 'call auth() first'
        r=requests.post(f'{self.host}/partner/analyze', data={'token':self.token,'text':text})
        r.raise_for_status(); return r.json()
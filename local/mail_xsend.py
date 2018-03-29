import requests
import json


def mail_xsend(to, subject, var, link):
    url = 'https://api.mysubmail.com/mail/xsend'
    data = {
        'appid': '11664',
        'to': '<{}>'.format(to),
        'subject': '{}'.format(subject),
        'from_name': 'boss',
        'project': 'peKSO3',
        'vars': json.dumps({"fn": "{}".format(var)}),
        'links': json.dumps({"url": "http://{}".format(link)}),
        'signature': '26a5a8c9fe31f28a60fa1f2558f9d8fd',
    }
    resp_datas = requests.post(url, data=data)
    print(resp_datas.json())

mail_xsend(to='fanjindong@boluome.com', subject='test',
           var='我们是boss', link='www.12306.com')


import configparser
from pprint import pprint

cf = configparser.ConfigParser()
cf.read('config.ini')
cookies = cf.items('cookies')
cookies = dict(cookies)
for item in cf:
    print(item)
# pprint(cf)

email = cf.get('info', 'email')
password = cf.get('info', 'password')

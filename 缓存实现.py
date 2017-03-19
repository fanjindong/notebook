
from expiringdict import ExpiringDict
import time
cache = ExpiringDict(max_len=100, max_age_seconds=10)

cache['key'] = 'value'
for i in range(200):
    # time.sleep(0.5)
    value = cache.get('key')
    if value:
        print(value, 'True')
    else:
        print(value, 'False')

for i in range(105):
    cache[str(i)] = i
    print(cache.get(str(i)))
    print(cache)

print(cache.get(str(100)))
# http://xiaorui.cc/2015/04/19/python-ordereddict%E5%AE%9E%E7%8E%B0%E6%9C%89expire%E5%92%8Cmax%E7%9A%84%E9%98%9F%E5%88%97%E5%92%8C%E7%BC%93%E5%AD%98%E6%9C%8D%E5%8A%A1/
# http://www.jianshu.com/p/389fa4f48be6
# https://github.com/mailgun/expiringdict/issues

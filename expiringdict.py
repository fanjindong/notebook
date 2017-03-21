import time
from collections import OrderedDict


class ExpiringDict(OrderedDict):

    def __init__(self, max_len, max_age_seconds):
        assert max_age_seconds >= 0
        assert max_len >= 1
        super(ExpiringDict, self).__init__()
        self.max_len = max_len
        self.max_age = max_age_seconds

    def __getitem__(self, key):
        """ Return the item of the dict.
        Raises a KeyError if key is not in the map.
        """
        item = OrderedDict.__getitem__(self, key)
        item_age = time.time() - item[1]
        if item_age < self.max_age:
            return item[0]
        else:
            del self[key]
            raise KeyError(key)

    def __setitem__(self, key, value):
        """ Set d[key] to value. """
        if len(self) == self.max_len:
            self.popitem(last=False)
        OrderedDict.__setitem__(self, key, (value, time.time()))

    def get(self, key, default=None,):
        " Return the value for key if key is in the dictionary, else default. "
        try:
            return self.__getitem__(key)
        except KeyError:
            return default


e = ExpiringDict(max_len=5, max_age_seconds=10)
e['name'] = 'fanjindong'
for i in range(15):
    time.sleep(1)
    # e['name'] = i
    print(e.get('name'))


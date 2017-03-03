CSRF_ENABLED = True
SECRET_KEY = "\x15E\xba\xd7\xbc'h\xe0\xb0\x93g\xd6\xdfn m\xdd@\xa1<\xa6_\xed\xf7"

OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]

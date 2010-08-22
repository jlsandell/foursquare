#!/usr/bin/env python
import common
from foursquare import FourSquare

if __name__ == '__main__':
    # replace with your email address or phone number, and
    # password.
    foursquare = FourSquare('username@example.com', 'password')

    # for debugging
    #foursquare.set_api_host('http://some.other.host')

    response = foursquare.get_userinfo(userid='REPLACE_THIS_NUMERIC_ID')
    print response.read()

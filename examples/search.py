#!/usr/bin/env python

import common
from foursquare import FourSquare

if __name__ == '__main__':
    # replace with your email address or phone number, and
    # password. You can also omit the credentials, so long as
    # you pass authenticate=False to foursquare.search()

    foursquare = FourSquare('username@example.com', 'password')

    latitude = '21.396819'
    longitude = '-157.928467'

    # foursquare defaults to 30 if no limit is passed.
    response = foursquare.search(latitude, longitude,
                                 authenticate = False, limit = 10,
                                 query = 'pizza')

    print response.read()

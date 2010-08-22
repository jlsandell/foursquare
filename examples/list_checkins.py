#!/usr/bin/env python
import common
from foursquare import FourSquare

if __name__ == '__main__':
    # replace with your email address or phone number, and
    # password.
    foursquare = FourSquare('username@example.com', 'password')

    response = foursquare.get_checkins()
    print response.read()

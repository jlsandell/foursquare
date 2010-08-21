#!/usr/bin/env python

import urllib2
import urllib
from base64 import b64encode

class FourSquare(object):
    """
    >>> foursquare = FourSquare('name@example.com', 'password')
    >>> latitude = '21.396819'
    >>> longitude = '-157.928467'
    >>> venue_id = '4760229'
    >>> response = foursquare.check_in(latitude, longitude, venue_id)

    """
    def __init__(self, username=None, password=None, ua=None):
        """
        Create a foursquare object, set username and password,
        as well as base64 encode them together for auth requests.
        """

        self.api_host = 'http://api.foursquare.com'

        if not username or not password:
            raise TypeError('username and password must be provided.')
                
        self.username = username
        self.password = password
        self.credentials = b64encode(':'.join((username, password)))

        self.headers = {
            'ua' : '''Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420 (KHTML, like Gecko) Version/3.0 Mobile/1C10 Safari/419.3+''',
            'auth': 'Basic %s' % self.credentials
        }


    def check_in(self,lat, lon, vid):
        """
        Checks in to foursquare.
        """
        host = '%s/v1/checkin.json' % self.api_host

        params = dict(
            vid = vid,
            private = 0,
            geolat = lat,
            geolong = lon,)

        post_data = urllib.urlencode(params)

        request = urllib2.Request(host, post_data)
        request.add_header('User-Agent', self.headers['ua'])
        request.add_header('Authorization', self.headers['auth'])

        response  = urllib2.urlopen(request)
        return response

    

if __name__ == '__main__':
    # Create object
    foursquare = FourSquare('username@email.com', 'password')

    # ???
    latitude = '21.396819'
    longitude = '-157.928467'
    venue_id = '4760229'
    response = foursquare.check_in(latitude, longitude, venue_id)

    # Profit!!
    print response.read()

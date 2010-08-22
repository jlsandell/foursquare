#!/usr/bin/env python
"""
    foursquare.py - a Python class library for interacting with FourSquare's
    API.

    Copyright (C) 2010 Jeremy Sandell 

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import urllib2
import urllib
from base64 import b64encode

class AuthenticationError(Exception):
    pass

class FourSquare(object):
    """
    >>> foursquare = FourSquare('name@example.com', 'password')
    >>> latitude = '21.396819'
    >>> longitude = '-157.928467'
    >>> venue_id = '4760229'
    >>> response = foursquare.checkin(latitude, longitude, venue_id)

    """

    def __init__(self, username=None, password=None, useragent=None):
        """
        Create a foursquare object, set username and password,
        as well as base64 encode them together for auth requests.
        """
        self.__api_host = 'http://api.foursquare.com'
        self.headers = {}

        if username and password:
            self.set_credentials(username, password)

        else:
            self.credentials = False

        if useragent:
            self.set_useragent(useragent)

        else:
            # Default to iPhone
            self.set_useragent('''Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) '''
            '''AppleWebKit/420 (KHTML, like Gecko) Version/3.0 '''
            '''Mobile/1C10 Safari/419.3+''')

    def set_useragent(self, useragent):
        self.headers['ua'] = useragent

    def set_credentials(self, username, password):
        self.credentials = b64encode(':'.join((username, password)))
        self.headers['auth'] = 'Basic %s' % self.credentials

    def set_api_host(self, uri):
        """
        Primarily for debugging, lets one set the base uri for
        where requests are sent.
        """
        
        self.__api_host = uri

    def _build_request(self, uri, data=None, authenticate=True):
        """
        Build an HTTP request with a given uri, and optional data.
        If data is given, it's a POST request, otherwise it's a
        GET.

        Defaults to authenticate with foursquare, but can be
        overridden by setting the keyword `authenticate` to False.

        This is useful for the few foursquare methods that don't
        require authentication, e.g., the search function.
        """

        if not data:
            # build a get request
            request = urllib2.Request(uri)
        else:
            # build a post request
            request = urllib2.Request(uri, data)

        # add user-agent and (unless overridden) basic HTTP auth
        # headers.
        request.add_header('User-Agent', self.headers['ua'])

        if authenticate:
            if not self.credentials:
                raise AuthenticationError('User credentials have not been set.')

            request.add_header('Authorization', self.headers['auth'])

        return request

    def checkin(self, latitude, longitude, vid):
        """
        Checks in to foursquare, returns a response object.
        """

        uri = '%s/v1/checkin.json' % self.__api_host

        params = dict(
            vid = vid,
            private = 0,
            geolat = latitude,
            geolong = longitude,)

        post_data = urllib.urlencode(params)

        request = self._build_request(uri, post_data) 
        response  = urllib2.urlopen(request)

        return response

    def get_checkins(self):
        """
        Get a json encoded list of check ins for the given account.

        """
        uri = '%s/v1/checkins.json' % self.__api_host

        request = self._build_request(uri)
        response = urllib2.urlopen(request)

        return response

    def get_userinfo(self, userid=None, twitter=None):
        """
        Returns user's profile, json encoded. Like the foursquare
        API it takes both userid and twitter, but will default to
        userid over the twitter handle.
        """

        if not userid and not twitter:
            raise TypeError('get_userinfo requires that you' 
                            'specify either the foursquare '
                            'userid, or their twitter handle')

        uri = '%s/v1/user.json' % self.__api_host

        if userid:
            uri = '%s?%s' % (uri, urllib.urlencode({'uid': userid}))
        else:
            uri = '%s?%s' % (uri, urllib.urlencode({'twitter': twitter}))

        request = self._build_request(uri)
        response = urllib2.urlopen(request)

        return response

    def search(self, latitude, longitude, authenticate=True, limit=None, query=None):
        """
        Search for venues near the given lat/long coordinates.
        """

        uri = '%s/v1/venues.json' % self.__api_host

        params = dict(
            geolat = latitude,
            geolong = longitude,
        )

        if limit:
            params['l'] = limit

        if query:
            params['q'] = query

        # build out the uri based on the parameters given
        uri = '%s?%s' % (uri, urllib.urlencode(params))

        request = self._build_request(uri, authenticate=authenticate)
        response = urllib2.urlopen(request)

        return response

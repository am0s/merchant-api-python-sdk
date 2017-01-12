# -*- coding: utf-8 -*-
import json

from google.appengine.api import urlfetch

from ..mapi_response import MapiResponse

__all__ = ["UrlFetchFramework"]


class UrlFetchFramework(object):
    def dispatch_request(self, method, url, body, headers, auth):
        method, url, headers, data = auth(method, url, headers, body)

        payload = {}
        if type(data) == dict:
            for key, value in data.iteritems():
                if value is not None:
                    payload.update({key: value})
            data = json.dumps(payload)

        res = urlfetch.fetch(url=url,
                             payload=data,
                             method=method,
                             deadline=60,
                             headers=headers)
        return MapiResponse(res.status_code, res.headers, res.content)

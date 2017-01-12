# -*- coding: utf-8 -*-
from ..mapi_response import MapiResponse

from ..six import binary_type

__all__ = ["RequestsFramework"]


class RequestsFramework(object):
    def dispatch_request(self, method, url, body, headers, auth, files=None):
        """
        :type auth: mcash.mapi_client.auth.AuthBase
        """
        import requests
        method, url, headers, body = auth.prepare_request(method, url, headers, body)
        res = requests.request(method,
                               url,
                               data=body,
                               headers=headers,
                               auth=auth,
                               timeout=60)
        content = res.content
        if isinstance(res.content, binary_type):
            content = res.content.decode('utf-8')
        return MapiResponse(res.status_code, res.headers, content)

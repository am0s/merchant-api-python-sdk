# coding=utf-8
from mcash.mapi_client.six import PY3
if PY3:
    import http.client as httplib
else:
    import httplib

__all__ = ['httplib']

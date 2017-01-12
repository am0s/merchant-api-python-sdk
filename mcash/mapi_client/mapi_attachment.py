# coding=utf-8
from poster.encode import MultipartParam
from poster.encode import multipart_encode

from .auth import OpenAuth
from .mapi_response import MapiResponse
from .mapi_error import MapiError


def upload_attachment(client, url, mime_type, data):
    data, headers = multipart_encode([MultipartParam('file', value=data, filename='filename', filetype=mime_type)])
    data = "".join(data)

    res = client.backend.dispatch_request(
        method='POST',
        url=url,
        body=data,
        headers=headers,
        auth=OpenAuth())

    if not isinstance(res, MapiResponse):
        res = MapiResponse(*res)

    if res.status // 100 != 2:
        raise MapiError(*res)

    return res

# -*- coding: utf-8 -*-
import base64
from time import strftime

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

from .six import binary_type

__all__ = ["OpenAuth", "SecretAuth", "RsaSha256Auth"]


class AuthBase(object):
    """Base class for authentation classes"""

    def __call__(self, req):
        return req

    def prepare_request(self, method, url, headers, body):
        return method, url, headers, body


class OpenAuth(AuthBase):
    """Attaches no authentication to the given Request object."""

    def __call__(self, req):
        return req


class SecretAuth(AuthBase):
    """Attaches Authentication with secret token to
    the given Request object."""

    def __init__(self, secret):
        self.secret = secret

    def __call__(self, req):
        req.headers['Authorization'] = 'SECRET ' + self.secret
        return req


class RsaSha256Auth(AuthBase):
    """Attaches RSA authentication to the given Request object."""

    def __init__(self, privkey):
        self.signer = PKCS1_v1_5.new(RSA.importKey(privkey))

    def __call__(self, req):
        req.headers['X-Mcash-Timestamp'] = self._get_timestamp()
        req.headers['X-Mcash-Content-Digest'] = self._get_sha256_digest(req.body or b'')
        req.headers['Authorization'] = self._sha256_sign(req.method, req.url, req.headers, req.body or b'')
        return req

    def _get_timestamp(self):
        """Return the timestamp formatted to comply with
        Merchant API expectations.
        """
        return strftime("%Y-%m-%d %H:%M:%S").encode('utf-8')

    def _get_sha256_digest(self, content):
        """Return the sha256 digest of the content in the
        header format the Merchant API expects.
        """
        content_sha256 = base64.b64encode(SHA256.new(content).digest())
        return b'SHA256=' + content_sha256

    def _sha256_sign(self, method, url, headers, body):
        """Sign the request with SHA256.
        """
        d = b''
        sign_headers = method.upper().encode('utf-8') + b'|' + url.encode('utf-8') + b'|'
        for key, value in sorted(headers.items()):
            if key.startswith('X-Mcash-'):
                if not isinstance(value, binary_type):
                    value = value.encode('utf-8')
                sign_headers += d + key.upper().encode('utf-8') + b'=' + value
                d = b'&'

        rsa_signature = base64.b64encode(
            self.signer.sign(SHA256.new(sign_headers)))

        return b'RSA-SHA256 ' + rsa_signature

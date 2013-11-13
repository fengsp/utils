# -*- coding: utf-8 -*-
"""
    signing
    ~~~~~~~

    Implementation of a simple signing.

    :copyright: (c) 2013 by fsp.
    :license: BSD.
"""
import hashlib
import hmac
import base64


try:
    import simplejson as json
except ImportError:
    import json


class Signer(object):
    """The Signer.
    """

    def __init__(self, secret_key):
        secret_key = self.want(secret_key)
        self.secret_key = secret_key
        self.seq = ':'

    def sign(self, value):
        return value + self.seq + self.get_signature(value)

    def unsign(self, signed_value):
        signed_value = self.want(signed_value)
        value, sig = signed_value.rsplit(self.seq, 1)
        if self.verify_signature(value, sig):
            return value
        return False

    # encode unicode into utf-8 string
    def want(self, value):
        if isinstance(value, unicode):
            value = value.encode('utf-8', 'strict')
        return value

    def derive_key(self):
        mac = hmac.new(self.secret_key, digestmod=hashlib.sha1)
        mac.update('SimpleSigner')
        return mac.digest()

    def get_signature(self, value, verify=None):
        value = self.want(value)
        key = self.derive_key()
        mac = hmac.new(key, msg=value, digestmod=hashlib.sha1)
        sig = mac.digest()
        if verify is None:
            return base64.urlsafe_b64encode(sig).strip(b'=')
        else:
            return sig
    
    def verify_signature(self, value, sig):
        sig = self.want(sig)
        sig = base64.urlsafe_b64decode(sig + b'=' * (-len(sig) % 4))
        # can be improved through constant time comparison
        return sig == self.get_signature(value, verify=1)

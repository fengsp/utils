# -*- coding: utf-8 -*-
"""
    Secret
    ~~~~~~

    Generate app secret.

    :copyright: (c) 2013 by fsp.
    :license: BSD.
"""
import base64, uuid


def generate_secret():
    return base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)


if __name__ == "__main__":
    print generate_secret()

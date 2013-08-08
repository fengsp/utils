#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import hashlib, random


def gamble():
    m = hashlib.md5()
    m.update(str(random.randrange(1000000)))
    r = random.randint(0, 28)
    return m.hexdigest()[r:r+4]

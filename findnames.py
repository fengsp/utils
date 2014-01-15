# -*- coding: utf-8 -*-
"""
    Find names
    ~~~~~~~~~~

    Finding objects' names

    http://pythonic.pocoo.org/2009/5/30/finding-objects-names
"""
import gc, sys


def find_names(obj):
    frame = sys._getframe()
    for frame in iter(lambda: frame.f_back, None):
        frame.f_locals
    result = []
    for referrer in gc.get_referrers(obj):
        if isinstance(referrer, dict):
            for k, v in referrer.iteritems():
                if v is obj:
                    result.append(k)
    return result


foo = []


def demo():
    bar = foo
    def inner():
        fsp = bar
        print find_names(fsp)
    return inner


demo()()

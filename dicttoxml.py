# -*- coding: utf-8 -*-
"""
    dicttoxml
    ~~~~~~~~~

    A Tool used for convert a Python dict into a XML string or file.

    :copyright: (c) 2013 by fsp.
    :license: BSD.
"""
import os


try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

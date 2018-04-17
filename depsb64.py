#!/usr/bin/env python3.6
# -*- encoding: utf-8 -*-

import base64


def decode_base64(data):
    missing_padding = len(data) % 4
    if missing_padding != 0:
        data += b'=' * (4 - missing_padding)
    return base64.decodebytes(data)

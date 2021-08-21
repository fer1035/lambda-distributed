#!/usr/bin/env python3
# -*- coding: latin-1 -*-
"""
Process data one-by-one.

Usage: python3 <script_file.py> data_file
"""
import sys
import requests
import json
from multiprocessing import Pool


def post(
    data: str
) -> str:
    """
    Post data to API.

    return str
    """
    response = requests.post(
        '<API_endpoint_URL>',
        headers={
            'x-api-key': '<API_key>'
        },
        data=(
            '{{"data": "{}"}}'
            .format(data.replace('\n', ''))
        )
    )
    print(json.loads(response.text)['message'])
    return json.loads(response.text)['message']


if __name__ == "__main__":

    with open(sys.argv[1], 'r') as f:
        data_list = f.readlines()

    for data in data_list:
        response = post(data)

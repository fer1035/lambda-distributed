#!/usr/bin/env python3
"""
Process data in parallel.

Usage: python3 <script_file.py> number_of_processes data_file
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

    with open(sys.argv[2], 'r') as f:
        data_list = f.readlines()

    # available methods:
    # map, map_async, imap, imap_unordered, apply, apply_async
    p = Pool(int(sys.argv[1]))
    results = p.imap_unordered(
        post,
        data_list
    )
    p.close()
    p.join()

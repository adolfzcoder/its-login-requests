"""
Example of payload
    # payload = {
    # "numtype": "S",
    # "unum": 224037928,  #Student number
    # "pin": 123452, # Pin for KIOSK
    # "authorise_function": "Login"
    # }

"""

import requests
from credentials import unum, pin
from Payload import Payload
from flask import jsonify
url = "https://ienabler.nust.na/pls/prodi41/w99pkg.mi_validate_user"

def login(data: Payload):
    # payload = {
    # "numtype": "S",
    # "unum": unum,
    # "pin": pin,
    # "authorise_function": "Login"
    # }


    payload = {
    "numtype":data.accType,
    "unum":data.number,
    "pin":data.pin
    }
    

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    with requests.Session() as session:
        response = session.post(url, data=payload, headers=headers)
        # print("Status code:", response.status_code)
        # print("Response URL:", response.url)
        # print("Response text snippet:", response.text[:500])

    if response.status_code == 200:

        return True, "Login Succesful"
    else:
        return False, "Invalid credentials"


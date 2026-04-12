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
#url = "https://ienabler.nust.na/pls/prodi41/w99pkg.mi_validate_user"
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
    "pin":data.pin,
    "authorise_function":"Login"
    }
    

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0",
        "Referer": "https://ienabler.nust.na/pls/prodi41/w99pkg.mi_login"
    }

    with requests.Session() as session:
        response = session.post(url, data=payload, headers=headers)
        # print("Status code:", response.status_code)
        # print("Response URL:", response.url)
        # print("Response text snippet:", response.text[:500])

    if response.status_code == 200:
        # Check if the response contains the encrypted checksum (indicator of successful login)
        if "encrypted checksum:" in response.text:
            return True, "Login Successful", "Valid credentials - Session created", response.status_code, response.text, response.url
        else:
            # Login failed, contains "Illegal Login" or "A Value Error Occurred"
            return False, "Invalid credentials", "Login rejected by server", response.status_code, response.text, response.url
    else:
        return False, "Invalid credentials", response.reason, response.status_code, response.text, response.url


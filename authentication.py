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
import re
from credentials import unum, pin
from Payload import Payload
from flask import jsonify
#url = "https://ienabler.nust.na/pls/prodi41/w99pkg.mi_validate_user"
url = "https://ienabler.nust.na/pls/prodi41/w99pkg.mi_validate_user"


def extract_student_name(html: str):
    # Expected pattern in the frame: <tr><th colspan="2">SURNAME, NAME</th></tr>
    match = re.search(r'<tr><th\s+colspan="2">\s*([^<]+?)\s*</th></tr>', html, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None


def extract_sessid(html: str):
    # Session id is embedded in login response HTML and normally set by JS in browser.
    checksum_match = re.search(r'encrypted checksum:\s*([A-F0-9]{32,128})', html, re.IGNORECASE)
    if checksum_match:
        return checksum_match.group(1)

    js_cookie_match = re.search(r'JsCreate_Cookie\("([A-F0-9]{32,128})"\s*,\s*"sessid"\)', html, re.IGNORECASE)
    if js_cookie_match:
        return js_cookie_match.group(1)

    return None

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
                sessid = extract_sessid(response.text)
                if sessid:
                    session.cookies.set("sessid", sessid, domain="ienabler.nust.na", path="/")

                # Login successful, fetch the main menu page first
                menu_url = "https://ienabler.nust.na/pls/prodi41/w99pkg.mi_main_menu"
                menu_response = session.get(menu_url, allow_redirects=True)
                
                # Now fetch the iframe content with proper referer
                frame_main_url = "https://ienabler.nust.na/pls/prodi41/w99pkg.mi_frame_main"
                frame_headers = {
                    "Referer": menu_url,
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Sec-Fetch-Dest": "iframe",
                    "Sec-Fetch-Mode": "navigate",
                    "Sec-Fetch-Site": "same-origin",
                    "Upgrade-Insecure-Requests": "1"
                }
                frame_main_response = session.get(frame_main_url, headers=frame_headers, allow_redirects=True)

                frame_html = frame_main_response.text
                student_name = extract_student_name(frame_html)

                # Return structured result for easier API consumption.
                result = {
                    "student_name": student_name
                }
                return True, "Login Successful", "Valid credentials - Session created", response.status_code, result, frame_main_response.url
            else:
                # Login failed, contains "Illegal Login" or "A Value Error Occurred"
                return False, "Invalid credentials", "Login rejected by server", response.status_code, response.text, response.url
        else:
            return False, "Invalid credentials", response.reason, response.status_code, response.text, response.url


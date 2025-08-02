import requests
from credentials import unum, pin
import Payload 
url = "https://ienabler.nust.na/pls/prodi41/w99pkg.mi_validate_user"

def login(accountType, user_number, pin, authorise_function):
    # payload = {
    # "numtype": "S",
    # "unum": unum,
    # "pin": pin,
    # "authorise_function": "Login"
    # }
    payload = Payload(accountType, user_number, pin, authorise_function) 

    

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    with requests.Session() as session:
        response = session.post(url, data=payload, headers=headers)
        print("Status code:", response.status_code)
        print("Response URL:", response.url)
        print("Response text snippet:", response.text[:500])

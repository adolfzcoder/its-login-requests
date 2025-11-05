
"""
http://127.0.0.1:5000/api/v1/login
{
    "numtype": "S",
    "unum": "224XXXXXX",
    "pin": "XXXXX"
}

"""
import requests
from flask import Flask, request, jsonify
import authentication
from Payload import Payload
from credentials import unum, pin


app = Flask(__name__)

@app.route('/api/v1/login', methods=['POST'])
def sign_in():
    data = request.get_json()

    numtype = data.get("numtype")
    user_number = data.get("unum")
    pin = data.get("pin")
    

    signin_data = Payload(numtype, user_number, pin)
    success, message, reason, res_code, raw, url  = authentication.login(signin_data)
    if success:
        return jsonify({"message": message, "reason": reason}), 200
    else:
        return jsonify({
            "message": message,
            "reason": reason, 
            "res_code": res_code, 
            "raw": raw.text if hasattr(raw, "text") else str(raw),
            "url": str(url) 
            }), 401
    


def main():
    print("App Starting now...")    
# accountType, user_number, pin, authorise_function

if __name__ == "__main__":
    main()
    app.run(debug=True, port=9090)
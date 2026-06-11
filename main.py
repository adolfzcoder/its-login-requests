
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
from flask_cors import CORS
from Student import Student
import authentication
from Payload import Payload
from credentials import unum, pin
from get_results import get_results


app = Flask(__name__)
CORS(app)


@app.route('/api/v2/login', methods=['POST'])
def sign_in():
    data = request.get_json(silent=True) or request.form.to_dict() or {}

    numtype = data.get("numtype")
    user_number = data.get("unum")
    pin = data.get("pin")

    if not numtype or not user_number or not pin:
        return jsonify({
            "message": "Missing required fields",
            "reason": "Expected numtype, unum, and pin",
            "res_code": 400
        }), 400
    

    signin_data = Payload(numtype, user_number, pin)
    success, message, reason, res_code, page_data, url = authentication.login(signin_data)
    if success:
        student_name = page_data.get("student_name") if isinstance(page_data, dict) else None
        return jsonify({
            "message": message,
            "reason": reason,
            "res_code": res_code,
            "student_name": student_name
        }), 200
    else:
        if res_code == 503:
            status_code = 503
        elif res_code and int(res_code) >= 500:
            status_code = 502
        else:
            status_code = 401
        return jsonify({
            "message": message,
            "reason": reason, 
            "res_code": res_code, 
            "url": str(url) 
            }), status_code
    
@app.route('/api/v2/results', methods=['POST'])
def results():
    data = request.get_json(silent=True) or request.form.to_dict() or {}

    numtype = data.get("numtype")
    user_number = data.get("unum")
    pin = data.get("pin")

    if not numtype or not user_number or not pin:
        return jsonify({
            "message": "Missing required fields",
            "reason": "Expected numtype, unum, and pin",
            "res_code": 400
        }), 400
    

    signin_data = Payload(numtype, user_number, pin)
    success, message, reason, res_code, page_data, url = authentication.login(signin_data)
    if success:
        
        student_name = page_data.get("student_name") if isinstance(page_data, dict) else None
        student = Student(student_name, user_number)
        results = get_results(student, page_data.get("frame_html") if isinstance(page_data, dict) else None)

        return jsonify({
            "message": message,
            "reason": reason,
            "res_code": res_code,
            "student_name": student.name,
            "student_number": student.student_number,
            "page_url": str(url),
            "results": results.to_dict()
        }), 200
    else:
        if res_code == 503:
            status_code = 503
        elif res_code and int(res_code) >= 500:
            status_code = 502
        else:
            status_code = 401
        return jsonify({
            "message": message,
            "reason": reason, 
            "res_code": res_code, 
            "url": str(url) 
            }), status_code
    

def main():
    print("App Starting now...")    
# accountType, user_number, pin, authorise_function

if __name__ == "__main__":
    main()
    app.run(debug=True, port=9090)
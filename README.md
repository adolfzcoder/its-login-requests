# its-login-requests

Use this API to validate login credentials if your're making a NUST app or UNAM app. If it uses ITS-KIOSK then use this API

## Run

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Start server:

```bash
python main.py 
```

Server runs on `http://localhost:9090`.

## Endpoint
You may now call the api
- Method: `POST`
- URL: `http://localhost:9090/api/v2/login`
- Content-Type: `application/json`

## Request Body

```json
{
  "numtype": "S",
  "unum": "224091778",
  "pin": "12345"
}
```
```
numtype --> user type student or staff or alumni
num --> student number
pin --> kiosk 5 digit login pin
```
## Success Response (200)

```json
{
  "message": "Login Successful",
  "reason": "Valid credentials - Session created",
  "res_code": 200,
  "student_name": "SURNAME, NAME"
}
```

## Failure Response (401)

```json
{
  "message": "Invalid credentials",
  "reason": "Login rejected by server",
  "res_code": 200,
  "url": "https://ienabler.nust.na/pls/prodi41/w99pkg.mi_validate_user"
}
```

Notes:

- ITS can return HTTP `200` even for invalid login content; this API checks page content to decide success/failure.
- `res_code` is the upstream ITS response code.

## Quick Test (curl)

```bash
curl -X POST http://localhost:9090/api/v2/login \
  -H "Content-Type: application/json" \
  -d '{"numtype":"S","unum":"2240XXXXX","pin":"12345"}'
```


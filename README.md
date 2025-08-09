# its-login-requests
Use this API to validate login credentials if your're making a NUST app or UNAM app. If it uses ITS-KIOSK then use this API


# How the Request looks like

## End point : /api/v1/login
### POST
   Body:
`
{
    "numtype": "S", 
    "unum": "2240XXXXX",
    "pin": "XXXXX"
}
`
numtype --> user type, student or staff or alumni
unum --> student number
pin --> kiosk 5 digit login pin


   

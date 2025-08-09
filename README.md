# its-login-requests
Use this API to validate login credentials if your're making a NUST app or UNAM app. If it uses ITS-KIOSK then use this API

#

## Start the flask server with ```python main.py``` (its port 9090 by default)
### After starting, you may call the api 



# How the Request looks like

## End point : /api/v1/login ```http://localhost:9090/api/v1/login```
### POST
   Body:
```
{
    "numtype": "S", 
    "unum": "2240XXXXX",
    "pin": "XXXXX"
}
```
# 
```
numtype --> user type student or staff or alumni
num --> student number
pin --> kiosk 5 digit login pin
```

   

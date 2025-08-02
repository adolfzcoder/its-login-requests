
"""
  # payload = {
    # "numtype": "S",
    # "unum": unum,
    # "pin": pin,
    # "authorise_function": "Login"
    # }
"""
import authentication
from credentials import unum, pin
def main():
    authentication.login("S", unum, pin, "Login")
    
# accountType, user_number, pin, authorise_function

if __name__ == "__main__":
    main()
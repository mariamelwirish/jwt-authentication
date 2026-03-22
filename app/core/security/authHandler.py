import jwt
from decouple import config
import time

JWT_SECRET = config('JWT_SECRET')
JWT_ALGORITHM = config('JWT_ALGORITHM')

class AuthHandler(object):

    @staticmethod
    def sign_jwt(user_id : int):
        payload = {
            'user_id' : user_id,
            'expires' : time.time() + 900
        }

        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return token
    
    @staticmethod
    # return payload if token is valid, else return None
    def decode_jwt(token : str):
        try:
            decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            if decoded_token['expires'] >= time.time():
                return decoded_token
            else:
                return None
        except:
            print("Unable to decode token")
            return None
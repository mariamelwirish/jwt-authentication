from bcrypt import hashpw, gensalt, checkpw

class HashHelper(object):

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

    @staticmethod
    def hash_password(plain_password: str) -> str:
        return hashpw(plain_password.encode('utf-8'), gensalt()).decode('utf-8')

     
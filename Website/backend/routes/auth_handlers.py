import jwt
import datetime
import bcrypt

from db.services import get_user_by_id

SECRET_KEY = 'RouteOptimization-secret'

def generate_jwt_token(user_id):
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),  # Token expiration time
            'iat': datetime.datetime.utcnow(),  # Token issuance time
            'sub': user_id,  # Subject (typically user ID)
        }
        # Encode the payload with the secret key
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return token
    except Exception as e:
        return str(e)

def get_user_by_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user = get_user_by_id(payload['sub'])
        return user
    except Exception as e:
        return str(e)


salt = bcrypt.gensalt()

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

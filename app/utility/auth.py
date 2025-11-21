from datetime import datetime, timedelta, timezone
from jose import jwt
import jose
from functools import wraps
from flask import request, jsonify

SECRET_KEY = "supersecretkey"

def encode_token(mechanic_id):
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days=0, hours=1), # Set token expiration.Token expires in 1 hour
        'iat': datetime.now(timezone.utc),  # Issued at time
        'sub': str(mechanic_id), #VERY IMPORTANT, SET YOUR USER ID TO A STRING
        
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def token_required(f): #f stands for the function that is getting wrapped. Delete user function from routes is f. 
    @wraps(f)
    def decoration(*args, **kwargs): #The function that runs before the function that we're wrapping  
        
        token = None
        
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1] #Bearer <token> 
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            print(data)
            request.logged_in_mechanic_id = data['sub'] #Attach the user id to the request object for use in the route. adding another attribute to the request object called logged_in_user_id
        except jose.exceptions.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 403
        except jose.exceptions.JWTError:
            return jsonify({'message': 'Token is invalid!'}), 401
        
        return f(*args, **kwargs)
    
    return decoration
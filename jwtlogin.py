#For prototypes we can use werkzeug.security for production we should use bcrypt or argon2
from flask import Flask, request, jsonify
import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
SECRET_KEY = "mysecretkey"

# In-memory "database" for users
users_db = {}

# Generate JWT token
def generate_jwt(payload, expires_in_minutes=30):
    payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(minutes=expires_in_minutes)
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# Verify JWT token
def verify_jwt(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# Register API
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Username and password required"}), 400

    if username in users_db:
        return jsonify({"message": "User already exists"}), 400

    # Hash the password before storing
    hashed_password = generate_password_hash(password)
    users_db[username] = {"password": hashed_password}

    return jsonify({"message": "User registered successfully"}), 201

# Login API
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = users_db.get(username)
    if not user or not check_password_hash(user["password"], password):
        return jsonify({"message": "Invalid credentials"}), 401

    token = generate_jwt({"user": username})
    return jsonify({"token": token})

# Protected API
@app.route("/protected", methods=["GET"])
def protected():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "Token is missing"}), 401

    # If token is prefixed with "Bearer "
    if token.startswith("Bearer "):
        token = token[7:]

    decoded = verify_jwt(token)
    if not decoded:
        return jsonify({"message": "Invalid or expired token"}), 401

    return jsonify({"message": f"Welcome {decoded['user']}!"})

if __name__ == "__main__":
    app.run(debug=True)

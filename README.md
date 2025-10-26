Flask is the core class of the Flask framework.
You use it to create a web application instance.
request is an object that gives you all the data sent by a client (like a browser, Postman, or other apps).
jsonify is a helper function to send JSON responses to the client.
generate_password_hash : This function takes a plain text password and converts it into a hashed version.
check_password_hash : This function checks whether a plain text password matches a hashed password.
1. Register a user: POST /register with JSON:

{
  "username": "alice",
  "password": "mypassword"
}

2. Login: POST /login with JSON:

{
  "username": "alice",
  "password": "mypassword"
}

Returns a JWT token.

3. Access protected route: GET /protected with Header:

Authorization: Bearer <your_jwt_token>

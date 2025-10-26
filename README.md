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

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from db import get_db_connection

# Define blueprint for authentication-related routes
auth_bp = Blueprint('auth', __name__)

# Login API
@auth_bp.route('/login', methods=['POST'])
def login():
    """
    API to handle user login. Returns a JWT token if credentials are valid.
    """
    data = request.json
    username = data.get('username')  # Get username from request
    password = data.get('password')  # Get password from request

    print(f"Debug: Username received: {username}, Password received: {password}")

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = "SELECT id, username, password_hash, role FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()

        print(f"Debug: Fetched user from database: {user}")

        if user and user['password_hash'] == password:  # Compare plaintext password
            # Generate JWT token
            access_token = create_access_token(identity={'id': user['id'], 'role': user['role']})
            return jsonify({'access_token': access_token}), 200
        else:
            return jsonify({'message': 'Invalid username or password'}), 401
    finally:
        cursor.close()
        conn.close()

# Register API
@auth_bp.route('/register', methods=['POST'])
@jwt_required()  # Require JWT token for authentication
def register():
    """
    API to register a new user. Only accessible by admins.
    """
    # Get current user identity
    current_user = get_jwt_identity()

    # Check if the current user has admin privileges
    if current_user['role'] != 'admin':
        return jsonify({'message': 'Access denied: Admin privileges required'}), 403

    # Get request data
    data = request.json
    username = data.get('username')  # Get new username
    password = data.get('password')  # Get new password
    role = data.get('role', 'user')  # Default to 'user' if no role is provided

    # Validate required fields
    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Check if the username already exists
        query = "SELECT id FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        if cursor.fetchone():
            return jsonify({'message': 'Username already exists'}), 400

        # Insert the new user into the database
        query = "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, password, role))
        conn.commit()

        return jsonify({'message': 'User registered successfully!'}), 201
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500
    finally:
        cursor.close()
        conn.close()

from flask import Blueprint, jsonify
from db import get_db_connection
import pymysql

roles_bp = Blueprint('roles', __name__)

# Get all roles
@roles_bp.route('/', methods=['GET'])
def get_roles():
    """Fetch all roles from the database."""
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute("SELECT * FROM roles")
        roles = cursor.fetchall()
        return jsonify(roles)  # Return the list of roles as JSON
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

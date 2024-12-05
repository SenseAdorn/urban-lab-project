from flask import Blueprint, request, jsonify
from db import get_db_connection
import pymysql

contacts_bp = Blueprint('contacts', __name__)

@contacts_bp.route('/', methods=['GET'])
def get_contacts():
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    # Join contacts with roles to include role_name
    query = """
        SELECT 
            contacts.id, 
            contacts.first_name, 
            contacts.last_name, 
            contacts.email, 
            contacts.phone, 
            contacts.role_id, 
            roles.role_name, 
            contacts.organization, 
            contacts.city, 
            contacts.country, 
            contacts.notes
        FROM contacts
        LEFT JOIN roles ON contacts.role_id = roles.id
    """
    cursor.execute(query)
    contacts = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(contacts)

def get_all_contacts():
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        query = "SELECT * FROM contacts"
        cursor.execute(query)
        contacts = cursor.fetchall()  # 获取所有contacts数据
        return jsonify(contacts)  # 返回JSON格式数据
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@contacts_bp.route('/<int:id>', methods=['GET'])
def get_contact_by_id(id):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM contacts WHERE id = %s", (id,))
    contact = cursor.fetchone()
    cursor.close()
    conn.close()
    if contact:
        return jsonify(contact)
    else:
        return jsonify({'message': 'Contact not found'}), 404

@contacts_bp.route('/', methods=['POST'])
def add_contact():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """
        INSERT INTO contacts (first_name, last_name, email, phone, role_id, organization, city, country, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        data['first_name'],
        data['last_name'],
        data['email'],
        data.get('phone'),
        data.get('role_id'),
        data.get('organization'),
        data.get('city'),
        data.get('country'),
        data.get('notes')
    )
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Contact added successfully!'}), 201

@contacts_bp.route('/<int:id>', methods=['PUT'])
def update_contact(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """
        UPDATE contacts
        SET first_name = %s, last_name = %s, email = %s, phone = %s, role_id = %s,
            organization = %s, city = %s, country = %s, notes = %s
        WHERE id = %s
    """
    values = (
        data['first_name'],
        data['last_name'],
        data['email'],
        data.get('phone'),
        data.get('role_id'),
        data.get('organization'),
        data.get('city'),
        data.get('country'),
        data.get('notes'),
        id
    )
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()
    if cursor.rowcount > 0:
        return jsonify({'message': 'Contact updated successfully!'})
    else:
        return jsonify({'message': 'Contact not found'}), 404

@contacts_bp.route('/<int:id>', methods=['DELETE'])
def delete_contact(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contacts WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    if cursor.rowcount > 0:
        return jsonify({'message': 'Contact deleted successfully!'})
    else:
        return jsonify({'message': 'Contact not found'}), 404

@contacts_bp.route('/role-count', methods=['GET'])
def get_contact_role_count():
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        query = """
        SELECT roles.role_name, COUNT(*) AS contact_count
        FROM contacts
        JOIN roles ON contacts.role_id = roles.id
        GROUP BY roles.role_name
        """
        cursor.execute(query)
        role_counts = cursor.fetchall()
        return jsonify(role_counts)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@contacts_bp.route('/filter-by-role', methods=['GET'])
def get_contacts_by_role():
    role_id = request.args.get('role_id')
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        query = """
        SELECT * FROM contacts
        WHERE role_id = %s
        """
        cursor.execute(query, (role_id,))
        contacts = cursor.fetchall()
        return jsonify(contacts)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@contacts_bp.route('/roles/', methods=['GET'])
def get_roles():
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM roles")
    roles = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(roles)


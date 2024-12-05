from flask import Blueprint, request, jsonify
from db import get_db_connection
import pymysql
import pandas as pd

# Define Blueprint
grants_bp = Blueprint('grants', __name__)

# Add a new grant
@grants_bp.route('/', methods=['POST'])
def add_grant():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO grants (grant_name, purpose, amount, frequency, start_date, end_date)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (
            data['grant_name'],
            data['purpose'],
            data['amount'],
            data['frequency'],
            data['start_date'],
            data.get('end_date')  # Nullable
        )
        cursor.execute(query, values)
        conn.commit()
        return jsonify({'message': 'Grant added successfully!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Update an existing grant
@grants_bp.route('/<int:id>', methods=['PUT'])
def update_grant(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        UPDATE grants
        SET grant_name = %s, purpose = %s, amount = %s, frequency = %s, 
            start_date = %s, end_date = %s
        WHERE id = %s
        """
        values = (
            data['grant_name'],
            data['purpose'],
            data['amount'],
            data['frequency'],
            data['start_date'],
            data.get('end_date'),  # Nullable
            id
        )
        cursor.execute(query, values)
        conn.commit()
        if cursor.rowcount > 0:
            return jsonify({'message': 'Grant updated successfully!'})
        else:
            return jsonify({'message': 'Grant not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Delete a grant
@grants_bp.route('/<int:id>', methods=['DELETE'])
def delete_grant(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = "DELETE FROM grants WHERE id = %s"
        cursor.execute(query, (id,))
        conn.commit()
        if cursor.rowcount > 0:
            return jsonify({'message': 'Grant deleted successfully!'})
        else:
            return jsonify({'message': 'Grant not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Get all grants
@grants_bp.route('/', methods=['GET'])
def get_all_grants():
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        query = """
        SELECT 
            id, 
            grant_name, 
            purpose, 
            amount, 
            frequency, 
            DATE_FORMAT(start_date, '%Y-%m-%d') as start_date, 
            DATE_FORMAT(end_date, '%Y-%m-%d') as end_date
        FROM grants
        """
        cursor.execute(query)
        grants = cursor.fetchall()
        return jsonify(grants)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Get a specific grant by ID
@grants_bp.route('/<int:id>', methods=['GET'])
def get_grant_by_id(id):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        query = "SELECT * FROM grants WHERE id = %s"
        cursor.execute(query, (id,))
        grant = cursor.fetchone()
        if grant:
            return jsonify(grant)
        else:
            return jsonify({'message': 'Grant not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Filter grants by date range
@grants_bp.route('/filter-by-date', methods=['GET'])
def filter_grants_by_date():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        query = """
        SELECT * FROM grants
        WHERE start_date >= %s AND (end_date <= %s OR end_date IS NULL)
        """
        cursor.execute(query, (start_date, end_date))
        grants = cursor.fetchall()
        return jsonify(grants)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Filter grants by frequency
@grants_bp.route('/filter-by-frequency', methods=['GET'])
def filter_grants_by_frequency():
    frequency = request.args.get('frequency')
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        query = "SELECT * FROM grants WHERE frequency = %s"
        cursor.execute(query, (frequency,))
        grants = cursor.fetchall()
        return jsonify(grants)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Export grants to Excel
@grants_bp.route('/export', methods=['GET'])
def export_grants_to_excel():
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        query = "SELECT * FROM grants"
        cursor.execute(query)
        grants = cursor.fetchall()
        # Convert to DataFrame
        df = pd.DataFrame(grants)
        file_path = 'exported_grants.xlsx'
        df.to_excel(file_path, index=False)
        return jsonify({'message': f'Data exported to {file_path}'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@grants_bp.route('/grant_frequency_distribution', methods=['GET'])
def get_grant_frequency_distribution():
    # 连接到数据库
    conn = mysql.connector.connect(**DATABASE_CONFIG)
    cursor = conn.cursor(dictionary=True)

    # 执行查询
    cursor.execute("""
        SELECT frequency, COUNT(*) AS count
        FROM grants
        GROUP BY frequency
    """)

    # 获取结果
    result = cursor.fetchall()

    # 关闭连接
    cursor.close()
    conn.close()

    # 返回结果
    return jsonify(result)

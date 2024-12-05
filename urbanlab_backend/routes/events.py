from flask import Blueprint, request, jsonify
from db import get_db_connection
import pymysql
import pandas as pd

events_bp = Blueprint('events', __name__)

@events_bp.route('/', methods=['GET'])
def get_events():
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT id, event_name, DATE_FORMAT(event_date, '%Y-%m-%d') as event_date, location, event_type, content FROM events")
    events = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(events)

def get_all_events():
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        query = "SELECT * FROM events"
        cursor.execute(query)
        events = cursor.fetchall()  # 获取所有events数据
        return jsonify(events)  # 返回JSON格式数据
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@events_bp.route('/<int:id>', methods=['GET'])
def get_event_by_id(id):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM events WHERE id = %s", (id,))
    event = cursor.fetchone()
    cursor.close()
    conn.close()
    if event:
        return jsonify(event)
    else:
        return jsonify({'message': 'Event not found'}), 404

@events_bp.route('/', methods=['POST'])
def add_event():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """
        INSERT INTO events (event_name, event_date, location, event_type, content)
        VALUES (%s, %s, %s, %s, %s)
    """
    values = (
        data['event_name'],
        data['event_date'],
        data.get('location'),
        data.get('event_type'),
        data.get('content')
    )
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Event added successfully!'}), 201

@events_bp.route('/<int:id>', methods=['PUT'])
def update_event(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """
        UPDATE events
        SET event_name = %s, event_date = %s, location = %s, event_type = %s, content = %s
        WHERE id = %s
    """
    values = (
        data['event_name'],
        data['event_date'],
        data.get('location'),
        data.get('event_type'),
        data.get('content'),
        id
    )
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()
    if cursor.rowcount > 0:
        return jsonify({'message': 'Event updated successfully!'})
    else:
        return jsonify({'message': 'Event not found'}), 404

@events_bp.route('/<int:id>', methods=['DELETE'])
def delete_event(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM events WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    if cursor.rowcount > 0:
        return jsonify({'message': 'Event deleted successfully!'})
    else:
        return jsonify({'message': 'Event not found'}), 404

@events_bp.route('/monthly-count', methods=['GET'])
def get_monthly_event_count():
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        query = """
        SELECT MONTH(event_date) AS month, COUNT(*) AS event_count
        FROM events
        GROUP BY MONTH(event_date)
        ORDER BY MONTH(event_date)
        """
        cursor.execute(query)
        monthly_counts = cursor.fetchall()
        return jsonify(monthly_counts)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@events_bp.route('/date-range', methods=['GET'])
def get_events_by_date_range():
    start_date = request.args.get('start_date')  # 获取查询参数
    end_date = request.args.get('end_date')
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        query = """
        SELECT * FROM events
        WHERE event_date BETWEEN %s AND %s
        """
        cursor.execute(query, (start_date, end_date))
        events = cursor.fetchall()
        return jsonify(events)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

import pandas as pd

@events_bp.route('/export', methods=['GET'])
def export_events_to_excel():
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        query = "SELECT * FROM events"
        cursor.execute(query)
        events = cursor.fetchall()
        # 转换为 DataFrame
        df = pd.DataFrame(events)
        file_path = 'exported_events.xlsx'
        # 导出为 Excel
        df.to_excel(file_path, index=False)
        return jsonify({'message': f'Data exported to {file_path}'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

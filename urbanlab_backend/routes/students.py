from flask import Blueprint, request, jsonify
from db import get_db_connection
import pymysql

students_bp = Blueprint('students', __name__)

@students_bp.route('/', methods=['GET'])
def get_students():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)  # Initialize the cursor
        cursor.execute("SELECT * FROM students")  # Execute the query
        students = cursor.fetchall()  # Fetch all results
        return jsonify(students)  # Return results as JSON
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Ensure cursor is closed if it was created
        if cursor:
            cursor.close()
        # Ensure connection is closed if it was created
        if conn:
            conn.close()



@students_bp.route('/', methods=['POST'])
def add_student():
    conn = None
    cursor = None
    try:
        data = request.json  # 获取请求中的 JSON 数据
        conn = get_db_connection()
        cursor = conn.cursor()
        # 插入学生数据的 SQL 语句
        sql = """
            INSERT INTO students (first_name, last_name, email, phone, course, city, country, student_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        # 提取 JSON 数据中的字段
        values = (
            data['first_name'],
            data['last_name'],
            data['email'],
            data.get('phone'),
            data.get('course'),
            data.get('city'),
            data.get('country'),
            data['student_type']
        )
        cursor.execute(sql, values)
        conn.commit()
        return jsonify({'message': 'Student added successfully!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@students_bp.route('/<int:id>', methods=['GET'])
def get_student_by_id(id):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # 查询特定学生的 SQL 语句
        cursor.execute("SELECT * FROM students WHERE id = %s", (id,))
        student = cursor.fetchone()
        if student:
            return jsonify(student)
        else:
            return jsonify({'message': 'Student not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@students_bp.route('/<int:id>', methods=['DELETE'])
def delete_student(id):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # 删除学生的 SQL 语句
        cursor.execute("DELETE FROM students WHERE id = %s", (id,))
        conn.commit()
        if cursor.rowcount > 0:
            return jsonify({'message': 'Student deleted successfully!'})
        else:
            return jsonify({'message': 'Student not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@students_bp.route('/<int:id>', methods=['PUT'])
def update_student(id):
    conn = None
    cursor = None
    try:
        data = request.json  # 获取请求中的 JSON 数据
        conn = get_db_connection()
        cursor = conn.cursor()
        # 更新学生信息的 SQL 语句
        sql = """
            UPDATE students
            SET first_name = %s, last_name = %s, email = %s, phone = %s,
                course = %s, city = %s, country = %s, student_type = %s
            WHERE id = %s
        """
        values = (
            data['first_name'],
            data['last_name'],
            data['email'],
            data.get('phone'),
            data.get('course'),
            data.get('city'),
            data.get('country'),
            data['student_type'],
            id
        )
        cursor.execute(sql, values)
        conn.commit()
        if cursor.rowcount > 0:
            return jsonify({'message': 'Student updated successfully!'})
        else:
            return jsonify({'message': 'Student not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@students_bp.route('/statistics', methods=['GET'])
def get_student_statistics():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # 查询 current 学生数量
        cursor.execute("SELECT COUNT(*) FROM students WHERE student_type = 'Current'")
        current_count = cursor.fetchone()[0]

        # 查询 alumni 学生数量
        cursor.execute("SELECT COUNT(*) FROM students WHERE student_type = 'Alumni'")
        alumni_count = cursor.fetchone()[0]

        return jsonify({
            "current_students": current_count,
            "alumni_students": alumni_count
        })
    except Exception as e:
        print("Error occurred:", str(e))  # 在服务器端控制台中查看错误详情
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
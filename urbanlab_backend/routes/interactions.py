from flask import Blueprint, request, jsonify
from db import get_db_connection
import pymysql

interactions_bp = Blueprint('interactions', __name__)

@interactions_bp.route('/activity-participants/<int:event_id>', methods=['GET'])
def get_activity_participants(event_id):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        # Query to fetch all participants for a given event
        query = """
        SELECT
            students.first_name AS student_name,
            students.email AS student_email,
            contacts.first_name AS contact_name,
            contacts.email AS contact_email
        FROM interactions
        LEFT JOIN students ON interactions.student_id = students.id
        LEFT JOIN contacts ON interactions.contact_id = contacts.id
        WHERE interactions.event_id = %s
        """
        cursor.execute(query, (event_id,))
        participants = cursor.fetchall()
        return jsonify(participants)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@interactions_bp.route('/role-activity/<int:role_id>', methods=['GET'])
def get_role_based_activities(role_id):
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        # Query to fetch activities for a specific role
        query = """
        SELECT
            events.event_name,
            events.event_date,
            contacts.first_name AS contact_name,
            contacts.email AS contact_email
        FROM interactions
        LEFT JOIN events ON interactions.event_id = events.id
        LEFT JOIN contacts ON interactions.contact_id = contacts.id
        WHERE contacts.role_id = %s
        """
        cursor.execute(query, (role_id,))
        role_activities = cursor.fetchall()
        return jsonify(role_activities)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@interactions_bp.route('/', methods=['POST'])
def add_interaction():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Insert interaction record
        query = """
        INSERT INTO interactions (student_id, contact_id, event_id, interaction_type_id, notes)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (
            data.get('student_id'),       # Nullable: Interaction may involve either student or contact
            data.get('contact_id'),       # Nullable
            data['event_id'],             # Required
            data.get('interaction_type_id'), # Nullable
            data.get('notes')             # Optional notes
        )
        cursor.execute(query, values)
        conn.commit()
        return jsonify({'message': 'Interaction added successfully!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@interactions_bp.route('/<int:id>', methods=['PUT'])
def update_interaction(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Update interaction record
        query = """
        UPDATE interactions
        SET student_id = %s, contact_id = %s, event_id = %s,
            interaction_type_id = %s, notes = %s
        WHERE id = %s
        """
        values = (
            data.get('student_id'),       # Nullable
            data.get('contact_id'),       # Nullable
            data['event_id'],             # Required
            data.get('interaction_type_id'), # Nullable
            data.get('notes'),            # Optional notes
            id
        )
        cursor.execute(query, values)
        conn.commit()
        if cursor.rowcount > 0:
            return jsonify({'message': 'Interaction updated successfully!'})
        else:
            return jsonify({'message': 'Interaction not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@interactions_bp.route('/<int:id>', methods=['DELETE'])
def delete_interaction(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Delete interaction record
        query = "DELETE FROM interactions WHERE id = %s"
        cursor.execute(query, (id,))
        conn.commit()
        if cursor.rowcount > 0:
            return jsonify({'message': 'Interaction deleted successfully!'})
        else:
            return jsonify({'message': 'Interaction not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@interactions_bp.route('/', methods=['GET'])
def get_interactions():
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        # Fetch all interaction records
        query = """
        SELECT interactions.id, students.first_name AS student_name,
               contacts.first_name AS contact_name, events.event_name,
               interaction_types.type_name AS interaction_type,
               interactions.notes, interactions.created_at
        FROM interactions
        LEFT JOIN students ON interactions.student_id = students.id
        LEFT JOIN contacts ON interactions.contact_id = contacts.id
        LEFT JOIN events ON interactions.event_id = events.id
        LEFT JOIN interaction_types ON interactions.interaction_type_id = interaction_types.id
        """
        cursor.execute(query)
        interactions = cursor.fetchall()
        return jsonify(interactions)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()


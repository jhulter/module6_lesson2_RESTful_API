import marshmallow
import flask_marshmallow
from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
import mysql.connector
from mysql.connector import Error
from marshmallow import fields, ValidationError

def get_db_connection():
    # Database connection parameters
    db_name = "gym"
    user = "root"
    password = "Theezfoot7!"
    host = "127.0.0.1"

    try:
        # Attempt to establish a connection
        conn = mysql.connector.connect(
            database=db_name,
            user=user,
            password=password,
            host=host
        )
        # Check if connection is successful
        if conn.is_connected():
            print("Connected to MySQL Database successful.")
            return conn

    except Error as e:
        # Handling any connection errors
        print(f"Error: {e}")

app = Flask(__name__)
ma = Marshmallow(app)

class MemberSchema(ma.Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    age = fields.Integer(required=True)

    class Meta:
        fields = ("id", "name", "age")

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)

class WorkoutSchema(ma.Schema):
    member_id = fields.Integer(required=True)
    session_id = fields.Integer(required=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Integer(required=True)
    calories_burned = fields.Integer(required=True)
    
    class Meta:
        fields = ("member_id", "session_id", "date", "duration_minutes", "calories_burned")

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

@app.route('/workoutsessions', methods=["GET"])
def get_workouts():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM workoutsessions"

        cursor.execute(query)

        workouts = cursor.fetchall()

        return workouts_schema.jsonify(workouts)
    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/workoutsessions', methods=['POST'])
def add_workout_session():
    try:
        workout_data = workout_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)

        new_workout = (workout_data['member_id'], workout_data['session_id'], workout_data['date'], workout_data['duration_minutes'], workout_data['calories_burned'])

        query = "INSERT INTO workoutsessions (member_id, session_id, date, duration_minutes, calories_burned) VALUES (%s, %s, %s, %s, %s)"

        cursor.execute(query, new_workout)

        conn.commit()

        return jsonify({"message": "New workout added successfully"}), 201

    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/workoutsessions/<int:id>', methods=['PUT'])
def update_workout(id):
    try:
        workout_data = workout_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)

        updated_workout = (workout_data['member_id'], workout_data['date'], workout_data['duration_minutes'], workout_data['calories_burned'], (session_id,))

        query = "UPDATE workoutsessions SET member_id = %s, date = %s, duration_minutes = %s, calories_burned = %s WHERE session_id = %s)"

        cursor.execute(query, updated_workout)

        conn.commit()

        return jsonify({"message": "Workout updated successfully"}), 201

    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/workoutsessions/<int:id>', methods=['DELETE'])
def delete_workout(id):

    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)

        workout_to_delete = (id,)

        cursor.execute("SELECT * FROM workoutsessions WHERE session_id = %s", workout_to_delete)

        member = cursor.fetchone()

        if not member:
            return jsonify({"Error": "Workout not found"}), 404
        
        query = "DELETE FROM workoutsessions WHERE id = %s"

        cursor.execute(query, workout_to_delete)
        
        conn.commit()

        return jsonify({"message": "Workout removed successfully"}), 201

    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/workoutsessions/<int:id>', methods=["GET"])
def get_member(id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM workoutsessoins WHERE id = %s", (id,))

        workout = cursor.fetchone()

        if workout:
            return workout_schema.jsonify(workout)
        else:
            return jsonify({"error": "member not found"})
        
    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/')
def home():
    return 'Welcome Home'

@app.route('/members', methods=["GET"])
def get_members():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM Members"

        cursor.execute(query)

        members = cursor.fetchall()

        return members_schema.jsonify(members)
    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/members', methods=['POST'])
def add_member():
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)

        new_member = (member_data['id'], member_data['name'], member_data['age'])

        query = "INSERT INTO members (id, name, age) VALUES (%s, %s, %s)"

        cursor.execute(query, new_member)

        conn.commit()

        return jsonify({"message": "New member added successfully"}), 201

    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)

        updated_member = (member_data['name'], member_data['age'], member_data['id'], id)

        query = "UPDATE members SET id = %s, name = %s, age = %s WHERE id = %s)"

        cursor.execute(query, updated_member)

        conn.commit()

        return jsonify({"message": "Member updated successfully"}), 201

    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):

    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)

        member_to_delete = (id,)

        cursor.execute("SELECT * FROM Members WHERE id = %s", member_to_delete)

        member = cursor.fetchone()

        if not member:
            return jsonify({"Error": "Member not found"}), 404
        
        query = "DELETE FROM Members WHERE id = %s"

        cursor.execute(query, member_to_delete)
        
        conn.commit()

        return jsonify({"message": "Customer removed successfully"}), 201

    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/members/<int:id>', methods=["GET"])
def get_member(id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM Members WHERE id = %s", (id,))

        member = cursor.fetchone()

        if member:
            return member_schema.jsonify(member)
        else:
            return jsonify({"error": "member not found"})
        
    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()



if __name__ == '__main__':
    app.run(debug=True)

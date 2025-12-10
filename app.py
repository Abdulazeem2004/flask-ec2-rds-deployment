from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
import mysql.connector
app = Flask(__name__)
CORS(app)   # allow frontend to call backend from any domain
def get_db():
    return mysql.connector.connect(
     host="mydb.c3208wyo6crt.af-south-1.rds.amazonaws.com",
     user="admin",
     password="Adenekan44",
     database="mydatabase"
    )
# Home route to serve HTML page
@app.route("/")
def home():
    return send_from_directory(".", "index.html")

# API endpoint to interact with frontend
@app.route("/api/hello", methods=["POST"])
def api_hello():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    if not name or not email or not message:
       return jsonify({"message": "All fields are required"}), 400
    conn = get_db()
    cursor = conn.cursor()

    sql = "INSERT INTO contact_messages (name, email, message) VALUES (%s, %s, %s)"
    cursor.execute(sql, (name, email, message))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Message saved successfully!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

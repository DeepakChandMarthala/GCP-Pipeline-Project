from flask import Flask, request, render_template
import MySQLdb

app = Flask(__name__, template_folder="frontend")  # Specify 'frontend' as template folder

# Configurations for Cloud SQL
app.config['MYSQL_HOST'] = '35.193.246.77'  # Replace with your Cloud SQL public IP
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'ica'

# Initialize MySQL connection
db = MySQLdb.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB']
)

@app.route('/')
def index():
    return render_template('index.html')  # Serve the frontend HTML form

@app.route('/add', methods=['POST'])
def add_entry():
    # Get form values
    value1 = request.form.get('value1')
    value2 = request.form.get('value2')

    cursor = db.cursor()
    try:
        # Insert data into the database
        query = "INSERT INTO entries (value1, value2) VALUES (%s, %s)"
        cursor.execute(query, (value1, value2))
        db.commit()
        return f"Data inserted successfully: Value1 = {value1}, Value2 = {value2}"
    except Exception as e:
        db.rollback()
        return f"Error: {str(e)}"
    finally:
        cursor.close()

@app.route('/entries', methods=['GET'])
def get_entries():
    cursor = db.cursor()
    try:
        # Fetch all data from the database
        query = "SELECT * FROM entries"
        cursor.execute(query)
        rows = cursor.fetchall()
        result = [{'id': row[0], 'value1': row[1], 'value2': row[2]} for row in rows]
        return {"entries": result}
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

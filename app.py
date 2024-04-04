from flask import Flask, request, jsonify
import mysql.connector
import sendEmail

app = Flask(__name__)
lambda_function_name = 'emailSenderLambdaFunction'

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'kapoor123',
    'database': 'jira'
}

# Function to connect to the database
def connect_to_db():
    return mysql.connector.connect(**db_config)

@app.route('/')
def hello():
    return ("Jell-o World!")

# Create Issue endpoint
@app.route('/create', methods=['POST'])
def create_issue():
    # Parse request data
    data = request.json

    assignee_email = data['assignee']
    assigner_email = data['assigner']
    status = "Open"
    date = data['date']
    title = data['title']

    # Connect to the database
    conn = connect_to_db()
    cursor = conn.cursor()

    # Insert data into Issue table
    try:
        cursor.execute("INSERT INTO Issue (assignee, assigner, status, date, title) VALUES (%s, %s, %s, %s, %s)",
                       (assignee_email, assigner_email, status, date, title))
        conn.commit()
        return jsonify({'message': 'Issue created successfully'}), 200
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        payload = {
            'Subject': 'Issue Created!',
            'Body': 'Hello! A new issue has been created for you.'
        }
        print("Sending Email!")
        sendEmail.invoke_lambda_function(lambda_function_name, payload)
        cursor.close()
        conn.close()

@app.route('/edit/<int:issue_id>', methods=['POST'])
def edit_issue(issue_id):
    data = request.json

    assignee_email = data['assignee']
    status = data['status']
    date = data['date']

    # Connect to the database
    conn = connect_to_db()
    cursor = conn.cursor()

    # Update data into Issue table
    try:
        cursor.execute("UPDATE Issue SET assignee = %s, status = %s, date = %s WHERE issue_id = %s",
                       (assignee_email, status, date, issue_id))
        conn.commit()
        return jsonify({'message': f'Issue #{issue_id} edited successfully'}), 200
    
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        payload = {
            'Subject': 'Issue Edited!',
            'Body': f'Issue #{issue_id} edited successfully.'
        }
        sendEmail.invoke_lambda_function(lambda_function_name, payload)
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(port=8080)

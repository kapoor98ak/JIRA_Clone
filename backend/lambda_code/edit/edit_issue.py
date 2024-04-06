from flask import Flask, request, jsonify, render_template
import mysql.connector
import boto3
import json

app = Flask(__name__)
lambda_function_name = 'emailSenderLambdaFunction'


@app.route('/')
def home():
    return render_template('issue_management.html')


@app.route('/edit/<int:issue_id>', methods=['POST'])
def edit_issue(issue_id):
    print("edit_issue")
    data = request.json


    assignee_email = data['assignee']
    status = data['status']
    date = data['date']
    title = data['title']

    # Connect to the database
    conn = connect_to_db()
    cursor = conn.cursor()

    # Update data into Issue table
    try:
        cursor.execute("USE JIRA")
        cursor.execute("UPDATE Issue SET assignee = %s, status = %s, date = %s, title = %s WHERE issue_id = %s",
                       (assignee_email, status, date, title, issue_id))
        conn.commit()
        return jsonify({'message': f'Issue #{issue_id} edited successfully'}), 200
    
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        payload = {
            'Subject': 'Issue Edited!',
            'Body': f'Issue #{issue_id} edited successfully.'
        }
        print("Sending Email!")

        invoke_lambda_function(lambda_function_name, payload)
        
        cursor.close()
        conn.close()


#  Common Code for Both Lambdas
def getSecretCred():
    print("getSecretCred")
    region_name = 'us-east-1'
    client = boto3.client('secretsmanager', region_name=region_name)
    response = client.get_secret_value(
        SecretId='arn:aws:secretsmanager:us-east-1:851725512559:secret:MyRDSCredentials-1-jB69vE'
    )
    return response

def connect_to_db():
    print("connecting to db")
    response_data = getSecretCred()
    db_config = {}

    # db_config['host'] = os.environ['RDSSecret_ARN']

    db_config['host'] = 'mydbinstance-2107-1.cjs42euouytr.us-east-1.rds.amazonaws.com'
    db_config['user'] = json.loads(response_data['SecretString'])['username']
    db_config['password'] = json.loads(response_data['SecretString'])['password']

    return mysql.connector.connect(**db_config)


def invoke_lambda_function(function_name, payload):
    
    region_name = 'us-east-1'
    lambda_client = boto3.client('lambda', region_name=region_name)
    
    payload_bytes = json.dumps(payload).encode('utf-8')

    try:
        print("Invoking Lambda!")
        response = lambda_client.invoke(
            FunctionName=function_name,
            InvocationType='RequestResponse', 
            Payload=payload_bytes
        )
        return response
    except Exception as e:
        print(f"Error invoking Lambda function: {e}")

def execute_SQL_RDS(SQL_Path):
    with open(SQL_Path) as SQL:
        SQL_Script = SQL.read()

    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        # Split the SQL script into individual statements
        statements = SQL_Script.split(';')

        for statement in statements:
            # Skip empty statements
            if not statement.strip():
                continue

            print(statement)
            cursor.execute(statement.strip())  # Execute each statement

        conn.commit()  # Commit the transaction on the connection

        return 'SQL Run successfully'
    except mysql.connector.Error as err:
        return 'Error'
    finally:
        cursor.close()  # Close cursor
        conn.close()    # Close connection

def setup_RDS():
    print("setup_RDS")

    print(execute_SQL_RDS('sql-scripts/create-database.sql'))
    print(execute_SQL_RDS('sql-scripts/create-table.sql'))
    print(execute_SQL_RDS('sql-scripts/insert-data.sql'))



# if __name__ == '__main__':
#     # execute_SQL_RDS('sql-scripts/delete-database.sql')
#     app.run(port=8081)
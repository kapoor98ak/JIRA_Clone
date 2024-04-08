from venv import logger
# from flask import Flask, request, jsonify, render_template
import mysql.connector
import boto3
import json
import os

lambda_function_name = 'emailSenderLambdaFunction'


#  Common Code for Both Lambdas
def getSecretCred():
    print("getSecretCred")
    region_name = 'us-east-1'
    client = boto3.client('secretsmanager', region_name=region_name)
    response = client.get_secret_value(
            # SecretId='arn:aws:secretsmanager:us-east-1:851725512559:secret:MyRDSCredentials-1-jB69vE'
            SecretId= os.environ['RDSSecret_ARN']
    )
    return response

def connect_to_db():
    print("connecting to db")
    response_data = getSecretCred()
    db_config = {}

    # db_config['host'] = 'mydbinstance-2107-1.cjs42euouytr.us-east-1.rds.amazonaws.com'
    
    db_config['host'] = os.environ['RDSInstance']
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



def lambda_handler(event, context):
    try:
        print("Event:", event)
        # print("issue_id:", event.get('issue_id'))
        # print("assignee:", event.get('assignee'))
        # print("status:", event.get('status'))
        # print("date:", event.get('date'))
        # print("title:", event.get('title'))
        
        body = event['body']
        body_json = json.loads(body)
        
        issue_id = body_json['issue_id']
        assignee_email = body_json['assignee']
        status = body_json['status']
        date = body_json['date']
        title = body_json['title']
        
        print("Trying to connect:")

        # Connect to the database
        conn = connect_to_db()
        print("Connection Successful!")
        cursor = conn.cursor()

        # Update data into Issue table
        try:
            # Execute SQL query to check for existing tables in the 'JIRA' schema
            cursor.execute("SELECT TABLE_NAME FROM information_schema.tables WHERE TABLE_SCHEMA = 'JIRA' AND TABLE_TYPE = 'BASE TABLE'")
            tables = cursor.fetchall()
            existing_tables = [table[0] for table in tables]

            if existing_tables:
                print("Tables found...")
                print("Existing tables in 'JIRA' schema:", existing_tables)
            else:
                print("No tables found in 'JIRA' schema")
                return jsonify({'message': f'Issue #{issue_id} not found!'}), 200

            cursor.execute("USE JIRA")
            cursor.execute("UPDATE Issue SET assignee = %s, status = %s, date = %s, title = %s WHERE issue_id = %s",
                        (assignee_email, status, date, title, issue_id))
            conn.commit()
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Issue Edited successfully'}),
                'headers': {
                    'Content-Type': 'application/json'
                },
            }
        
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

    except Exception as e:
        logger.error(f"Failed to create issue: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error'}),
            'headers': {
                'Content-Type': 'application/json'
            },
        }
    

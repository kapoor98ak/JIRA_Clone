import boto3
import os
import mysql.connector
import json

db_config = {}

def getSecretCred():
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(
        SecretId='arn:aws:secretsmanager:us-east-1:851725512559:secret:MyRDSCredentials-1-9wPKec'
    )
    return response

def connect_to_db():
    return mysql.connector.connect(**db_config)

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

            cursor.execute(statement.strip())  # Execute each statement

        conn.commit()  # Commit the transaction on the connection

        return 'SQL Run successfully'
    except mysql.connector.Error as err:
        return 'Error'
    finally:
        cursor.close()  # Close cursor
        conn.close()    # Close connection

if __name__ == "__main__":
    response_data = getSecretCred()

    db_config['host'] = 'mydbinstance-2107-1.cjs42euouytr.us-east-1.rds.amazonaws.com'
    # db_config['host'] = os.environ['RDSSecret_ARN']
    db_config['user'] = json.loads(response_data['SecretString'])['username']
    db_config['password'] = json.loads(response_data['SecretString'])['password']
    
    # execute_SQL_RDS('cloud-project/sql-scripts/create-database.sql')
    # execute_SQL_RDS('cloud-project/sql-scripts/create-table.sql')
    execute_SQL_RDS('cloud-project/sql-scripts/insert-data.sql')
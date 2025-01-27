import boto3
import os
import mysql.connector
import json

db_config = {}

def getSecretCred():
    region_name = 'us-east-1'
    client = boto3.client('secretsmanager', region_name=region_name)
    response = client.get_secret_value(
        SecretId='arn:aws:secretsmanager:us-east-1:851725512559:secret:MyRDSCredentials-1-Ta5ebx'
    )
    return response

def connect_to_db():
    response_data = getSecretCred()

    
    # db_config['host'] = os.environ['RDSSecret_ARN']
    db_config['host'] = 'mydbinstance-2107-1.cjs42euouytr.us-east-1.rds.amazonaws.com'

    db_config['user'] = json.loads(response_data['SecretString'])['username']
    # db_config['user'] = 'admin'
    
    db_config['password'] = json.loads(response_data['SecretString'])['password']
    # db_config['password'] = '{0<=D1oNw3Cfu:+q'
    
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

def setup_RDS():
    print(execute_SQL_RDS('sql-scripts/create-database.sql'))
    print(execute_SQL_RDS('sql-scripts/create-table.sql'))
    print(execute_SQL_RDS('sql-scripts/insert-data.sql'))
    # print(execute_SQL_RDS(os.path.join(os.pardir, 'sql-scripts', 'create-database.sql')))
    # print(execute_SQL_RDS(os.path.join(os.pardir, 'sql-scripts', 'create-table.sql')))
    # print(execute_SQL_RDS(os.path.join(os.pardir, 'sql-scripts', 'insert-data.sql')))


if __name__ == '__main__':
    setup_RDS()

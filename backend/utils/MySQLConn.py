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
    response_data = getSecretCred()

    db_config['host'] = 'mydbinstance-2107-1.cjs42euouytr.us-east-1.rds.amazonaws.com'
    # db_config['host'] = os.environ['RDSSecret_ARN']
    db_config['user'] = json.loads(response_data['SecretString'])['username']
    db_config['password'] = json.loads(response_data['SecretString'])['password']
    
    return mysql.connector.connect(**db_config)

# if __name__ == "__main__":

    # execute_SQL_RDS('cloud-project/sql-scripts/create-database.sql')
    # execute_SQL_RDS('cloud-project/sql-scripts/create-table.sql')
    # execute_SQL_RDS('cloud-project/sql-scripts/insert-data.sql')
import boto3
import json

lambda_client = boto3.client('lambda')

def invoke_lambda_function(function_name, payload):
    # This is an important step!!!
    
    payload_bytes = json.dumps(payload).encode('utf-8')

    try:
        print("Invoking Lambda!")
        response = lambda_client.invoke(
            FunctionName=function_name,
            InvocationType='RequestResponse',  # Can be 'Event' for asynchronous invocation
            Payload=payload_bytes
        )
        return response
    except Exception as e:
        print(f"Error invoking Lambda function: {e}")

if __name__ == "__main__":
    
    # Put the Lambda Function's Name here!!

    # function_name = 'test-lambda'
    function_name = 'emailSenderLambdaFunction'
    
    payload = {
        'Subject': 'EMail Subject 1',
        'Body': 'EMail Body 2'
    }
    
    # Invoke the Lambda function
    response = invoke_lambda_function(function_name, payload)
    
    # Print the response
    print(response)
import json
import boto3
import os

def send_email_via_sns(topic_arn, subject, message):
    
    sns = boto3.client('sns')

    # Publish a message to the topic
    response = sns.publish(
        TopicArn=topic_arn,
        Subject=subject,
        Message=message
    )

    return response

def lambda_handler(event, context):
    # Extracting 'Subject' and 'Body' from the event
    subject = event.get('Subject', 'Default Subject')
    body = event.get('Body', 'Default Body')
    
    # Example usage
    # topic_arn = 'arn:aws:sns:us-east-1:851725512559:test-sns'
    topic_arn = os.environ['SNS_TOPIC_ARN']

    try:
        response = send_email_via_sns(topic_arn, subject, body)
        print("Email sent! Message ID:", response['MessageId'])
        return {
            'statusCode': 200,
            'body': 'Email sent successfully!'
        }
    except Exception as e:
        print("Failed to send email:", e)
        return {
            'statusCode': 500,
            'body': 'Failed to send email.'
        }

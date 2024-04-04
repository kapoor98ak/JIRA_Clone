import boto3

client = boto3.client('sns')

def create_SNS_Subscription(topic_arn, subscriber_email):
    try:
        print("Invoking Topic Subscription Creation!")

        response = client.subscribe(
            TopicArn=topic_arn,
            Protocol='email',
            Endpoint=subscriber_email,
            ReturnSubscriptionArn=True
        )   
        return response    
    except Exception as e:
        print(f"Error invoking Lambda function: {e}")
    


if __name__ == "__main__":
    response = create_SNS_Subscription('arn:aws:sns:us-east-1:851725512559:test-sns-topic-issue', 'abhisheklatawa1103@gmail.com')
    print(response)



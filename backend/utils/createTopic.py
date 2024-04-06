import boto3

region_name = 'us-east-1'
client = boto3.client('sns', region_name = region_name)

def create_SNS_Topic(issue_identifier):
    try:
        print("Invoking Topic Creation!")

        response = client.create_topic(
        Name=f'Topic-{issue_identifier}',
        Attributes={
            'FifoTopic': 'false',
            }
        )   
        return response    
    except Exception as e:
        print(f"Error invoking Lambda function: {e}")
    


if __name__ == "__main__":
    response = create_SNS_Topic('test-issue')
    print(response)



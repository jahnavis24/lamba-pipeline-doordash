import json
import boto3
import pandas as pd
import os
from io import StringIO

s3 = boto3.client('s3')
sns = boto3.client('sns')

# SNS topic ARN
SNS_TOPIC_ARN = 'YOUR-SNS_TOPIC_ARN'

def lambda_handler(event, context):
    try:
        # 1. Get uploaded S3 file info
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']

        # 2. Read the file content
        obj = s3.get_object(Bucket=bucket_name, Key=key)
        data = obj['Body'].read().decode('utf-8')
        json_data = [json.loads(line) for line in data.strip().splitlines()]

        # 3. Convert to DataFrame
        df = pd.DataFrame(json_data)

        # 4. Filter delivered orders
        df_delivered = df[df['status'] == 'delivered']

        # 5. Save filtered data as JSON string
        filtered_json = df_delivered.to_json(orient='records', indent=2)
        output_key = key.replace('landing', 'target')

        # 6. Upload to target bucket
        s3.put_object(
            Bucket='class3-assign-doordash-target-zn',
            Key=output_key,
            Body=filtered_json
        )

        # 7. Send SNS notification
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=f"File {key} processed successfully. Delivered orders uploaded to target bucket.",
            Subject="Lambda Processing Success"
        )

        return {
            'statusCode': 200,
            'body': f'Successfully processed and filtered: {key}'
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        raise e

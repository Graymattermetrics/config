import json
import yaml

def lambda_handler(event, context):
    with open('./config.yaml') as f:
        config = yaml.safe_load(f)

    return {
        'statusCode': 200,
        'body': json.dumps(config),
        'headers': {
            'Access-Control-Allow-Headers' : 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
    }

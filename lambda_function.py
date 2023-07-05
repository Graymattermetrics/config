import json
import yaml
import requests

def lambda_handler(event, context):
    with open('./config.yaml') as f:
        config = yaml.safe_load(f)


    request = requests.get("https://api.github.com/repos/graymattermetrics/config/branches/main")
    config['version'] = request.json()['commit']['sha']

    return {
        'statusCode': 200,
        'body': json.dumps(config),
        'headers': {
            'Access-Control-Allow-Headers' : 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
    }

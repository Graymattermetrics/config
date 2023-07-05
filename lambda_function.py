import json
import yaml
import requests


def lambda_handler(event, context):
    """
    Takes in optional paramater version from the queryStringParameters
    which is a git commit sha. If no version is provided, the latest commit from main
    is used.
    """
    version = event['queryStringParameters'].get('version', None)
    if version is None:
        request = requests.get("https://api.github.com/repos/graymattermetrics/config/branches/main")
        version = request.json()['commit']['sha']

    content = requests.get(f"https://raw.githubusercontent.com/graymattermetrics/config/{version}/config.yaml")
    config = yaml.safe_load(content)
    config['version'] = version

    return {
        'statusCode': 200,
        'body': json.dumps(config),
        'headers': {
            'Access-Control-Allow-Headers' : 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
    }

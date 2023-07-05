import json
import yaml
import requests


def lambda_handler(event, context):
    """
    Takes in optional paramater version from the queryStringParameters
    which is a git commit sha. If no version is provided, you can provide a 
    branch name and it will return the latest commit sha for that branch.
    Defaults to main.
    """
    version = (event['queryStringParameters'] or {}).get('version', None)
    if version is None:
        branch = (event['queryStringParameters'] or {}).get('branch', 'main')
        request = requests.get(f"https://api.github.com/repos/graymattermetrics/config/branches/{branch}")
        version = request.json()['commit']['sha']

    request = requests.get(f"https://raw.githubusercontent.com/graymattermetrics/config/{version}/config.yaml")
    config = yaml.safe_load(request.content)
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

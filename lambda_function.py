import json
import yaml
import requests


def count_keys(data: dict) -> int:
    """
    Uses iteration to count the length of each
    dictionary and sub-dictionary
    """
    t = len(data)
    for value in data.values():
        if isinstance(value, dict):
            t += count_keys(value)
    return t


def get_main_keys() -> dict:
    """
    Returns the length of the keys in the 
    main branch (which is associated to the
    actual cogspeed algorithm)
    """
    request = requests.get("https://raw.githubusercontent.com/Graymattermetrics/config/main/config.yaml")
    return yaml.safe_load(request.content)

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

    # Minus one because its the 'version' key
    if count_keys(config) - 1 < count_keys(get_main_keys()):
        reason = (
            "Error: the number of keys in the config is less than "
            "the number of keys in the main branch"
        )
        config = {'error': True, 'reason': reason}

    return {
        'statusCode': 200,
        'body': json.dumps(config),
        'headers': {
            'Access-Control-Allow-Headers' : 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
    }

if __name__ == "__main__":
    print(lambda_handler({
        "queryStringParameters": {"branch": "test-broken-version"}
    },{}))
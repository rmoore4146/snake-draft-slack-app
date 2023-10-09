import base64
import urllib
import draft_creator
import boto3
import threading

from boto3.dynamodb.conditions import Key


def send_text_response(event):
    print("Messaging Slack...")
    SLACK_URL = "https://slack.com/api/chat.postMessage"
    msg_map = dict(urllib.parse.parse_qsl(
        base64.b64decode(str(event['body'])).decode('ascii')))  # data comes b64 and also urlencoded name=value& pairs
    print(msg_map)
    channel = msg_map.get('channel_id', 'err')
    params = msg_map.get('text', 'err')
    parsed_params = parse_params(params)
    response_string = 'Usage: /snake-draft [# rounds] [... draftees]'
    if parse_params is not None:
        response_string = draft_creator.generate_draft(parsed_params[1], parsed_params[0])
    print(response_string)
    team_id = msg_map["team_id"]
    bot_token = get_token_for_team(team_id)
    print('token: %s' % bot_token)
    data = urllib.parse.urlencode({
        "channel": channel,
        "text": response_string,
        "user": msg_map['user_name'],
        "link_names": True
    })
    data = data.encode("ascii")
    request = urllib.request.Request(SLACK_URL, data=data, method="POST")
    request.add_header("Content-Type", "application/x-www-form-urlencoded")
    request.add_header("Authorization", "Bearer %s" % bot_token)
    res = urllib.request.urlopen(request).read()
    print('res: %s' % res)


def parse_params(args):
    split_args = args.split(" ")
    if len(args) < 3:
        return None
    else:
        draftees = []
        for non_rounds_arg_index in range(1, len(split_args)):
            draftees.append(split_args[non_rounds_arg_index])
        return int(split_args[0]), draftees


def lambda_handler(event, context):
    print(f"Received event:\n{event}\nWith context:\n{context}")
    send_text_response(event)
    return {
        'statusCode': 200,
    }


def get_token_for_team(team):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('token')
    response = table.get_item(
        Key={
            'team_id': team
        }
    )
    return response['Item']["token"]

import os
from slackclient import SlackClient


BOT_NAME = 'prometheus'

slack_client = SlackClient(os.environ.get('SLACKBOT_TOKEN'))

print('test')
#if __name__ == "__main__":
api_call = slack_client.api_call("users.list")
print('test2')
if api_call.get('ok'):
    # retrieve all users so we can find our bot
    users = api_call.get('members')
    print(users)
    for user in users:
        if 'name' in user and user.get('name') == BOT_NAME:
            print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
else:
    print('API call failed')

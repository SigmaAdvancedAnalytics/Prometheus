import logging
import os
import time
import traceback
import subprocess

# pip install slackclient
from slackclient import SlackClient

SLACK_BOT_NAME = 'prometheus'
SLACK_CHANNEL = 'test'
SLACKBOT_TOKEN = os.environ.get('SLACKBOT_TOKEN')
ADMIN_MODE = False

#retrieve SLACK_BOT_ID and SLACK_BOT_MENTION as this is unqiue per team
slack_client = SlackClient(SLACKBOT_TOKEN)
api_call = slack_client.api_call("users.list")
if api_call.get('ok'):
    # retrieve all users so we can find our bot
    users = api_call.get('members')
    for user in users:
        if 'name' in user and user.get('name') == SLACK_BOT_NAME.lower():
            SLACK_BOT_ID = user.get('id')
            SLACK_BOT_MENTION = '<@%s>' % SLACK_BOT_ID
else:
            print("api-call failed for token " + SLACKBOT_TOKEN)

#begin slackbot helper functions
def send_message(text):
    slack_client.rtm_send_message(channel=SLACK_CHANNEL, message=text)


def process_terminal_cmd(cmd):
    cmd = cmd.strip()
    if cmd.startswith('deactivate admin'):
        ADMIN_MODE = False
        send_message("*!!!ADMIN MODE DEACTIVATED!!!*)
    else:
        cmd = cmd.split(' ')
        send_message("_Executing.._")
        cmd_output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
        send_message("_Output:_\n{}".format(cmd_output.decode()))

def process_deploy(cmd, event):
    pass

def process_help(*args):
    pass

def process_event(event):
    # filter out slack events that are not for us
    text = event.get('text')
    if text is None:
        return

    # make sure our bot is only called for a specified channel
    channel = event.get('channel')
    if channel is None:
        return
    if channel != slack_client.server.channels.find(SLACK_CHANNEL).id:
        slack_client.rtm_send_message(channel = channel, message ='<@{user}> I only run tasks asked from `{channel}` channel'.format(user=event['user'],
                                                                                                                                    channel=SLACK_CHANNEL))
        return

    # remove bot name and extract command
    if text.startswith(SLACK_BOT_MENTION):
        cmd = text.split('%s' % SLACK_BOT_MENTION)[1]
        cmd = cmd.strip()
    else:
        cmd = text.split('%s ' % SLACK_BOT_NAME)[1]

    # process command
    try:
        if ADMIN_MODE:
            process_terminal_cmd(cmd)
        elif cmd.startswith('activate admin'):
            send_message("*!!!ADMIN MODE ACTIVATED!!!*)
        elif cmd.startswith('deploy'):
            process_deploy(cmd, event)
        else:
            send_message("*I don't know how to do that*: `%s`" % cmd)
    except:
        send_message("*I don't know how to do that*: `%s`" % cmd)


def process_events(events):
    for event in events:
        try:
            process_event(event)
        except Exception as e:
            logging.exception(e)
            msg = '%s: %s\n%s' % (e.__class__.__name__, e, traceback.format_exc())
            send_message(msg)


def main():
    if slack_client.rtm_connect():
        send_message('_starting..._')

        # --
        # Here is a good place to init git repositories if needed, in order to provide git-based features:
        # - list of commits to deploy
        # - history of deployments
        # - status of deployed services vs what's available in git

        send_message("*All right, I'm ready, ask me anything!*")

        while True:
            events = slack_client.rtm_read()
            if events:
                logging.info(events)
            process_events(events)
            time.sleep(0.1)
    else:
        logging.error('Connection Failed, invalid token?')


if __name__ == '__main__':
    main()

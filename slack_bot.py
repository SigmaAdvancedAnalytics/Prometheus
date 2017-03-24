import time
import os
from slackclient import SlackClient
import subprocess

BOT_TOKEN = os.environ['SLACKBOT_TOKEN']
CHANNEL_NAME = "test"

def main():
    # Create the slackclient instance
    sc = SlackClient(BOT_TOKEN)

    # Connect to slack
    if sc.rtm_connect():
        # Send first message
        sc.rtm_send_message(CHANNEL_NAME, "I'm ALIVE!!!")

        while True:
            # Read latest messages
            for slack_message in sc.rtm_read():
                message = slack_message.get("text")
                user = slack_message.get("user")
                if not message or not user:
                    continue
                if message == "You'll be sentient one day":
                    sc.rtm_send_message(CHANNEL_NAME, "Thanks <@{}> I hope so".format(user))
                    continue
                #command parsing
                try:
                    cmd = subprocess.run(message, shell=True, stdout=subprocess.PIPE)
                    sc.rtm_send_message(CHANNEL_NAME, "{}".format(cmd.stdout.decode('utf-8')))
                except:
                    sc.rtm_send_message(CHANNEL_NAME, "Sorry! I don't understand: {}".format(message))
                    pass
            # Sleep for half a second
            time.sleep(0.2)

if __name__ == '__main__':
    main()
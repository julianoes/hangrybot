#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import time
import re
import schedule
from random import randint
from slackclient import SlackClient
from menucrawler import CoronaCrawler, BackmarktCrawler


class HangryBot(object):
    RTM_READ_DELAY = 1  # 1 second delay between reading from RTM
    EXAMPLE_COMMAND = "do"
    MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

    def __init__(self):
        self.slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
        self.legacy_token = os.environ.get('SLACK_LEGACY_TOKEN')
        self.starterbot_id = None

    def run(self):
        if not self.slack_client.rtm_connect(with_team_state=False):
            print("Connection failed. Exception traceback printed above.")

        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        self.starterbot_id = \
            self.slack_client.api_call("auth.test")["user_id"]

        schedule.every().day.at("11:30").do(self.daily_message)

        while True:
            command, channel = self.parse_bot_commands(
                self.slack_client.rtm_read())
            if command:
                self.handle_command(command, channel)
            schedule.run_pending()
            time.sleep(self.RTM_READ_DELAY)

    def daily_message(self, channel="#lunch"):
        """Print the menus and create a poll."""
        cc = CoronaCrawler()
        text = "*Corona:*\n```"
        text += cc.get_menus()
        text += "```"
        self.slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=text
        )
        bc = BackmarktCrawler()
        text = "*Backmarkt:*\n```"
        text += bc.get_menus()
        text += "```"
        self.slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=text
        )
        text = '"Where do we go?" "Corona" "Backmarkt" "Thai"'
        command = '/poll'
        self.slack_client.api_call(
            "chat.command",
            token=self.legacy_token,
            channel=channel,
            command=command,
            text=text
        )

    def parse_bot_commands(self, slack_events):
        """Parses a list of events from the RTM API to find bot commands.

        If a bot command is found, this function returns a tuple of
        command and channel.
        If its not found, then this function returns None, None.
        """
        for event in slack_events:
            if event["type"] == "message" and "subtype" not in event:
                user_id, message = self.parse_direct_mention(event["text"])
                if user_id == self.starterbot_id:
                    return message, event["channel"]
        return None, None

    def parse_direct_mention(self, message_text):
        """Finds a direct mention in message text and returns the user ID.

        Returns the which was mentioned.
        If there is no direct mention, returns None
        """
        matches = re.search(self.MENTION_REGEX, message_text)
        # the first group contains the username,
        # the second group contains the remaining message.
        return (matches.group(1), matches.group(2).strip()) \
            if matches else (None, None)

    def handle_command(self, command, channel):
        """Executes bot command if the command is known."""
        if command == "Corona?":
            cc = CoronaCrawler()
            text = "*Corona:*\n```"
            text += cc.get_menus()
            text += "```"
            self.slack_client.api_call(
                "chat.postMessage",
                channel=channel,
                text=text
            )
        elif command == "Backmarkt?":
            bc = BackmarktCrawler()
            text = "*Backmarkt:*\n```"
            text += bc.get_menus()
            text += "```"
            self.slack_client.api_call(
                "chat.postMessage",
                channel=channel,
                text=text
            )
        elif "where" in command.lower():
            random_number = randint(0, 3)
            if random_number == 0:
                text = "You seem hungry. Let's have some thai food!"
            elif random_number == 1:
                text = "You can't go wrong with Pizza. Let's go to Corona!"
            elif random_number == 2:
                text = "Backmarkt it is!"
            else:
                text = "You have things to do! Just grab a swandwich."

            self.slack_client.api_call(
                "chat.postMessage",
                channel=channel,
                text=text
            )
        elif "test-daily" in command.lower():
            self.daily_message(channel)
        else:
            # Sends the response back to the channel
            self.slack_client.api_call(
                "chat.postMessage",
                channel=channel,
                text="Not sure what to do 😋😠")


def main():
    bot = HangryBot()
    bot.run()


if __name__ == '__main__':
    main()

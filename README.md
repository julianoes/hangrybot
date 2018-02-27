# Hangry Bot

A bot to present lunch infos and start a poll where to go.

## Set up the Slack integration

1. Create a Slack App.
2. Create a Slack Bot User.
3. Get the `Bot User OAuth Access Token`.

```
pip3 install --user slackclient
```

## Run the bot

```
export SLACK_BOT_TOKEN=xoxb-...
./hangrybot.py
```

# Hangry Bot

A bot to present lunch infos and start a poll where to go.

## Set up the Slack integration

1. Create a Slack App.
2. Create a Slack Bot User.
3. Get the `Bot User OAuth Access Token`.

```
pip3 install --user slackclient beautifulsoup4 schedule
```

## Run the bot

```
export SLACK_BOT_TOKEN=xoxb-...
./hangrybot.py
```

## Run the bot on Heroku

1. Register a (free) Heroku account.
2. Add a Heroku app.
3. Connect to github.
4. Enable auto-deploy from master.
5. Add the Slack token in 'Settings -> Config Variables'.
6. Add the heroku/python buildpack.
7. Don't forget to start the dyno in 'Overwiew -> Configure Dynos' and there set the worker to `ON`.

Note that Heroku makes use of [requirements.txt](requirements.txt) and [Procfile](Procfile).

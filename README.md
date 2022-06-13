# Slack app request validation


To include a security measure in your Slack app, you can validate that the request that is coming from Slack to your app. This uses payload that Slack includes in the requests, and the app's `Signing Secret` which is shown in the apps configuration page: `https://api.slack.com/apps/{AppID}/general?`

The script in this repo is a Flask application that I wrote following [Slack docs](https://api.slack.com/authentication/verifying-requests-from-slack).
 

## Steps to run the app

Download the repo into a folder. Open a terminal and `cd` into the folder.

Create a virtual environment, choosing a `Name` for it:
```
$ python3 -m venv {Name}
```

Activate the virtual environment
```
$ source {Name}/bin/activate
```

Install the requirements with
```
$ pip3 install -r requirements.txt
```

Once you have the Slack Signing Secret, you'd need to add it as an environment variable. To do so, create an `.env` file. You can use the template in this repo:
```
$ cp .env.template .env
```

Then, add the Signing Secret in it and save. Once you saved the file, you'll need to source environment variables with:
```
$ source .env
```

Then you could run the app: 

```
$ python3 validate_slack_request.py
```

Now port 5000 in your local machine is listening.

To test this with Slack, I used `ngrok` and create a public internet URL. Here's [instructions](https://nahusznaj.github.io/learning/ngrok-alias/) on setting up ngrok.

Once you try your command and Slack requests the ngrok URL, you'll see the response in Slack and in your terminal Flask logs.


## Slack's incoming request

For reference, the request this app is able to validate has this form (note that this was triggered from a user in Slack running a forward slash command):

HEADERS
```
Host: public.url.for.your.app
User-Agent: Slackbot 1.0 (+https://api.slack.com/robots)
Accept-Encoding: gzip,deflate
Accept: application/json,*/*
X-Slack-Signature: v0=XXXXXXX_signature
X-Slack-Request-Timestamp: 1619186236
Content-Length: 425
Content-Type: application/x-www-form-urlencoded
X-Forwarded-Proto: https
X-Forwarded-For: A.VALID.IP.20.176.196
```

BODY
```
{'api_app_id': 'appID',
 'channel_id': 'channelID',
 'channel_name': 'channelName',
 'command': '/thecommand',
 'is_enterprise_install': 'false',
 'response_url': 'https://hooks.slack.com/commands/MOREINFO',
 'team_domain': 'workspace',
 'team_id': 'teamID',
 'text': 'input text',
 'token': 'app token',
 'trigger_id': 'triggerID',
 'user_id': 'userID',
 'user_name': 'userName'}
```


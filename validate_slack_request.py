from flask import Flask, request, make_response
import requests
import json
import time 
import hmac 
import hashlib
import urllib.parse 

from dotenv import load_dotenv
load_dotenv()

import os
slack_signing_secret = os.getenv("slack_signing_secret")

app = Flask(__name__)

@app.route('/', methods=['POST']) 
def foo():    
    slack_headers = request.headers #obtain the headers from the incoming POST request

    timestamp = slack_headers['X-Slack-Request-Timestamp'] #absolute time in headers sent by Slack in the headers

    if timestamp is not None: # this security measure is documented by Slack
        timestamp = float(timestamp)
        if abs(time.time() - timestamp) > 60 * 5:
        # The request timestamp is more than five minutes from local time.
        # It could be a replay attack, so let's ignore it.
            return '', 403  
    
    timestamp = str(timestamp)[:-2] # after converting to float to check the replay thread, we need to cut the last two digits: XXXX.0 (float) -> 'XXXX' (str)

    slack_signature = slack_headers['X-Slack-Signature'] # this is the signature that Slack sends along in the headers of the request. The one we need to build and compare against to decide if the request to our app came genuinely from our Slack app

    slack_payload = request.form #obtain the incoming request's POST payload

    dict_slack = slack_payload.to_dict()

    payload= "&".join(['='.join([key, urllib.parse.quote(val, safe='')]) for key, val in dict_slack.items()]) # it's important to notice that we're parsing through the payload to replace characters / -> %2, : -> %3A

    ### compose the message for our side's sha256 signature
    sig_basestring = 'v0:' + timestamp + ':' + payload
    sig_basestring = sig_basestring.encode('utf-8')

    ### Signing Secret provided by Slack upon creating the App, encoded:
    signing_secret = slack_signing_secret.encode('utf-8')
    
    ## create our signature
    my_signature = 'v0=' + hmac.new(signing_secret, sig_basestring, hashlib.sha256).hexdigest()
    
    # if the signatures match, let's then run this show!
    if my_signature == slack_signature:  
        ## do what your app does!
        output = 'great, request validated!'
    
        response = make_response(output, 200)
        
        response.mimetype = "text/plain"
        
        return response

    ## do what your app does!
    output = 'request not validated, sorry!'

    response = make_response(output, 403)
    
    response.mimetype = "text/plain"
    
    return response


if __name__ == "__main__":
    app.run(debug=True)
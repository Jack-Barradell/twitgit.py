#!/usr/bin/python3

from flask import Flask, request, abort
import tweepy
from Crypto.Hash import SHA, HMAC


app = Flask(__name__)

# Twitter config
app.config['PERMITTED_HOOKS'] = ['127.0.0.1']
app.config['CONSUMER_TOKEN'] = 'FakeConsumerToken'
app.config['CONSUMER_SECRET'] = 'FakeConsumerSecret'
app.config['ACCESS_TOKEN'] = 'FakeAccessToken'
app.config['ACCESS_TOKEN_SECRET'] = 'FakeAccessSecret'

# Github Config
app.config['GITHUB_SECRET'] = 'f53904ec713350e5a9faa550d146f46ea54af492'  # This is a temporary key and no longer valid
app.config['VERIFY_GITHUB'] = True

# Setup twitter
# auth = tweepy.OAuthHandler(app.config['CONSUMER_TOKEN'], app.config['CONSUMER_SECRET'])
# auth.set_access_token(app.config['ACCESS_TOKEN,'], app.config['ACCESS_TOKEN_SECRET'])
# api = tweepy.api(auth)


@app.route('/', methods=['POST'])
def github_update():
    github_mac = request.headers.get('HTTP_X_HUB_SIGNATURE')
    sig = "sha1=" + HMAC.new(app.config['GITHUB_SECRET'], request.data, SHA).hexdigest()
    print("Github hashed {}".format(github_mac))
    print("Calced sig {}".format(sig))
    if sig != github_mac:
        abort(403)

    # Debug message
    print("\n ######################################### \n")
    print("Github verified")
    print("\n ######################################### \n")
    return "OK"


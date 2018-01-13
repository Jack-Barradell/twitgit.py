#!/usr/bin/python3

from flask import Flask, request
import tweepy
from Crypto.Hash import SHA, HMAC


app = Flask(__name__)

# Twitter config
app.config['PERMITTED_HOOKS'] = ['127.0.0.1']
app.config['CONSUMER_TOKEN'] = 'FakeConsumerToken'
app.config['CONSUMER_SECRET'] = 'FakeConsumerSecret'
app.config['ACCESS_TOKEN'] = 'FakeAccessToken'
app.config['ACCESS_TOKEN_SECRET'] = 'FakeAccessSecret'
app.config['GITHUB_SECRET'] = 'f53904ec713350e5a9faa550d146f46ea54af492' # This is a temporary key and no longer valid

# Setup twitter
#auth = tweepy.OAuthHandler(app.config['CONSUMER_TOKEN'], app.config['CONSUMER_SECRET'])
#auth.set_access_token(app.config['ACCESS_TOKEN,'], app.config['ACCESS_TOKEN_SECRET'])
#api = tweepy.api(auth)


@app.route('/', methods=['POST'])
def github_update():
    print("Github hashed {}".format((request.headers.get('HTTP_X_HUB_SIGNATURE'))))
    #x = HMAC.new(,app.config['GITHUB_SECRET'], )
    print(request.remote_addr)
    print(request.remote_user)
    return "OK"


#def verify_webhook(payload_body):

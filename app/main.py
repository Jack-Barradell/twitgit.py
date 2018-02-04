from flask import Flask, request, abort
import tweepy
import logging
import json
import textwrap
from Crypto.Hash import SHA, HMAC


app = Flask(__name__)

# Twitter config
app.config['PERMITTED_HOOKS'] = ['127.0.0.1']
app.config['CONSUMER_TOKEN'] = 'FakeConsumerToken'
app.config['CONSUMER_SECRET'] = 'FakeConsumerSecret'
app.config['ACCESS_TOKEN'] = 'FakeAccessToken'
app.config['ACCESS_TOKEN_SECRET'] = 'FakeAccessSecret'
app.config['MAX_TWEET_LENGTH'] = 280

# Github Config
app.config['GITHUB_SECRET'] = 'f53904ec713350e5a9faa550d146f46ea54af492'  # This is a temporary key and no longer valid
app.config['VERIFY_GITHUB'] = True

# Setup twitter
# auth = tweepy.OAuthHandler(app.config['CONSUMER_TOKEN'], app.config['CONSUMER_SECRET'])
# auth.set_access_token(app.config['ACCESS_TOKEN,'], app.config['ACCESS_TOKEN_SECRET'])
# api = tweepy.api(auth)


@app.route('/', methods=['GET'])
def index_page():
    return "Twitgit is live!"


@app.route('/', methods=['POST'])
def receive_post():
    logging.debug('Received request from {}'.format(request.remote_addr))
    if app.config['VERIFY_GITHUB']:
        github_mac = request.headers.get('X-HUB-SIGNATURE')
        sig = "sha1={}".format(HMAC.new(app.config['GITHUB_SECRET'].encode('utf-8'), request.get_data(), SHA).hexdigest())
        print("Github hashed {}".format(github_mac))
        print("Calced sig {}".format(sig))
        if not sig == github_mac:
            abort(403)
        # Debug message
        print("\n ######################################### \n")
        print("Github verified")
        print("\n ######################################### \n")

    request_details = request.get_json(force=True)
    #print("request details are {}".format(request_details))
    #json_data = json.loads(request_details)[0]
    print("\n \n")
    #print("commits {}".format(request_details['commits']))
    commit_list = request_details['commits']
    tweets = []
    for commit in commit_list:
        if len(commit['message']) + 24 > app.config['MAX_TWEET_LENGTH']:
            print("msg needs trimming")
            tweet = '{}...\n{}'.format(textwrap.shorten(commit['message'], width=app.config['MAX_TWEET_LENGTH']-27, placeholder='...'), commit['url'])
            tweets.append(tweet)
        else:
            print("Tweet dat boi")
            tweet = '{}\n{}'.format(commit['message'], commit['url'])
            tweets.append(tweet)
            print("Tweet :\n{}".format(tweet))


    return "OK", 200


if __name__ == '__main__':
    # Debug mode
    app.run(host='0.0.0.0', debug=True, port=80)


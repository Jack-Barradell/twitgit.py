from flask import Flask, request, abort
import tweepy
import logging
import textwrap
import time
from Crypto.Hash import SHA, HMAC


app = Flask(__name__)

# Twitter config
app.config['PERMITTED_HOOKS'] = ['127.0.0.1']
app.config['CONSUMER_TOKEN'] = 'FhfY3KQyQq1miyCS0sQFm8z6S'
app.config['CONSUMER_SECRET'] = 'eqOSYx1Q8UAsk0G2FVEX4QBQdhH4Ujb10nNT3zUv4CoTqvGABI'
app.config['ACCESS_TOKEN'] = '1551044965-P1FWKcMniCfDnxQaVBi4hnCsm01KM9laMRG00LS'
app.config['ACCESS_TOKEN_SECRET'] = 'FTBtzcoTGWJBiW9R0ocMOUxrNyvfLOeMxIIFcUy2HwBGk'
app.config['MAX_TWEET_LENGTH'] = 280

# Github Config
app.config['GITHUB_SECRET'] = 'f53904ec713350e5a9faa550d146f46ea54af492'  # This is a temporary key and no longer valid
app.config['VERIFY_GITHUB'] = True

# Setup twitter
auth = tweepy.OAuthHandler(app.config['CONSUMER_TOKEN'], app.config['CONSUMER_SECRET'])
auth.set_access_token(app.config['ACCESS_TOKEN'], app.config['ACCESS_TOKEN_SECRET'])
api = tweepy.API(auth)


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
        if len(commit['message']) + 32 > app.config['MAX_TWEET_LENGTH']:
            tweet = 'Commit:\n{}\n{}'.format(textwrap.shorten(commit['message'], width=app.config['MAX_TWEET_LENGTH']-32, placeholder='...'), commit['url'])
            tweets.append(tweet)
        else:
            tweet = 'Commit:\n{}\n{}'.format(commit['message'], commit['url'])
            tweets.append(tweet)

    for tweet in tweets:
        print(tweet + '\n\n\n')
        try:
            api.update_status(tweet)
        except tweepy.RateLimitError:
            limit_hit = True
            while limit_hit:
                print("Rate limit hit sleeping 60 seconds then trying again")
                time.sleep(60)
                try:
                    api.update_status(tweet)
                    limit_hit = False
                    break
                except tweepy.RateLimitError:
                    continue


    return "OK", 200


if __name__ == '__main__':
    # Debug mode
    app.run(host='0.0.0.0', debug=True, port=80)


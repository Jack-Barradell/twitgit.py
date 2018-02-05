# Twitgit.py

Automatically tweet your commit messages!

## Installation

1) Build Docker image
2) Setup twitter app
3) Generate and set github secret
4) Start docker container with following enviroment variables
* CONSUMER_TOKEN
* CONSUMER_SECRET
* ACCESS_TOKEN
* ACCESS_TOKEN_SECRET
* GITHUB_SECRET

(I Recommend using nginx-proxy for docker container management)

## Todo
* Upload docker image to docker hub
* Better instructions 
* Unit tests
* Support for other github webhooks
* Better GET route to explain what it is


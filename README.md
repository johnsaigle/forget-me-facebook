_This repo is a work in progress. Please read and contribute to the discussion taking place in the open Issues._

# Forget me, Facebook!

Periodically delete old Facebook interactions (posts, likes, tags, event attendance, etc.)

## Install

Clone this repo and then run `pip install -r requirements.txt`

## Run

`cd forget/ && scrapy crawl facebook` -- this will launch the facebook `LoginSpider`. Right now this just prompts for your credentials via command line. It will display a message whether you have succeeded or failed, and then quit. **This command must be run from within the `scrapy` root directory, i.e. `forget/`**.

#!//usr/bin/env python
"""
Description: 
    Download tweets using tweet ID, downloaded from https://noisy-text.github.io/files/tweet_downloader.py

Usage example (in linux):
    clear;python tweet_downloader.py --credentials ../data/credentials.txt --inputfile ../data/input.tids --outputtype IdTweetTok

Inputfile contains training/validation data whose first column is tweetID

credentials.txt stores the Twitter API keys and secrects in the following order:
consumer_key
consumer_secret
access_token
access_token_secret

Required Python library: 
    ujson, twython and twokenize (https://github.com/myleott/ark-twokenize-py)

An example output with whitespace tokenised text and tweet id in JSON format
    {"text":"@SupGirl whoaaaaa .... childhood flashback .","id_str":"470363741880463362"}
"""

try:
    import ujson as json
except ImportError:
    import json
import sys
import time
import argparse
from twython import Twython, TwythonError
from collections import OrderedDict

MAX_LOOKUP_NUMBER = 100
SLEEP_TIME = 15 + 1
twitter = None
arguments = None
tid_list = None

def init():
    global twitter, arguments, tid_list

    parser = argparse.ArgumentParser(description = "A simple tweet downloader for WNUT-NORM shared task.")
    parser.add_argument('--credentials', type=str, required = True, help = '''\
        Credential file which consists of four lines in the following order:
        consumer_key
        consumer_secret
        access_token
        access_token_secret
        ''')
    parser.add_argument('--inputfile', type=str, required = True, help = 'Input file one tweet id per line')
    parser.add_argument('--outputtype', type=str, default='IdTweet', choices = ['json', 'IdTweet'], help = '''\
        Output data type:
        (1) json: raw JSON data from Twitter API;
        (2) IdTweet: tweet ID and raw tweet messages (default)
        ''')
    arguments = parser.parse_args()

    credentials = []
    with open(arguments.credentials) as fr:
        for l in fr:
            credentials.append(l.strip())
    twitter = Twython(credentials[0], credentials[1], credentials[2], credentials[3])

    tid_list = []
    with open(arguments.inputfile) as fr:
        for l in fr:
            jobj = json.loads(l.strip())
            tid = jobj['tweet_id']
            tid_list.append(tid)

def download():
    global twitter, arguments, tid_list
    with open(arguments.inputfile + "." + arguments.outputtype, "w") as fw:
        tid_number = len(tid_list)
        max_round = tid_number // MAX_LOOKUP_NUMBER + 1
        for i in range(max_round):
            tids = tid_list[i * MAX_LOOKUP_NUMBER : (i + 1) * MAX_LOOKUP_NUMBER]
            time.sleep(SLEEP_TIME)
            jobjs = []
            jobjs = twitter.lookup_status(id = tids)
            for jobj in jobjs:
                if arguments.outputtype == "json":
                    fw.write(json.dumps(jobj))
                else:
                    tweet = jobj["text"]
                    tid = jobj["id_str"]
                    dic_tweet = (('tweet_id', tid), ('text', tweet))
                    fw.write(json.dumps(OrderedDict(dic_tweet)))
                fw.write("\n")

def main():
    init()
    download()

if __name__ == "__main__":
    main()
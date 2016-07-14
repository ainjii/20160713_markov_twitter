from random import choice
from sys import argv
import os    #to access our OS environment variables

import twitter #available on lab machines, otherwise pip install into active venv

#Using python os.environ to get environtmental variables
#
# Note: you must run 'source secrets.sh' before running this file to set reqd env vars

def twitter_funct(text):

    api = twitter.Api(
        consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
        access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
        access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

    #print out credentials to ensure correct
    print api.VerifyCredentials()

    #send a tweet
    status = api.PostUpdate(text)
    print status.text

    return None


def open_and_read_file(file_path):
    """Takes file path as string; returns text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    contents = open(file_path).read()

    return contents


def make_chains(text_string, n):
    """Takes input text as string; returns _dictionary_ of markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> make_chains("hi there mary hi there juanita")
        {('hi', 'there'): ['mary', 'juanita'], ('there', 'mary'): ['hi'], ('mary', 'hi': ['there']}
    """

    chains = {}

    words = text_string.split()

    
    # get keys for chains dictionary
    for i in range(len(words)-n):

        chains_key = tuple(words[i:i+n])
        # chains = (words[i], words[i+1])

        chains_value = words[i+n]

        # print chains_key
        # print chains_value
    
        chains[chains_key] = chains.get(chains_key, [])
        # don't assign this to a value because .append returns none
        chains[chains_key].append(chains_value)

        # print chains
    
    return chains


def make_text(chains, n):
    """Takes dictionary of markov chains; returns random text."""
    
    cap_keys = [key for key in chains.keys() if key[0] == key[0].capitalize()]
    key = choice(cap_keys)

    
    text = ""
    text_since_punctuation = " ".join(key) + " "

    #limiting output by character count if there's never an end to the string concatenation
    #could have user specify the default cut off value (characters)
    #setting cut off value to 140 to limit to Twitter allowable characters
    while chains.get(key, False) and len(text) < 140:
        # print text
        # print key
        next_word = choice(chains[key])
        text_since_punctuation += "{} ".format(next_word)

        print "length is:", len(text)+len(text_since_punctuation)
        #check if current string text is < 140 characters
        if len(text)+len(text_since_punctuation) > 140:
            break
        else:
            if text_since_punctuation.rstrip().endswith(('.', '!', '?', '"', "'", "...", ",")):
                text += text_since_punctuation
                text_since_punctuation = ""
            
            # start range at 1 because don't need first element in key (already used)
            key_list = [key[i] for i in range(1, len(key))]
            key_list.append(next_word)

            key = tuple(key_list)
            # print key will print out the tuple of 3 elements


    return text


input_path = argv[1]
n = int(argv[2])

# Open the file and turn it into one long string
input_text = open_and_read_file(input_path)
# print 'got input_text'
# Get a Markov chain
chains = make_chains(input_text, n)
# print 'chains made'
# Produce random text
random_text = make_text(chains, n)
# print 'random_text made'
print random_text

twitter_funct(random_text)
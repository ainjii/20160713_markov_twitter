import os
import twitter

from collections import defaultdict
from random import choice
from sys import argv


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

        >>> make_chains("hi there mary hi there juanita", 2)
        {('hi', 'there'): ['mary', 'juanita'], ('there', 'mary'): ['hi'], ('mary', 'hi': ['there']}
    """

    chains = defaultdict(list)
    words = text_string.split()

    # get keys for chains dictionary
    for i in range(len(words)-n):

        chains_key = tuple(words[i:i+n])
        chains_value = words[i+n]

        chains[chains_key].append(chains_value)

    return chains


def make_text(chains, n, hashtags):
    """Takes dictionary of markov chains.

    Returns semi-random text based on input string.
    """

    # set starting values for variables
    key = choose_random_start_key(chains)
    text = ""
    # This is a buffer variable.
    # We'll only add this if we get to a point where this ends
    # with valid sentence punctuation and doesn't cause 'text'
    # to be too long.
    text_since_punctuation = " ".join(key) + " "

    # while the current key has a value associated with it
    while chains.get(key, False):
        # choose a random word from those available for the current key
        # and add it to our buffer
        next_word = choice(chains[key])
        text_since_punctuation += "{} ".format(next_word)

        # if the length of our current text plus the length of the pending text
        # and hashtags exceeds 140 characters, stop adding to the buffer.
        if tweet_is_too_long(text, text_since_punctuation, hashtags):
            # add the hashtag once we've determined we're done adding
            # to our text
            text += hashtags
            # then exit the loop so we can finish the function
            break
        else:
            # if the test buffer ends with punctuation after adding the
            # new word, add it to text and clear the buffer
            if ends_with_punctuation(text_since_punctuation):
                text += text_since_punctuation
                text_since_punctuation = ""

            # update the key for the next iteration
            key_list = [item for i, item in enumerate(key) if i > 0]
            key_list.append(next_word)
            key = tuple(key_list)

    return text


def choose_random_start_key(chains):
    """ Chooses a starting key for a markov chain.

    Returns a random key from the keys whose first element begins
    with an uppercase letter.
    """

    cap_keys = [key for key in chains.keys() if key[0] == key[0].capitalize()]
    return choice(cap_keys)


def tweet_is_too_long(text, text_since_punctuation, hashtags):
    """ Determines whether the length of text would exceed 140
    characters if the buffer and hashtags were added to it.

    Returns a boolean.
    """

    return (len(text) + len(text_since_punctuation) + len(hashtags)) > 140


def ends_with_punctuation(text):
    """ Determines whether a string ends with valid sentence
    punctuation.

    Returns a boolean.
    """

    punctuation = ('.', '!', '?', '"', "'", "...")
    return text.rstrip().endswith(punctuation)


def tweet(text):
    """ Sends a tweet to Twitter using the Twitter API.

    Returns None.
    """

    api = twitter.Api(
        consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
        access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
        access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

    # send a tweet
    status = api.PostUpdate(text)


if __name__ == '__main__':
    # set constants and grab arguments from command line
    HASHTAGS = '#hbgraceXV'
    input_path = argv[1]
    n = int(argv[2])

    # initialize variable for user_input
    user_input = ''

    # read input file as one long string
    input_text = open_and_read_file(input_path)

    # create a dictionary of n-grams
    chains = make_chains(input_text, n)

    # until the user chooses to quit
    while user_input != 'q' :
        # ask if they want to tweet again
        user_input = raw_input('Press [Enter] to tweet. [q] to quit. ')

        # if they press anything other than Enter or q,
        # print an error.
        if user_input not in ['q', '']:
            print "Please press [Enter] or [q]."
        # if they press Enter, create and post another tweet
        elif user_input == '':
            random_text = make_text(chains, n, HASHTAGS)
            tweet(random_text)

import argparse
import matplotlib.pyplot as plt

from util.name_utils import parse_first_name
from util.message_reader import read_message_json, construct_fb_messages


def retrieve_frequencies(msgs):
    """
    Retrieve sender -> count numbers.
    
    :param msgs: list of FacebookMessage objects
    :return:     dictionary mapping sender name to count.
    """
    freqs = dict()
    for message in msgs:
        member = message.sender_name
        if member in freqs:
            freqs[member] += 1
        else:
            freqs[member] = 1

    return freqs


def plot_histogram(chat_name, freqs):
    """
    Plot the histogram of chat messages.
    
    :param chat_name: name (str) of the chat, which is used as the title of the plot.
    :param freqs:     dictionary of sender name -> count numbers used to construct the histogram.
    """
    plt.xlabel('Members')
    plt.ylabel('Frequency')
    plt.title('{} Message Frequency'.format(chat_name))
    plt.bar(freqs.keys(), freqs.values())
    plt.show()


def retrieve_first_names(freq):
    """
    For each name in the freq dictionary, key by only the first name.
    :param freq: (dict) containing name to frequency mapping
    :return:     (dict) with same contents of freq but keyed by first name
    """
    first_name_freq = dict()

    for name in freq:
        first_name = parse_first_name(name)

        first_name_freq[first_name] = freq[name]

    return first_name_freq


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Give you frequency of messages sent for each sender.')
    parser.add_argument('message_file', metavar='F', type=str, nargs=1, help='filepath of message file')
    parser.add_argument('-s', '--shorten', action='store_true', required=False,
                        help='flag to indicate whether to shorten names in the plot')

    args = parser.parse_args()
    message_file = args.message_file[0]

    chat_name, msgs = read_message_json(message_file)
    fb_messages = construct_fb_messages(msgs)

    freqs = retrieve_frequencies(fb_messages)

    if args.shorten:
        freqs = retrieve_first_names(freqs)

    plot_histogram(chat_name, freqs)


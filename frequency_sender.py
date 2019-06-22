import argparse
import json
import matplotlib.pyplot as plt

from util.name_utils import parse_first_name


def read_in_json(message_file):
    """
    Read in json file representing the chat messages and retrieve the chat name and all the messages.

    :param message_file: filepath (str) to the chat messages.
    :return:             chat name (str) and dictionary of messages from the chat.
    """
    with open(message_file) as f:
        msgs_file_json = json.load(f)

    chat_name = msgs_file_json['title']
    msgs = msgs_file_json['messages']
    return chat_name, msgs


def retrieve_frequencies(msgs):
    """
    Retrieve sender -> count numbers.
    
    :param msgs: dictionary containing chat messages where the keys are the senders.
    :return:     dictionary mapping sender name to count.
    """
    freqs = dict()
    for message in msgs:
        member = message['sender_name']
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
    plt.title(chat_name + ' Message Frequency')
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

    chat_name, msgs = read_in_json(message_file)
    freqs = retrieve_frequencies(msgs)

    if args.shorten:
        freqs = retrieve_first_names(freqs)

    plot_histogram(chat_name, freqs)


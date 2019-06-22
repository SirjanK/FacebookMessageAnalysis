import argparse
import matplotlib.pyplot as plt
import numpy as np

from datetime import datetime

from util.message_reader import construct_message_dataframe, MessageAttributes
from util.name_utils import parse_first_name

# Reasonable cap so that the line graph does not get over populated.
MAX_USERS = 20


def plot_growth(chat_name, msg_df):
    """
    Plot the number of messages over time on a per user basis.

    :param chat_name: name of the chat.
    :param msg_df:    pandas DataFrame holding message contents for the chat.
    """
    unique_names = msg_df[MessageAttributes.SENDER_NAME].unique()

    assert len(unique_names) <= MAX_USERS, 'Max users cannot exceed {}'.format(MAX_USERS)

    plt.xlabel('Date')
    plt.ylabel('Number of Messages')
    plt.title('{} Chat Growth'.format(chat_name))

    first_names = []

    # Iterate through the unique names.
    for name in unique_names:
        filtered_df = msg_df[msg_df[MessageAttributes.SENDER_NAME] == name]

        # Sort the timestamps for the single user
        sorted_timestamps = sorted(filtered_df[MessageAttributes.TIMESTAMP_MS])

        # Convert to datetime objects
        sorted_datetimes = [datetime.fromtimestamp(timestamp / 1000) for timestamp in sorted_timestamps]

        # Counts are monotonically increasing
        counts = np.arange(1, len(sorted_datetimes) + 1)

        first_name = parse_first_name(name)
        first_names.append(first_name)

        plt.plot(sorted_datetimes, counts)

    plt.legend(first_names, loc='upper left')

    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plots growth over time in a chat on a per user basis.')
    parser.add_argument('message_file', metavar='F', type=str, nargs=1, help='filepath of message file')

    args = parser.parse_args()
    message_file = args.message_file[0]

    chat_name, msg_df = construct_message_dataframe(message_file)

    plot_growth(chat_name, msg_df)

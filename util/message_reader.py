import json
import pandas as pd


class MessageType:
    """
    Enum containing the message type.
    """
    GENERIC = "Generic"
    SHARE = "Share"
    SUBSCRIBE = "Subscribe"
    UNSUBSCRIBE = "Unsubscribe"


class FacebookMessage:
    """
    A FacebookMessage object encapsulates a single message.
    """

    ATTRIBUTES = [
        'photos',
        'sender_name',
        'timestamp_ms',
        'audio_files',
        'gifs',
        'reactions',
        'users',
        'type',
        'share',
        'sticker',
        'content',
        'videos',
        'files'
    ]

    def __init__(self, msg_dict):
        """
        Initialize the Facebook message object from a raw message dict.
        :param msg_dict: standardized dictionary of a message in the format facebook provides.

        TODO: Add more support for canonical forms of all attributes
        """
        self.type = self.parse_from_dict(msg_dict, 'type')
        self.sender_name = self.parse_from_dict(msg_dict, 'sender_name')
        self.timestamp_ms = self.parse_from_dict(msg_dict, 'timestamp_ms')
        self.content = self.parse_from_dict(msg_dict, 'content')
        self.photos = self.parse_from_dict(msg_dict, 'photos')
        self.audio_files = self.parse_from_dict(msg_dict, 'audio_files')
        self.gifs = self.parse_from_dict(msg_dict, 'gifs')
        self.reactions = self.parse_from_dict(msg_dict, 'reactions')
        self.users = self.parse_from_dict(msg_dict, 'users')
        self.share = self.parse_from_dict(msg_dict, 'share')
        self.sticker = self.parse_from_dict(msg_dict, 'sticker')
        self.videos = self.parse_from_dict(msg_dict, 'videos')
        self.files = self.parse_from_dict(msg_dict, 'files')

    @staticmethod
    def parse_from_dict(msg_dict, key):
        """
        Util function to parse a value from a msg dict for a key
        if available.

        :return: value of the key if key exists, otherwise None.
        """
        if key in msg_dict:
            return msg_dict[key]

        return None


def read_message_json(msg_file):
    """
    Util function to read in contents from a message json.
    :param msg_file: file containing messages in standard format from facebook.
    :return:         chat name, and dictionary of messages
    """

    with open(msg_file) as f:
            msgs_file_json = json.load(f)

    chat_name = msgs_file_json['title']
    msgs = msgs_file_json['messages']

    return chat_name, msgs


def construct_fb_messages(msgs):
    """
    Construct a FacebookMessage object from all message dicts in the msgs list.

    :param msgs: list of dicts in standard format
    :return:     list of FacebookMessage objects
    """

    facebook_messages = []

    for msg in msgs:
        facebook_messages.append(FacebookMessage(msg))

    return facebook_messages


def construct_message_dataframe(msg_file):
    """
    Directly construct a Pandas DataFrame from a message file.
    This is a one-time expensive construction. The DataFrame is expected to fit in memory.
    :param msg_file: file containing messages in standard format from facebook.
    :return:         chat name, pandas DataFrame with None placeholders for empty fields.
    """
    chat_name, json_msgs = read_message_json(msg_file)

    fb_messages = construct_fb_messages(json_msgs)

    columns = dict()

    # Initialize as empty list
    for attr in FacebookMessage.ATTRIBUTES:
        columns[attr] = []

    # Iterate through messages
    for msg in fb_messages:
        msg_dict = msg.__dict__

        for attr in FacebookMessage.ATTRIBUTES:
            columns[attr].append(msg_dict[attr])

    return pd.DataFrame.from_dict(columns)


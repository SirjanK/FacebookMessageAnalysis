import argparse
import os
import matplotlib.pyplot as plt
import re

from wordcloud import WordCloud, STOPWORDS

from util.message_reader import read_message_json, construct_fb_messages, MessageType


def generate_word_cloud(body_of_text, title, max_words=200):
    """
    Generate the word cloud image given a body of text.
    :param body_of_text: concatenated words from chat(s).
    :param title:        title of the word cloud.
    :param max_words:    number of words to include in the cloud.
    """
    updated_text = preprocess_text(body_of_text)
    wordcloud = WordCloud(max_words=max_words, 
            width=800, height=400, stopwords=STOPWORDS).generate(updated_text)
    plt.title(title)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()


def preprocess_text(body_of_text):
    """
    Preprocess the text from chat(s).
    :param: body_of_text: concatenated words from chat(s).
    :return:              preprocessed concatenated words from chat(s).
    """
    text_without_at = body_of_text.replace('@', '')
    text_quote_sanitized = text_without_at.replace("\u00e2\u0080\u0099", '\'')
    lowercase_text = text_quote_sanitized.lower()
    return lowercase_text


def generate_word_cloud_all_messages(all_messages_dir, user, max_words=200):
    """
    Generate a word cloud of all the messages the user has sent.
    :param all_messages_dir: filepath to the directory containing all the messages for a user.
    :param user:             name of user as would appear in the message json.
    :param max_words:        number of words to include in the cloud.
    """
    all_chat_jsons = []
    for dir_path, dir_names, fnames in os.walk(all_messages_dir):
        if not dir_names and len(fnames) == 1 and re.match("message.*\.json", fnames[0]):
            chat_json_filepath = os.path.join(dir_path, fnames[0])
            all_chat_jsons.append(chat_json_filepath)

    title = "Word Cloud for {}".format(user)
    all_messages = []
    
    for chat_json_filepath in all_chat_jsons:
        _, msgs = read_message_json(chat_json_filepath)
        fb_msgs = construct_fb_messages(msgs)

        for message in fb_msgs:
            if message.sender_name == user and message.type == MessageType.GENERIC and message.content:
                all_messages.append(message.content)

    body_of_text = ' '.join(all_messages)
    generate_word_cloud(body_of_text, title, max_words)


def generate_word_cloud_specific_chat(message_file, max_words=200):
    """
    Generate a word cloud of all the messages (from any user) for a specific chat.
    :param message_file: filepath (str) to the chat messages.
    :param max_words:    number of words to include in the cloud.
    """
    chat_name, msgs = read_message_json(message_file)
    fb_messages = construct_fb_messages(msgs)

    title = "Word Cloud for {}".format(chat_name)

    all_messages = []
    for message in fb_messages:
        if message.type == MessageType.GENERIC and message.content:
            all_messages.append(message.content)

    body_of_text = ' '.join(all_messages)
    generate_word_cloud(body_of_text, title, max_words)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a word cloud for all your messages or for a specific chat.')
    parser.add_argument('-D', '--all_messages_dir', type=str, nargs='+',
                        help='filepath of the directory holding all the chats and the name of the user, in that order.')
    parser.add_argument('-F', '--message_file', type=str, nargs=1, help='filepath of message file for a specific chat.')

    args = parser.parse_args()
    if not (args.all_messages_dir or args.message_file):
        raise Exception("Specify one of the options for generating the word cloud")
    if args.all_messages_dir:
        user_name = ' '.join(args.all_messages_dir[1:])
        generate_word_cloud_all_messages(args.all_messages_dir[0], user_name)
    if args.message_file:
        generate_word_cloud_specific_chat(args.message_file[0])


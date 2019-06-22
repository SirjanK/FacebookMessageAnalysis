def parse_first_name(full_name):
    """
    Parses the first name from the full name. Simple as just
    splitting the name by a space and taking the first element.
    :param full_name: str of the full name.
    :return:          str of the first name.
    """
    assert type(full_name) == str
    assert len(full_name) > 0

    split_name = full_name.split()

    first_name = split_name[0]

    return first_name

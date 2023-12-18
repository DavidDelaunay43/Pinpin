def del_upper(string: str):
    '''
    '''

    for i, char in enumerate(string):
        if char.isupper():
            return string[:i]
    return string

import random


def id_generation(prefix=None):
    print('prefix ', prefix)
    if prefix is not None:
        return str(str(prefix) + '-' + str(random.randint(1111, 9999)))
    else:
        return str('NA' + '-' + str(random.randint(1111, 9999)))

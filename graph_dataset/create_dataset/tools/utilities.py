import time


def list_to_string(my_list, separator=","):
    return separator.join(map(str, my_list))


def print_date():
    print "Script started at " + time.strftime("%H:%M:%S")

"""
Module containing methods for sorting bike station lists.
"""


def python_sort(bike_list: list):
    """
    Function that uses python's "sorted" built-in function to sort lists
    of bike stations
    :param bike_list: The bike list to be sorted.
    :type bike_list: list of dict
    :return:
    :rtype: list
    """
    return sorted(
        bike_list, key=lambda k: (-k['free_bikes'], k['name'])
    )

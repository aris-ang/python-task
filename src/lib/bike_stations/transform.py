"""
Module containing functions useful for performing transformative actions
on bike station lists
"""


def clean_up(bike_station_list):
    """
    Function that restructures each element of the initial retrieved bike
    station list into the requested format of step one.
    :param bike_station_list: The list to be restructured.
    :type bike_station_list: list of dict
    :return: The restructured list, as requested in the test specification.
    :rtype: list of dict
    """
    return [
        {
            'id': x['id'],
            'name': x['name'],
            'active': x['status'] == 'aktiv',
            'description': x['description'],
            'boxes': x['boxes'],
            'free_boxes': x['free_boxes'],
            'free_bikes': x['free_bikes'],
            'free_ratio': x['free_boxes']/x['boxes'],
            'coordinates': [x['longitude'], x['latitude']]
        } for x in bike_station_list if x['free_bikes'] > 0
    ]


async def merge_stations_with_addresses(bike_station_list, address_list):
    """
    Function that merges the bike station and corresponding address list
    for step two. The result is a bike station list that includes addresses.
    :param address_list: The address list
    :type address_list: list of str
    :param bike_station_list: The bike station list.
    :type bike_station_list: list of dict
    :return: The merged list
    :rtype: list of dict
    """
    result = [
        {
            'address': total[1],
            **total[0]
        } for total in zip(bike_station_list, address_list)
    ]
    return result


def partition_station_list(bike_station_list, part_size):
    """
    Function that breaks a bike station into pieces and returns them in a list.
    :param part_size: the size of each partition
    :type part_size: int
    :param bike_station_list: The bike station list to be fragmented.
    :type bike_station_list: list of dict
    :return: A list of bike station lists.
    :rtype: list[list of dict]
    """
    return [
        bike_station_list[i:i + part_size] for i in range(
            0, len(bike_station_list), part_size
        )
    ]

"""
The application's main file
"""
import asyncio
import time
from dotenv import load_dotenv
load_dotenv()

from src.handlers.request_handler import RequestHandler
from src.lib.bike_stations.sorting import python_sort
from src.lib.bike_stations.transform import clean_up,\
    merge_stations_with_addresses
from src.lib.logger.console_logger import logger, listener

listener.start()


async def part_1(request_handler):
    """
    Function that wraps the first part of the task's specification.
    :param request_handler: The request handler.
    :type request_handler: RequestHandler
    :return: The list as requested at the first part of the task spec.
    :rtype: list of dict
    """
    bikes_start = time.time()
    bike_stations = await request_handler.get_bike_stations()
    bikes_stop = time.time() - bikes_start
    logger.debug(
        'bike station response took %f seconds.', bikes_stop
    )
    list_trans_start = time.time()
    cleaned_up_stations = clean_up(bike_stations)
    step_one_list = python_sort(cleaned_up_stations)
    list_trans_stop = time.time() - list_trans_start
    logger.debug(
        'bike list edit took %f seconds.', list_trans_stop
    )
    logger.info(
        'Step one result: %s, length=%i', step_one_list, len(step_one_list)
    )
    return step_one_list


async def part_2(step_one_list, request_handler):
    """
    Function that wraps the second part of the task's specification.
    :param step_one_list: The result of the first part.
    :type step_one_list: list of dict
    :param request_handler: The Request Handler
    :type request_handler: RequestHandler
    :return: The final list as requested on part 2.
    :rtype: list of dict
    """
    part_2_start = time.time()
    address_list = await request_handler.get_station_addresses(
        step_one_list
    )
    logger.debug('Address GATHER took: %f', time.time() - part_2_start)
    merge_start = time.time()
    step_two_list = await merge_stations_with_addresses(
        step_one_list, address_list
    )
    logger.debug(
        'Bike stations - addresses merge took: %f', time.time() - merge_start
    )
    logger.info(
        'Step two result: %s, length=%i', step_two_list, len(step_two_list)
    )
    logger.info('Part 2 took %f', time.time() - part_2_start)
    return step_two_list


async def main():
    """
    Main function.
    :return: None
    :rtype: None
    """
    total_start = time.time()
    request_handler = RequestHandler()
    step_one_result = await part_1(request_handler)
    await part_2(step_one_result, request_handler)
    logger.info('total time: %f', time.time() - total_start)
    await request_handler.close()
    listener.stop()

if __name__ == '__main__':
    asyncio.run(main())

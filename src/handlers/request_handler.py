"""
Class that handles requests to the bike stations and addresses APIs
"""
import asyncio
import os

from aiohttp import ClientSession

from src.exceptions.http.requests import RequestJSONError
from src.exceptions.handlers.request_handler import RequestError
from src.lib.http.requests import request_json
from src.lib.logger.console_logger import logger


class RequestHandler:
    """
    The class member of this class, session, is an aiohttp ClientSession object.
    Request Handler does not hold any other class members.
    """
    def __init__(self):
        """
        Constructor method
        """
        self.session = ClientSession()

    async def close(self):
        """
        Method that closes the member aiohttp client session, thus terminating
        functionality for the request handler.
        :return: None
        :rtype: None
        """
        await self.session.close()

    async def get_bike_stations(self):
        """
        Method that retrieves the initial bike stations as a list
        :return: The bike station list
        :rtype: list of dict
        """
        try:
            bike_stations = await request_json(
                url=f'{os.getenv("BIKE_STATIONS_ENDPOINT")}',
                session=self.session
            )
        except RequestJSONError as error:
            logger.error(error)
            raise RequestError(error) from error

        return bike_stations

    async def get_address_for_point(self, lng, lat):
        """
        Method that retrieves the address of a bike station using its location.
        :param lng: The location's longitude
        :type lng: float
        :param lat: The location's latitude
        :type lat: float
        :return: The address string.
        :rtype: str
        """
        try:
            station = await request_json(
                url=f'{os.getenv("ADDRESS_ENDPOINT")}'
                    f'?latitude={lat}&longitude={lng}',
                session=self.session
            )
            address = station['data']['name']
        except RequestJSONError as error:
            logger.error(
                'Something went wrong with the address request for point'
                ' with lat=%f, lng=%f. %s', lat, lng, error)
            return 'Unknown'
        except KeyError:
            logger.error('Received bad address response body for point with '
                         'lat=%f, lng=%f', lat, lng)
            return 'Unknown'
        return address

    async def get_addresses_for_bike_stations(self, bike_station_list):
        """
        Method that gets the addresses for all bike stations in a list
        concurrently using asyncio.gather
        :param bike_station_list: The bike station list
        :type bike_station_list: list of dict
        :return: The list of addresses.
        :rtype: list of str
        """
        return await asyncio.gather(
            *[self.get_address_for_point(
                lng=x['coordinates'][0], lat=x['coordinates'][1]
            ) for x in bike_station_list]
        )

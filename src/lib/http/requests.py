"""
Module containing functions that involve HTTP requests
"""
from typing import Optional

from aiohttp import ClientSession, ClientError

from src.exceptions.http.requests import RequestJSONError


async def request_json(
        url: str,
        session: ClientSession,
        method: str = 'get',
        body: Optional[dict] = None
):
    """
    Function that performs HTTP requests, expecting JSON responses.
    :param url: The endpoint of the request.
    :type url: str
    :param session: The aiohttp client session used for this request.
    :type session: ClientSession
    :param method: the HTTP method
    :type method: str
    :param body: The request body (if it applies).
    :type body: Optional[dict]
    :return: The JSON response as dict
    :rtype: dict
    """
    try:
        async with session.request(
                method=method,
                url=url,
                json=body if body is not None else None
        ) as resp:
            return await resp.json()
    except ClientError as client_error:
        raise RequestJSONError(client_error) from client_error
    except Exception as exc:
        raise RequestJSONError(exc) from exc


#TODO:
    # Make multiple requests within the same session

from requests import (
    PreparedRequest
)

from .init_request import init_req


def stage_requests(method : str, base_url : str, path : str, **kwargs) -> list[PreparedRequest]:
    """Staging of a list of requests to be sent through a Session. Keywords arguments
    should be arguments related with the parameter from init_req function.

    :param method :
    :param base_url :
    :param path :
    :param **kwargs : dict | list[dict] (header, params, queries or payload)
    """
    staged_args = []
    staged_requests = []

    # longest args

    for k, v in kwargs.items():
        # validate kwargs:
        if k not in ("header", "params", "queries", "payload"):
            raise ValueError(f"{k} is not a valid argument to be passed to init_req")

        # unpack kwargs
        # create recursive function to make a vectorial multiplication with the values
        # from kwargs
        



    return [PreparedRequest()]

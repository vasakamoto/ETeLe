
#TODO:
    # Make multiple requests within the same session

from requests import (
    PreparedRequest,
    Response,
    Session
)

from .init_request import (
    init_req,
    Endpoint
)


def stage_requests(ne : list[Endpoint]) -> list[PreparedRequest]:
    """Staging of a list of requests to be sent through a Session."""

    staged_requests = []
        
    for e in ne:
        staged_requests.append(init_req(e))

    return staged_requests


def request_data(sr : PreparedRequest | list[PreparedRequest]) -> Response | None:
    "Use the PreapredRequests in staged_requests within one sessions to request everything "
    
    with Session() as s:
        if isinstance(sr, list):
            for i in range(len(sr)):
                sr[i] = s.send(sr[i])
        else:
            return s.send(sr)

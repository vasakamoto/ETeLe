
from dataclasses import dataclass

from requests import (
    Request,
    PreparedRequest
)


# TODO:
    # docstring properly
    # handle exceptions
    # tests


@dataclass
class Endpoint():
    method : str
    base_url : str
    path : str
    headers : dict
    payload : dict | None
    params : dict | tuple | None
    queries : dict | tuple | None


def _params_url(url : str, params : dict | tuple) -> str:
    """Returns a formated url string with params. Params values should be passed as 
    string values.

    >>> _params_url("https://api.com/v0/endpoint/:id/path/:name", {'id' : 2, 'name' : "x"})
    "https://api.com/v0/endpoin/2/path/x"

    >>> _params_url("https://api.com/v0/endpoint/{id}/path/{name}", {'id' : 2, 'name' : "x"})
    "https://api.com/v0/endpoin/2/path/x"
    """

    if isinstance(params, dict):
        url_components = url.split("/")
        enum_url_components = enumerate(url_components)
        if url.find("/:") > 0:
            index = [i for i, v in enum_url_components if v.startswith(":")]
            for i in index:
                v = url_components[i][1:]
                url_components[i] = params[v]

            return f"{url_components[0]}//{'/'.join(url_components)}"

        if url.find("/{") > 0:
            index = [i for i, v in enum_url_components if v.startswith("{") and v.endswith("}")]
            for i in index:
                v = url_components[i][1:-1]
                url_components[i] = params[v]
           
            return f"{url_components[0]}//{'/'.join(url_components)}"

        return url

    if isinstance(params, tuple):
        return url

    raise ValueError("Params should be passed as dictionary")


def _queries_url(url : str, queries : dict) -> str:
    """Returns a url string formated with queries passed as a dictionary.

    >>> _queries_url("https://api.com/v0/endpoint", {'date' : "day", 'color' : "colour"})
    "https://api.com/v0/endpoint?date=day&color=colour"
    """

    if not isinstance(queries, dict):
        raise ValueError("Queries should be passed as a dictionary")

    concat_kv = [f"{k}={v}" for k, v in  queries.items()]
    stringfy_query = "&".join(concat_kv)

    return f"{url}?{stringfy_query}"


# construct request 
def init_req(e : Endpoint) -> PreparedRequest:
    """Initialization of parameters used in data requests, basically, url structuring.
    Parse possible url params and queries to structure url string and return a Request
    object to be prepared in a Session request.
    """
    # prepare headers

    # prepare url
    full_path = f"{e.base_url}{e.path}"
    # prepare params
    if e.params:
        full_path = _params_url(full_path, e.params)
    # prepare queries
    if e.queries:
        full_path = _queries_url(full_path, queries)

    if e.method == "POST":
        return Request("POST", url=full_path, headers=e.headers, json=e.payload).prepare()

    return Request("GET", url=full_path, headers=e.headers).prepare()


if __name__ == "__main__":
    header = {
        'Content-Type' : "application/json",
        'ApiToken' : "token"
    }

    url_bracket = "https://api.com/v0/endpoint/{id}/path/{name}"
    url_colon = "https://api.com/v0/endpoint/:id/path/:name"
    params = {'id' : "2", 'name' : "x"}
    queries = {'date' : "day", 'color' : "colour"}
    print(url_colon)
    print(_params_url(url_colon, params))
    print(url_bracket)
    print(_params_url(url_bracket, params))
    print(_queries_url("https://api.com/v0/endpoint", queries))

    base_url = "https://api.com/v0/"
    path = "endpoint/:id/path/:name"
    request = init_req("GET", base_url, path, header, params, queries)
    print(request)



# TODO:
#   Validate if every row have the same number of elements
#       If doesn't, fill with null values
#   Test properly

from ..utils.logger_config import SLOG


def transpose_flat_json(e : list[tuple]) -> None:
    """Receive a list of tuples with pairs of key and values, transpose a matrix i:2
    to a matrix of 2:j.

    >>> transpose_flat_json([("key1", "value01"), ("key2", "value02"), ("key3", "value03")])
    [
        ("key1", "key2", "key3"),
        ("value01", "value02", "value03"),
    ]
    """

    keys = tuple((i[0] for i in e))
    values = tuple((j[1] for j in e)) 

    e = [keys, values]



if __name__ == "__main__":
    transposed = transpose_flat_json([("key1", "value01"), ("key2", "value02"), ("key3", "value03")])
    print(transposed)

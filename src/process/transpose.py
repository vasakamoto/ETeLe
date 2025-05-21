
# TODO:
#   Validate if every row have the same number of elements
#   Test properly

from ..utils.logger_config import SLOG


def transpose_flat_json(R : list[list[tuple]]) -> None:
    """Receive a list of list of tuples with pairs of key and values returning a list
    of rows, the first row being the columns headers.

    >>> transpose_flat_json([
            [("key1", "value01"), ("key2", "value02"), ("key3", "value03")],
            [("key1", "value11"), ("key2", "value12"), ("key3", "value13")],
        ])
    [
        ("key1", "key2", "key3"),
        ("value01", "value02", "value03"),
        ("value11", "value12", "value13"),
    ]
    """

    buffer = []
    headers = []

    # length of list of tuples
    l_length = len(R[0])

    # append column headers to the head of buffer
    for t in R[0]:
        headers.append(t[0]) 

    buffer.append(tuple(headers))

    # for every list of tuples, append values into a list that will be appended to 
    # the buffer
    for l in R:
        row = []
        for i in range(l_length):
            row.append(l[i][1])

        buffer.append(tuple(row))


    R.clear()
    R.extend(buffer)


if __name__ == "__main__":
    transposed = transpose_flat_json([
            [("key1", "value01"), ("key2", "value02"), ("key3", "value03")],
            [("key1", "value11"), ("key2", "value12"), ("key3", "value13")],
        ])
    print(transposed)


# TODO:
#   Validate if every row have the same number of elements
#   Test properly

from ..utils.logger_config import SLOG


def _remove_non_primitive(R : list[list[tuple]]) -> None:
    """The set R doesn't remove the original and pre-flattened data when using flat_json.
    In such way is necessary to clean these data before transposing it, removing every
    tuple that has values with non-primitive values.
    """

    n_R = len(R)
    i = 0
    switch = False
    # Remove everything that is not a primitive data
    while i < n_R:
        SLOG.debug(f"Tuple at index {i} : {R[i]}")
        for t in R[i]:
            if isinstance(t[1], list) or isinstance(t[1], dict):
                R.pop(i)
                SLOG.debug(f"Tuple popped at index {i}")
                n_R = len(R)
                SLOG.debug(f"New length for R: {n_R}")
                switch = True
                break
            switch = False
        if switch:
            i = 0
            continue
        i += 1


def _remove_duplicate_rows(R : list[list[tuple]]) -> None:
    """The function flat_json does not remove duplicate values generated when flattening
    json. So, before transposing the set it should remove duplicate data.
    """
    R.sort()
    
    n_R = len(R)
    i = 1
    while i < n_R:
        if R[i] == R[i-1]:
            R.pop(i)
            n_R = len(R)
            SLOG.debug(f"Popped equal tuples at index {i} and {i-1}\nNew length for R {n_R}")
            i = 1

        else:
            i += 1
             

def sanitize(R : list[list[tuple]]) -> None: 
    _remove_non_primitive(R)
    _remove_duplicate_rows(R)

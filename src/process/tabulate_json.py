"Transforms JSON into a table structure"

#TODO
#   It may be smarter to store the indexes where something happens and then pop then
#   at the end of function execution instead of popping as you go


from os import system

from ..utils.logger_config import SLOG


def _flat_tree(l: list[tuple], i: int=0) -> bool:
    """Destructure a nested tree from a list of tuples *l* obtained from an 
    dict_items into a flattened tree. The index *i* is used to traverse the tree.
    """

    m = f"\nITERATION : {i}\n"
    # Instaciate key *k* and value *v* from a dict_items object
    k, v = l[i]
    m += f"\nKEY : {k}\nVALUE : {v}\n"

    # If value *v* is a dictionary, remove node at index *i*, destructure dictionary
    # into a dict_items and append the tuples into *l*
    if isinstance(v, dict):
        m += f"\nREMOVING ELEMENT AT POSITION : {i}\n"
        l.pop(i)
        for k_n, v_n in v.items():
            m += f"\nNEW COLUMN: {k}_{k_n}, {v_n}\n"
            l.append((f"{k}_{k_n}", v_n))

        SLOG.debug(m)
        return True

    SLOG.debug(m)
    return False



def _multiply_tree(R : list[list[tuple]], l: list[tuple], i: int=0) -> bool:
    """Search for arrays in the tree, if an array with n elements *e* is found, copy 
    base node *bn* and append the new element into a new column.
    """

    m = f"\nITERATION : {i}\n"
    # Instaciate key *k* and value *v* from a dict_items object
    k, v = l[i]
    m += f"\nKEY : {k}\nVALUE : {v}\n"

    # If value *v* is a list, copies l, fetchs list elements *e* and appends into the 
    # copied l, *c*, appends into a new column
    if isinstance(v, list) and len(v) > 0:
        l.pop(i)
        l.append(("k", "v"))
        for e in v:
            l[-1] = (k, e)
            m += f"\nNEW ROW: {l[-1]}\n"
            R.append(l)

        m += f"\nREMOVING ELEMENT AT POSITION : {i}\n"
        l.pop(i)

        SLOG.debug(m)
        return True

    SLOG.debug(m)
    return False


def _tabulate_json(R : list, l : list[tuple], i : int=0) -> None:
    """Traverse JSON, j, nodes flattening it into a tabular format, appending the flattened
    structure into buffer R.
    """

    if i >= len(l):
        return

    # If something is found, retraverse tree
    print("\n\n\nAPPENDING COLUMNS")
    if _flat_tree(l, i):
        _tabulate_json(R, l)
    print("\n\n\n===============================================================\n\n\n")
    print("APPENDING ROWS")
    if _multiply_tree(R, l, i):
        _tabulate_json(R, l)
    _tabulate_json(R, l, i+1)


def tabulate(j : dict) -> list[list[tuple]]:
    system("cls")

    for row in list(jason.items()):
        print(row)

    l = list(j.items())
    R = []
    _tabulate_json(R, l)

    for row in R:
        print("------ROW-------")
        for column in row:
            print(column)

    return R


def tabooit(j : dict) -> list[list]:
    """Flattening of a JSON-like, j, structure into a tabular structure. Dictionary-like
    structures are basically columns and array-like structures can be considered as rows.
    """

    system("cls")
    # Use first level of the tree as a base model
    l = list(j.items())
    m0 = f"\nDICT_ITEMS :\n"
    for tp in l:
        m0 += f"{tp}\n"

    # Transpose dict_items()
    # Base column
    bc = [tp[0] for tp in l]
    m0 += f"\nBASE COLUMNS : {bc}\n"
    # Base row
    br = [tp[1] for tp in l]
    m0 += f"\nBASE ROWS : {br}\n"
    # Base structure
    bs = [bc, br]
    # Buffer for elements from json
    R = []


    # Iterate over values 
    i = 0
    # First, search for dictionaries
    m0 += f"\nSEARCHING FOR DICT-LIKE STRUCTURES\n"
    SLOG.debug(m0)

    while i < len(br):
        m1 = f"\nITERATION AT INDEX: {i}\n"
        m1 += f"\n{bc[i]} : {br[i]} [{type(br[i])}]\n"
        if isinstance(br[i], dict):
            m1 += f"\nFOUND IT AT INDEX: {i}\n"
            parent_column = bc[i]
            m1 += f"\nPARENT COLUMN: {parent_column}\n"
            for k, v in br[i].items():
                nested_column = f"{parent_column}_{k}"
                m1+= f"\nNESTED COLUMN: {nested_column}\n"
                m1+= f"\nNESTED VALUE: {v}\n"
                bc.append(nested_column)
                br.append(v)

            # Remove parent column, value and reiterate
            bc.pop(i)
            br.pop(i)
            SLOG.debug(m1)
            continue

        SLOG.debug(m1)
        i += 1

    # Then, search for lists
    i = 0
    m0 = "\nSEARCHING FOR ARRAY-LIKE STRUCTURES\n"
    m0 += f"BASE COLUMNS : {bc}\n"
    m0 += f"BASE ROWS : {br}\n"
    SLOG.debug(m0)
    while i < len(br):
        m1 = f"\nITERATION AT INDEX: {i}\n"
        m1 += f"\n{bc[i]} : {br[i]} [{type(br[i])}]\n"
        if isinstance(br[i], list):
            m1 += f"\nFOUND IT AT INDEX: {i}\n"
            for e in br[i]:
                bbs = bs[:]
                bbs[1][i] = e 
                m1 += f"\nNEW ROW WITH {bbs[0][i]}: {bbs[1][i]}\n"
                R.append(bbs)

            SLOG.debug(m1)
            continue

        SLOG.debug(m1)
        i += 1

    m0 += "\nROWS IN R :\n"
    for row in R:
        m0 += f"{row}\n"

    SLOG.debug(m0)
    return [[]]



if __name__ == "__main__":
    jason = {
        "rows": [
            {
                "x": "aaaaaaaaaaaaaa",
            },
            {
                "y": "bbbbbbbbbbbbbb"
            }
        ],
        "column": {
            "x": 111111,
            "y": 222222,
            "nested_columns" : {
                "a": 333333,
                "b": 444444,
            }
        },
        "total": 2,
        "values": [
            {
                "links": [
                    {
                        "rel": "self",
                        "uri": "https://sandboxapi.deere.com/platform/partnerships/2b1b34fc-2cc3-4a57-8120-28ea912113fc"
                    },
                    {
                        "rel": "fromPartnership",
                        "uri": "https://sandboxapi.deere.com/platform/organizations/0987"
                    },
                    {
                        "rel": "toPartnership",
                        "uri": "https://sandboxapi.deere.com/platform/organizations/1234"
                    },
                    {
                        "rel": "permissions",
                        "uri": "https://sandboxapi.deere.com/platform/partnerships/2b1b34fc-2cc3-4a57-8120-28ea912113fc/permissions"
                    },
                    {
                        "rel": "contactInvitation",
                        "uri": "https://sandboxapi.deere.com/platform/partnerships/c3cf441b-d814-400b-842c-44fb7ecad703"
                    }
                ],
                "status": "ACCEPTED"
            },
            {
                "links": [
                    {
                        "rel": "self",
                        "uri": "https://sandboxapi.deere.com/platform/partnerships/2b1b34fc-2cc3-4a57-8120-28ea912113fc"
                    },
                    {
                        "rel": "fromPartnership",
                        "uri": "https://sandboxapi.deere.com/platform/organizations/0987"
                    },
                    {
                        "rel": "toPartnership",
                        "uri": "https://sandboxapi.deere.com/platform/organizations/1234"
                    },
                    {
                        "rel": "permissions",
                        "uri": "https://sandboxapi.deere.com/platform/partnerships/2b1b34fc-2cc3-4a57-8120-28ea912113fc/permissions"
                    },
                    {
                        "rel": "contactInvitation",
                        "uri": "https://sandboxapi.deere.com/platform/partnerships/c3cf441b-d814-400b-842c-44fb7ecad703"
                    }
                ],
                "status": "ACCEPTED"
            },
        ]
    }

    tabooit(jason)

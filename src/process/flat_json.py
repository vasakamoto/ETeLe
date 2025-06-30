"""Flattening of a json element with nested arrays and objects in it. The thought 
process is to structure the json into a tabular format.
"""

# TODO
#   * Wrap everything properly
#   * Document properly
#   * Make tests


def _flat_tree(l: list[tuple], i: int=0) -> None:
    """Destructure a nested tree from a list of tuples *l* obtained from an 
    dict_items into a flattened tree. The index *i* is used to traverse the tree.
    """

    # Instaciate key *k* and value *v* from a dict_items object
    k, v = l[i]

    # If value *v* is a dictionary, remove node at index *i*, destructure dictionary
    # into a dict_items and append the tuples into *l*
    if isinstance(v, dict):
        l.pop(i)
        for k_n, v_n in v.items():
            l.append((f"{k}_{k_n}", v_n))

        # Retraverse flattened tree to destructure 2nd degree and deeper nodes 
        # appended into *l*
        _flat_tree(l)

    # Continue traverse to the others first degree nodes
    try:
        _flat_tree(l, i+1)

    # Stop after last node
    except IndexError:
        return


def _multiply_tree(l: list[tuple], R: list[list], i: int=0) -> None:
    """Search for arrays in the tree, if an array with n elements *e* is found, multiply 
    multiply the tree by n.
    """

    # Instaciate key *k* and value *v* from a dict_items object
    k, v = l[i]

    # If value *v* is a list, duplicate list and change the list value *v* for the
    # value *e*, append new tree into *R* list, do it n times and stop traversal
    if isinstance(v, list) and len(v) > 0:
        for e in v:
            c = l[:]
            c[i] = (k, e)
            c.sort()
            R.append(c)
        return

    # Continue traverse to the others first degree nodes
    try:
        _multiply_tree(l, R, i+1)

    # Stop after last node
    except IndexError:
        return


def flat_json(l: list[tuple], R: list, i: int=0) -> None:
    if i == 0 and len(R) < 1:
        _flat_tree(l)
        _multiply_tree(l, R)
        flat_json(R[i], R, i)

    if i >= len(R):
        return

    _flat_tree(R[i])
    _multiply_tree(R[i], R)
    flat_json(R[i], R, i+1)


def _flat_treev2(j : dict, d : int):



if __name__ == "__main__":
    jason = {
        "links": [
        {
            "rel": "self",
            "uri": "https://sandboxapi.deere.com/platform/partnerships"
        }
        ],
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
                        "uri": "https://sandboxapi.deere.com/platform/partnerships/4ecbb066-bd4c-485e-bcf8-99a470364d5a"
                    },
                    {
                        "rel": "fromPartnership",
                        "uri": "https://sandboxapi.deere.com/platform/organizations/7654"
                    },
                    {
                        "rel": "toPartnership",
                        "uri": "https://sandboxapi.deere.com/platform/organizations/1234"
                    },
                    {
                        "rel": "permissions",
                        "uri": "https://sandboxapi.deere.com/platform/partnerships/4ecbb066-bd4c-485e-bcf8-99a470364d5a/permissions"
                    },
                    {
                        "rel": "contactInvitation",
                        "uri": "https://sandboxapi.deere.com/platform/partnerships/47f27b3a-2639-4bc4-a1c3-33dc0bce32ac"
                    }
                ],
                "status": "ACCEPTED"
            }
        ]
    }


    R = []
    l = list(jason.items())
    flat_json(l, R)
    for r in R[:-11]:
        print("\n________________________________________________\n")
        print(r)

    R.clear()
    print("\n################################################\n")
        #for t in r:
        #    print(t)

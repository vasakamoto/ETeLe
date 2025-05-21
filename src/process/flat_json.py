"""Flattening of an entire json with nested arrays and objects in it. The thought 
process is to structure the json into a tabular format.
"""

import json
import os

# TODO
#   * Wrap everything properly
#   * Document properly
#   * Make tests


# Matrix to store the json "rows"
R = []


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



def _multiply_tree(l: list[tuple], R: list[list], i: int=0):
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


if __name__ == "__main__":
    path = "C:/Pogramacao/rascunhos/pitao/json_mocks"
    for entry in os.listdir(path):
        print(f"\n\nFILE {entry}")
        with open(os.path.join(path, entry), "r") as file:
            jason =  json.load(file)

        l = list(jason.items())
        flat_json(l, R)
        for r in R:
            print("\n________________________________________________\n")
            print(r)

        R.clear()
        print("\n################################################\n")
            #for t in r:
            #    print(t)

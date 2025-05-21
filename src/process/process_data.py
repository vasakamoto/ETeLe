"""Process handler"""

from .flat_json import flat_json
from .transpose import transpose_flat_json


def process_json(j : dict, R : list) -> list[tuple]:
    e = list(j.items())
    flat_json(e, R)  
    
    return transpose_flat_json(R) 

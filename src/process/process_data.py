"""Process handler"""

from .flat_json import flat_json
from .transpose import transpose_flat_json
from .sanitize_data import sanitize

def process_json(j : dict, R : list) -> None:
    e = list(j.items())
    flat_json(e, R)  
    sanitize(R)
    transpose_flat_json(R) 
    

if __name__ == "__main__":
    R = []
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
    process_json(jason, R)

    for row in R:
        print(row)

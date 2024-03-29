from fastapi import FastAPI
from pydantic import BaseModel

from src.api_modules.main_module import find_terms


class SimpleRequest(BaseModel):
    language: str
    values: list[str]

class Position(BaseModel):
    start: int
    end: int


class Target(BaseModel):
    language: str
    literal: str
    position: Position


class SimpleResponse(BaseModel):
    body: str
    target: Target


app = FastAPI()


@app.post('/')
async def simple_request(request: SimpleRequest) -> list[SimpleResponse]:
    request_json = request.json()

    # Extracting the necessary information from the request
    context = request_json['@context']
    limitPerPredicate = request_json['params']['limitPerPredicate']
    language = request_json['params']['language']
    provenance = request_json['params']['provenance']
    total_items = request_json['totalItems']
    items = request_json['items']

    ''' 
    The doc details dict will have as key a value to be debiased.
    The value corresponding to the key is a list of dictionaries, each containing the item_id
    and the property of the item that the value belongs to.
    The reason we need a list is because if in the request we have the same value for different
    records, we need to keep track of which property the value belongs to.
    
    Example:
    Request:
    "items" : [
        {
        "id": "12345/XPTO",
        "dc:title": [ "a sample title", "a second sample title" ],
        "dc:description": [ "a sample description", "a second sample description" ]
        },
        {
        "id": "12345/XPTO_2",
        "dc:title": [ "another sample title", "another second sample title" ],
        "dc:description": [ "a sample title", "another second sample description" ]
        },
    ]
    doc_details = {
        "a sample title": [ { "item_id": "12345/XPTO", "property": "dc:title" }, { "item_id": "12345/XPTO_2", "property": "dc:description" }],
        "a second sample title": [ { "item_id": "12345/XPTO", "property": "dc:title" } ],
        "a sample description": [ { "item_id": "12345/XPTO", "property": "dc:description" } ],
        "a second sample description": [ { "item_id": "12345/XPTO", "property": "dc:description" } ],
        "another sample title": [ { "item_id": "12345/XPTO_2", "property": "dc:title" } ],
        "another second sample title": [ { "item_id": "12345/XPTO_2", "property": "dc:title" } ],
        "another second sample description": [ { "item_id": "12345/XPTO_2", "property": "dc:description" } ]
    }

'''

    doc_details = {}
    for item in items:
        # the keys of the request e.g. dc:description (item properties) are not predefined
        # so we need to get them dynamically
        dict_keys = item.keys()
        id = item['id']
        dict_keys_cleaned = [key for key in dict_keys if key != 'id']
        for key in dict_keys_cleaned:
            val_lst = item[key]
            for val in val_lst:
                if val not in doc_details:
                   doc_details[val] = []
                doc_details[val].append({'item_id': id, 'property': key})
    
    ''' instead of raw text, we need to pass the doc_details dict to the find_terms function
        so that we can keep reference of which term belongs to which record
    '''
    filtered_matches = find_terms(doc_details, language)
    return filtered_matches

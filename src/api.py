import uuid
from itertools import groupby, islice
from pprint import pprint

from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware


from src.utils.api_helper_classes import *

from src.api_modules.main_module import find_terms

app = FastAPI()
app.add_middleware(GZipMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post('/simple')
async def simple_request(request: SimpleRequest) -> SimpleResponse:
    docs = request.values
    language = request.language
    filtered_matches = find_terms(docs, language, RequestMode.SIMPLE)
    response = {
        "metadata": {
            "annotator": "de-bias",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        },
        "results": filtered_matches
    }
    return response


@app.post('/')
async def detailed_request(request: DetailedRequest) -> DetailedResponse:
    """
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
    "doc_details" = {
        "a sample title": [ { "item_id": "12345/XPTO", "property": "dc:title" }, { "item_id":
        "12345/XPTO_2", "property": "dc:description" }],
        "a second sample title": [ { "item_id": "12345/XPTO", "property": "dc:title" } ],
        "a sample description": [ { "item_id": "12345/XPTO", "property": "dc:description" } ],
        "a second sample description": [ { "item_id": "12345/XPTO", "property": "dc:description"
        } ],
        "another sample title": [ { "item_id": "12345/XPTO_2", "property": "dc:title" } ],
        "another second sample title": [ { "item_id": "12345/XPTO_2", "property": "dc:title" } ],
        "another second sample description": [ { "item_id": "12345/XPTO_2", "property":
        "dc:description" } ]
    }
    """
    # pprint(request.model_dump())
    language = request.params.language
    limit_per_predicate = request.params.limit_per_predicate
    items = request.items
    flattened_items = [
        (field_value, field_name, item['id'])
        for item in items
        for field_name in item.keys() - {'id'}
        for field_value in item[field_name]
    ]
    # pprint(flattened_items)
    filtered_matches = find_terms(
        [item[0] for item in flattened_items], language, RequestMode.DETAILED
    )
    # print('filtered matches:')
    # pprint(filtered_matches)
    flattened_matches = [(item, match)
                         for item, matches in zip(flattened_items, filtered_matches)
                         for match in matches]
    # print('flattened_matches')
    # pprint(flattened_matches)
    matches_by_item_and_uri = groupby(sorted(flattened_matches,
                                             key=lambda x: (x[0][2], x[1].term_uri, x[0][1])),
                                      key=lambda x: (x[0][2], x[1].term_uri))
    # pprint(matches_by_item_and_term)

    response = {
        "@context": request.context,
        "type": "AnnotationPage",
        "partOf": {
            "type": "AnnotationCollection",
            "modified": datetime.now()
        }
    }
    response_items = [
        {
            # "id": str(uuid.uuid4()),
            "type": "Annotation",
            "motivation": "highlighting",
            "body": key[1],
            "target": [
                {
                    "source": item[2],
                    "selector": {
                        "type": "RDFStatementSelector",
                        "hasPredicate": predicate,
                        "refinedBy": {
                            "type": "TextQuoteSelector",
                            "exact": {
                                "@value": match.text,
                                "@language": language
                            },
                            "prefix": match.prefix,
                            "suffix": match.suffix
                        }
                    }
                }
                # for item, match in group
                for predicate, predicate_group in groupby(group, key=lambda x: x[0][1])
                for item, match in islice(predicate_group, limit_per_predicate)
            ]
        }
        for key, group in matches_by_item_and_uri
    ]

    response["items"] = response_items
    return response

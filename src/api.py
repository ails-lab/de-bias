from enum import Enum
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel, Field

from typing import List, Optional

from src.api_modules.main_module import find_terms

class RequestParams(BaseModel):
    limitPerPredicate: int
    language: str
    provenance: bool

class DetailedRequest(BaseModel):
    context: list = Field(alias="@context")
    type: str
    params: RequestParams
    total_items: int = Field(alias="totalItems")
    items: list

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

class RequestMode(Enum):
    SIMPLE = 1,
    DETAILED = 2

class DetailedResponsePartOf(BaseModel):
    type: str = "AnnotationCollection"
    modified: datetime = datetime.now()

class ItemTargetSelectorRefinedByExact(BaseModel):
    value: str = Field(alias="@value")
    language: Optional[str] = Field(alias="@language")

class ItemTargetSelectorRefinedBy(BaseModel):
    type: str = 'TextQuoteSelector'
    exact: ItemTargetSelectorRefinedByExact

class ItemTargetSelector(BaseModel):
    type: str = 'RDFStatementSelector'
    predicate: str
    refined_by: ItemTargetSelectorRefinedBy = Field(alias="refinedBy")
    prefix: Optional[str]
    suffix: Optional[str]

class DetailedResponseItemTarget(BaseModel):
    source: str
    selector: ItemTargetSelector

    def __init__(self, source, predicate, value, language = None, prefix = None, suffix = None):
        selector = ItemTargetSelector()
        selector.predicate = predicate
        refined_by = ItemTargetSelectorRefinedBy()
        exact = ItemTargetSelectorRefinedByExact()
        exact.value = value
        exact.language = language
        refined_by.exact = exact
        selector.refined_by = refined_by
        selector.prefix = prefix
        selector.suffix = suffix
        self.source = source
        self.selector = selector
        

class DetailedResponseItem(BaseModel):
    id: str
    type: str
    motivation: str
    body: str
    target: DetailedResponseItemTarget

class DetailedResponse(BaseModel):
    context: list = Field(alias="@context")
    type: str = "AnnotationPage"
    part_of: DetailedResponsePartOf = Field(alias= "partOf")
    items: list[DetailedResponseItem]

app = FastAPI()


@app.post('/simple')
async def simple_request(request: SimpleRequest) -> list[SimpleResponse]:
    docs = request.values
    language = request.language
    filtered_matches = find_terms(docs, language)
    return filtered_matches

@app.post('/')
async def detailed_request(request: DetailedRequest) -> DetailedResponse:

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
    for item in request.items:
        # the keys of the request e.g. dc:description (item properties) are not predefined
        # so we need to get them dynamically
        dict_keys = item.keys() - {'id'}
        id = item['id']
        for key in dict_keys:
            val_lst = item[key]
            for val in val_lst:
                if val not in doc_details:
                   doc_details[val] = []
                doc_details[val].append({'item_id': id, 'property': key})
    
    ''' instead of raw text, we need to pass the doc_details dict to the find_terms function
        so that we can keep reference of which term belongs to which record
    '''
    filtered_matches = find_terms(doc_details, request.language, RequestMode.DETAILED)

    response = DetailedResponse()
    response.context = request.context
    response.part_of = DetailedResponsePartOf()
    response.items = filtered_matches
    
    return response

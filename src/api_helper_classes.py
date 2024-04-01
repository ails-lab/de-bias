from pydantic import BaseModel, Field

from typing import List, Optional
from datetime import datetime
from enum import Enum

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

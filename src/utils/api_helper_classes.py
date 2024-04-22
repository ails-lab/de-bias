from dataclasses import dataclass

from pydantic import BaseModel, Field

from typing import Literal
from datetime import datetime
from enum import Enum


class SimpleRequest(BaseModel):
    language: str
    values: list[str]


class TextSpan(BaseModel):
    start: int
    end: int


class Target(BaseModel):
    language: str
    literal: str
    position: TextSpan


class SimpleResponseMetadata(BaseModel):
    annotator: str
    thesaurus: str | None = None
    date: datetime


class SimpleResponseItemTag(BaseModel):
    uri: str
    start: int
    end: int
    length: int


class SimpleResponseItem(BaseModel):
    language: str
    literal: str
    tags: list[SimpleResponseItemTag]


class SimpleResponse(BaseModel):
    metadata: SimpleResponseMetadata
    results: list[SimpleResponseItem]


# class Context(BaseModel):
#     uri: str
#     base: Literal["http://data.europeana.eu/item/"] = Field(alias="@base")


class RequestParams(BaseModel):
    limit_per_predicate: int | None = Field(None, alias="limitPerPredicate")
    language: str
    provenance: bool


class DetailedRequestItem(BaseModel):
    record_id: str = Field(alias="id")


class DetailedRequest(BaseModel):
    context: list = Field(alias="@context")
    type: Literal["Request"]
    params: RequestParams
    total_items: int | None = Field(None, alias="totalItems")
    # items: list[DetailedRequestItem]
    items: list[dict[str, str | list[str]]]


class DetailedResponsePartOf(BaseModel):
    type: Literal["AnnotationCollection"]
    modified: datetime


class ItemTargetSelectorRefinedByExact(BaseModel):
    value: str = Field(alias="@value")
    language: str = Field(alias="@language")


class ItemTargetSelectorRefinedBy(BaseModel):
    type: Literal["TextQuoteSelector"]
    exact: ItemTargetSelectorRefinedByExact
    prefix: str
    suffix: str


class ItemTargetSelector(BaseModel):
    type: Literal["RDFStatementSelector"]
    hasPredicate: str
    refined_by: ItemTargetSelectorRefinedBy = Field(alias="refinedBy")


class DetailedResponseItemTarget(BaseModel):
    source: str
    selector: ItemTargetSelector


class DetailedResponseItem(BaseModel):
    # id: str
    type: Literal["Annotation"]
    motivation: Literal["highlighting"]
    body: str
    target: list[DetailedResponseItemTarget]


class DetailedResponse(BaseModel):
    context: list = Field(alias="@context")
    type: Literal["AnnotationPage"]
    part_of: DetailedResponsePartOf = Field(alias="partOf")
    items: list[DetailedResponseItem]


class RequestMode(Enum):
    SIMPLE = 1,
    DETAILED = 2


@dataclass(frozen=True)
class Match:
    term: str
    start_char: int
    end_char: int
    sentence_index: int
    word_id: int


@dataclass(frozen=True)
class AnnotationMatch:
    term: str
    prefix: str | None
    suffix: str | None
    uri: str

from dataclasses import dataclass

from pydantic import BaseModel, Field

from typing import Optional, Literal
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


class SimpleResponse(BaseModel):
    body: str
    target: Target


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
    items: list


class DetailedResponsePartOf(BaseModel):
    type: Literal["AnnotationCollection"]
    modified: datetime


class ItemTargetSelectorRefinedByExact(BaseModel):
    value: str = Field(alias="@value")
    language: str = Field(alias="@language")


class ItemTargetSelectorRefinedBy(BaseModel):
    type: Literal["TextQuoteSelector"]
    exact: ItemTargetSelectorRefinedByExact


class ItemTargetSelector(BaseModel):
    type: Literal["RDFStatementSelector"]
    predicate: str
    refined_by: ItemTargetSelectorRefinedBy = Field(alias="refinedBy")
    prefix: str | None
    suffix: str | None


class DetailedResponseItemTarget(BaseModel):
    source: str
    selector: ItemTargetSelector
    #
    # def __init__(self, source, predicate, value, language=None, prefix=None, suffix=None):
    #     selector = ItemTargetSelector()
    #     selector.predicate = predicate
    #     refined_by = ItemTargetSelectorRefinedBy()
    #     exact = ItemTargetSelectorRefinedByExact()
    #     exact.value = value
    #     exact.language = language
    #     refined_by.exact = exact
    #     selector.refined_by = refined_by
    #     selector.prefix = prefix
    #     selector.suffix = suffix
    #     self.source = source
    #     self.selector = selector


class DetailedResponseItem(BaseModel):
    id: str
    type: Literal["Annotation"]
    motivation: Literal["highlighting"]
    body: str
    target: DetailedResponseItemTarget


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
    prefix: str
    suffix: str

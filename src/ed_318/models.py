from datetime import datetime, time
from typing import Annotated, Any

import geojson_pydantic as geojson
from pydantic import AnyUrl, BaseModel, EmailStr, Field

from .geometries import Geometry
from .types import (
    CodeAuthorityRole,
    CodeCountryISOType,
    CodeDaylightEventType,
    CodeWeekdayType,
    CodeYesNoType,
    CodeZoneIdentifierType,
    CodeZoneReasonType,
    CodeZoneType,
    CodeZoneVariantType,
    TextShortType,
    URNType,
)


class DailyPeriod(BaseModel):
    day: Annotated[list[CodeWeekdayType], Field(min_length=1, max_length=7)]
    startTime: time | None = None
    startEvent: CodeDaylightEventType | None = None
    endTime: time | None = None
    endEvent: CodeDaylightEventType | None = None


class TimePeriod(BaseModel):
    startDateTime: datetime | None = None
    endDateTime: datetime | None = None
    schedule: list[DailyPeriod] | None = None


class DatasetMetadata(BaseModel):
    provider: list[TextShortType] | None = None
    issued: datetime | None = None
    validFrom: datetime | None = None
    description: list[TextShortType] | None = None
    validTo: datetime | None = None
    otherGeoid: URNType | None = None
    technicalLimitation: list[TextShortType] | None = None


class Authority(BaseModel):
    """
    A relevant authority that is in charge for authorizing, being notified or providing information for
    UAS operations in the UAS Geographical Zone.
    """

    name: Annotated[list[TextShortType], Field(min_length=1)] | None = None
    service: Annotated[list[TextShortType], Field(min_length=1)] | None = None
    contactName: Annotated[list[TextShortType], Field(min_length=1)] | None = None
    siteURL: AnyUrl | None = None
    email: EmailStr | None = None
    phone: Annotated[str, Field(max_length=200)] | None = None
    purpose: CodeAuthorityRole
    intervalBefore: TimePeriod | None = None


class UASZoneVersion(BaseModel):
    """
    A specific version of an airspace of defined dimensions, above the land areas or territorial
    waters of a State, within which a particular restriction or condition for UAS flights applies.
    """

    identifier: CodeZoneIdentifierType
    country: CodeCountryISOType
    name: Annotated[list[TextShortType], Field(min_length=1)] | None = None
    type: CodeZoneType
    variant: CodeZoneVariantType
    restrictionConditions: str | None = None
    region: int | None = None
    reason: Annotated[list[CodeZoneReasonType], Field(max_length=9)] | None = None
    otherReasonInfo: list[TextShortType] | None = None
    regulationExemption: CodeYesNoType | None = None
    message: Annotated[list[TextShortType], Field(min_length=1)] | None = None
    zoneAuthority: Annotated[list[Authority], Field(min_length=1)]
    limitedApplicability: list[TimePeriod] | None = None
    extendedProperties: dict[str, Any] | None = None


class Feature(geojson.Feature):
    geometry: Geometry
    properties: UASZoneVersion | None = None


class FeatureCollection(geojson.FeatureCollection[Feature]):
    """ED-318 4.2.2.1 FeatureCollection

    GeoJSON FeatureCollection containing zero or more GeoJSON Features representing UAS Geographical Zones,
    plus additional foreign members capturing data set information.
    """

    name: Annotated[str, Field(max_length=200)] | None = None
    """A free text name that can be used to identifiy the UAS Geographical Zone data set."""
    metadata: DatasetMetadata
    """Qualification and constraint of the usage of the data in this data set."""

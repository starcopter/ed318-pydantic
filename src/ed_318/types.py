"""
ED-318 4.2.5 Simple Data Models
"""

import re
from datetime import datetime, time, timedelta
from typing import Annotated, Literal

from pydantic import BaseModel, Field

CodeAuthorityRole = Annotated[
    Literal["AUTHORIZATION", "NOTIFICATION", "INFORMATION"],
    Field(description="Role that an authority has in relation with the UAS zone."),
]
"""ED-318 4.2.5.1 CodeAuthorityRole

Allowed Values:
- AUTHORIZATION: The designated authority shall be contacted to get an authorization before accessing the UAS Geographical Zone.
- NOTIFICATION: The designated authority shall be notified of the UAS flight prior to accessing the UAS Geographical Zone.
- INFORMATION: The designated authority is a general purpose point of contact for the UAS in the Zone.
"""

CodeDaylightEventType = Annotated[
    Literal["BMCT", "SR", "SS", "EECT"],
    Field(description="A time identified in relation with an astronomical event, such as sunrise/sunset."),
]
"""ED-318 4.2.5.2 CodeDaylightEventType

Allowed Values:
- BMCT: Beginning of morning civil twilight (center of the sun 6 degrees below the horizon).
- SR: Civil Sunrise.
- SS: Civil Sunset.
- EECT: End of evening civil twilight (center of the sun 6 degrees below the horizon).
"""

UomDistance = Literal["m", "ft"]
"""ED-318 4.2.5.3 UomDistance

Allowed Values:
- m: Meters.
- ft: Feet.
"""

CodeZoneIdentifierType = Annotated[
    str,
    Field(
        min_length=1,
        max_length=7,
        pattern=r"[A-Za-z0-9_\-]{1,7}",
        description="A string that uniquely identifies the area within a geographical scope.",
    ),
]
"""ED-318 4.2.5.4 CodeZoneIdentifierType

A string that uniquely identifies the area within a geographical scope.
"""

CodeCountryISOType = Annotated[
    str,
    Field(
        min_length=3,
        max_length=3,
        description="A 3 letter identifier of a country or territory using the ISO 3166-1 alpha-3 standard.",
    ),
]
"""ED-318 4.2.5.5 CodeCountryISOType

A 3 letter identifier of a country or territory using the ISO 3166-1 alpha-3 standard.
"""

CodeZoneVariantType = Literal["COMMON", "CUSTOMIZED"]
"""ED-318 4.2.5.6 CodeZoneVariantType

Allowed Values:
- COMMON: The zone is provided with its common definition, valid for any UAS and operator.
- CUSTOMIZED: The zone is provided with a customised definition, for a particular UAS or operator.
  This is a design provision that could be used for example to provide waivers to specific users
  with restrictions removed on given zones for specific purposes. This information enables them to
  identify it is not the common version which has been transferred.
"""

CodeZoneType = Literal["USPACE", "PROHIBITED", "REQ_AUTHORIZATION", "CONDITIONAL", "NO_RESTRICTION"]
"""ED-318 4.2.5.7 CodeZoneType

Allowed Values:
- USPACE: Indicates a zone subject to the requirements of Regulation EU 664/2021.
- PROHIBITED: Indicates that the flight of UAS is prohibited during the applicability time.
- REQ_AUTHORIZATION: Indicates that the flight of UAS is subject to explicit authorization requirements during the
  time of applicability. Note that one Authority contact with role Authorization should be provided in this case.
- CONDITIONAL: Indicates that access in the UAS Geographical Zone is allowed only to operators fulfilling a
  special condition, which is defined as a logical expression.
- NO_RESTRICTION: Indicates that the zone may be used during the applicability time without any restrictions.
"""

ConditionExpressionType = Annotated[
    str,
    Field(
        max_length=10_000,
        description="Coded expression that provides information about what is authorized/forbidden in a zone "
        "that has conditional access.",
    ),
]
"""ED-318 4.2.5.8 ConditionExpressionType

A coded expression that provides information about what is authorized/forbidden in a zone with conditional access.
By difference with the "Message" field per zone, this coded expression is made to be interpreted by a machine,
while the "Message" field is to be interpreted by a human.
"""

CodeZoneReasonType = Annotated[
    Literal["AIR_TRAFFIC", "SENSITIVE", "PRIVACY", "POPULATION", "NATURE", "NOISE", "EMERGENCY", "DAR", "OTHER"],
    Field(description="An indication of a reason that justifies the existence of an UAS Zone."),
]
"""ED-318 4.2.5.9 CodeZoneReasonType

Allowed Values:
- AIR_TRAFFIC: Due to the presence of air traffic.
- SENSITIVE: Due to the presence of a sensitive site, in the vicinity of which the presence of drones could be
  considered a potential threat.
- PRIVACY: Due to the presence of a site for which the presence of drones could raise privacy concerns.
- POPULATION: Due to the presence of a significantly populated area.
- NATURE: Due to the presence of a wildlife/nature sanctuary or another area with sensitive nature/fauna.
- NOISE: Due to noise abatement regulations.
- EMERGENCY: Due to events related to a situation that requires urgent intervention (such as an accident).
- DAR: Due to the application of a dynamic airspace reconfiguration in a U-space volume, temporarily segregating
  the zone for UAS operations.
- OTHER: Due to another reason, which may be specified in the reasonInfo property.
"""


class TextShortType(BaseModel):
    """ED-318 4.2.5.10 TextShortType

    A free text with a maximum length of 200 characters, optionally accompanied
    by an indication of the language in which the text is written.
    """

    text: Annotated[str, Field(max_length=200)]
    lang: Annotated[str, Field(max_length=5, pattern=r"^[a-z]{2}-[A-Z]{2}$")] | None = None


class TextLongType(BaseModel):
    """ED-318 4.2.5.11 TextLongType

    A free text with a maximum length of 1000 characters, optionally accompanied
    by an indication of the language in which the text is written.
    """

    text: Annotated[str, Field(max_length=1_000)]
    lang: Annotated[str, Field(max_length=5, pattern=r"^[a-z]{2}-[A-Z]{2}$")] | None = None


CodeWeekdayType = Annotated[
    Literal["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN", "ANY"],
    Field(description="A day of the week."),
]
"""ED-318 4.2.5.12 CodeWeekdayType

Allowed Values:
- MON: Monday.
- TUE: Tuesday.
- WED: Wednesday.
- THU: Thursday.
- FRI: Friday.
- SAT: Saturday.
- SUN: Sunday.
- ANY: Any day of the week.
"""

DateTimeType = Annotated[
    datetime,
    Field(description="A date and time instant, represented as a string in the format specified by RFC 3339."),
]
"""ED-318 4.2.5.13 DateTimeType

A date and time instant, represented as a string in the format specified by RFC 3339.

Examples:
- 1990-12-31T15:30:00.00Z
- 1990-12-31T15:30:00.00-08:00 (offset of -8 hours from UTC)

Note: Although ISO 8601 permits the hour to be "24", RFC 3339 only allows values between "00" and "23" in order to reduce confusion.
"""

TimeInterval = Annotated[timedelta, Field(description="A time interval.")]
"""ED-318 4.2.5.14 TimeInterval

A time interval.
TODO: format using ISO 8601 PnnDTnnHnnM format.
"""

TimeType = Annotated[time, Field(description="Time with time zone.")]
"""ED-318 4.2.5.15 TimeType

Time with time zone.
TODO: format using ISO 8601 Tnn:nn:nn(Z|+nn:nn) format.
"""

CodeYesNoType = Annotated[Literal["YES", "NO"], Field(description="A boolean value.")]
"""ED-318 4.2.5.16 CodeYesNoType

Allowed Values:
- YES: True.
- NO: False.
"""

URNType = Annotated[str, Field(pattern=re.compile(r"^urn:.+:.*$", re.IGNORECASE))]
"""ED-318 4.2.5.17 URNType

Must comply with the URN syntax defined in RFC 2141.
"""

from __future__ import annotations

from typing import Annotated, Literal, Union

import geojson_pydantic as geojson
from pydantic import BaseModel, Field

from .types import UomDistance

CodeVerticalReferenceType = Literal["AGL", "AMSL", "WGS84"]
"""ED-318 4.2.3.3 CodeVerticalReferenceType

Allowed Values:
- AGL: Height above ground/surface level
- AMSL: Altitude above Mean Sea Level as defined by EGM-96 or a geoid model specified in the dataset metadata
- WGS84: Height above the WGS-84 ellipsoid
"""


class HorizontalExtent(BaseModel):
    """ED-318 4.2.3.1 HorizontalExtent

    Extension to GeoJSON which provides the possibility to specify a horizontal "circle" extent for a Point geometry.
    """

    subType: Literal["Circle"]
    radius: float
    """Distance, in meters, from the associated point along the
    WGS84 ellipsoidal surface of the Earth that this geometry extends."""


class VerticalLayer(BaseModel):
    """ED-318 4.2.3.2 VerticalLayer

    Extension to GeoJSON which provides a vertical extent to all standard GeoJSON geometries.
    """

    upper: float
    """The value of the upper limit of the UAS Geographical Zone expressed in a unit of measurement specified in uom,
    in relation with the vertical datum specified in the upperReference member."""
    upperReference: CodeVerticalReferenceType
    """The vertical reference for the upper limit of the UAS Geographical Zone."""
    lower: float
    """The value of the lower limit of the UAS Geographical Zone expressed in a unit of measurement specified in uom,
    in relation with the vertical datum specified in the lowerReference member."""
    lowerReference: CodeVerticalReferenceType
    """The vertical reference for the lower limit of the UAS Geographical Zone."""
    uom: UomDistance = "m"
    """The unit of measurement in which the upper and lower values are expressed (m) or (ft)."""


class _LayeredGeometryMixin(BaseModel):
    layer: VerticalLayer


class Point(geojson.Point, _LayeredGeometryMixin):
    extent: HorizontalExtent | None = None


class MultiPoint(geojson.MultiPoint, _LayeredGeometryMixin):
    pass


class LineString(geojson.LineString, _LayeredGeometryMixin):
    pass


class MultiLineString(geojson.MultiLineString, _LayeredGeometryMixin):
    pass


class Polygon(geojson.Polygon, _LayeredGeometryMixin):
    pass


class MultiPolygon(geojson.MultiPolygon, _LayeredGeometryMixin):
    pass


class GeometryCollection(geojson.GeometryCollection):
    geometries: list[Geometry]


Geometry = Annotated[
    Union[
        Point,
        MultiPoint,
        LineString,
        MultiLineString,
        Polygon,
        MultiPolygon,
        GeometryCollection,
    ],
    Field(discriminator="type"),
]

GeometryCollection.model_rebuild()

from pathlib import Path

import pytest
from pydantic import ValidationError

from ed_318.models import Authority, Feature, FeatureCollection, TimePeriod, UASZoneVersion

data_path = Path("test/data")


@pytest.mark.parametrize("path", data_path.glob("Example_*.json"))
def test_parse_feature_collection(path: Path):
    collection = FeatureCollection.model_validate_json(path.read_text())
    assert isinstance(collection, FeatureCollection)


def test_parse_ALTER_feature_collection():
    path = data_path / "UGZ_ED-318.json"
    collection = FeatureCollection.model_validate_json(path.read_text())
    assert isinstance(collection, FeatureCollection)


def test_parse_invalid_feature_collection():
    path = data_path / "InvalidExample_GeoZone_2_Layers.json"
    with pytest.raises(ValidationError):
        FeatureCollection.model_validate_json(path.read_text())


def test_parse_feature():
    path = data_path / "PartialExample_featureGeoJSON.json"
    feature = Feature.model_validate_json(path.read_text())
    assert isinstance(feature, Feature)


def test_parse_uas_zone_properties():
    path = data_path / "PartialExample_GeoZoneProperties.json"
    properties = UASZoneVersion.model_validate_json(path.read_text())
    assert isinstance(properties, UASZoneVersion)


def test_parse_time_period():
    path = data_path / "PartialExample_TimePeriod.json"
    time_period = TimePeriod.model_validate_json(path.read_text())
    assert isinstance(time_period, TimePeriod)


def test_parse_zone_authority():
    path = data_path / "PartialExample_ZoneAuthority.json"
    zone_authority = Authority.model_validate_json(path.read_text())
    assert isinstance(zone_authority, Authority)

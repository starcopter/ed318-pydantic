from pathlib import Path

import pytest

from ed_318.models import Feature, FeatureCollection

data_path = Path("test/data/enaire")


@pytest.mark.skip(reason="Dataset is horribly broken")
def test_parse_ZGUAS_aero():
    path = data_path / "ZGUAS_Aero.json"
    collection = FeatureCollection.model_validate_json(path.read_text())
    assert isinstance(collection, FeatureCollection)


# @pytest.mark.parametrize("path", sorted((data_path / "features").glob("*.json")))
@pytest.mark.parametrize("path", [data_path / "features/0006-4.fixed.json", data_path / "features/0006-4.json"])
def test_parse_enaire_features(path: Path):
    feature = Feature.model_validate_json(path.read_text())
    assert isinstance(feature, Feature)

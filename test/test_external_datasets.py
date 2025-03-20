from pathlib import Path

import pytest

from ed318_pydantic.models import Feature, FeatureCollection

data_path = Path("test/data")


@pytest.mark.slow
@pytest.mark.parametrize(
    "filename",
    [
        "ZGUAS_Aero.json",
        "ZGUAS_Medioambiente.json",
        "ZGUAS_Urbano.json",
        "ZGUAS_Infra.json",
    ],
)
def test_parse_ENAIRE_dataset(tmp_path: Path, filename: str):
    import urllib.request

    url = f"https://aip.enaire.es/recursos/descargas/ZGUAS/{filename}"
    json_file = tmp_path / filename
    urllib.request.urlretrieve(url, json_file)

    collection = FeatureCollection.model_validate_json(json_file.read_text())
    assert isinstance(collection, FeatureCollection)


@pytest.mark.parametrize("path", sorted((data_path / "ENAIRE/features").glob("*.json")))
def test_parse_enaire_features(path: Path):
    feature = Feature.model_validate_json(path.read_text())
    assert isinstance(feature, Feature)


def test_parse_ALTER_feature_collection():
    path = data_path / "ALTER/UGZ_ED-318.json"
    collection = FeatureCollection.model_validate_json(path.read_text())
    assert isinstance(collection, FeatureCollection)

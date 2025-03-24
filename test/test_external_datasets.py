from pathlib import Path

import pytest

from ed318_pydantic.models import Feature, FeatureCollection

data_path = Path("test/data")


@pytest.mark.slow
@pytest.mark.parametrize(
    "filename",
    [
        "ZGUAS_Aero.zip",
        "ZGUAS_Medioambiente.zip",
        "ZGUAS_Urbano.zip",
        "ZGUAS_Infra.zip",
    ],
)
def test_parse_ENAIRE_dataset(tmp_path: Path, filename: str):
    import urllib.request
    import zipfile

    url = f"https://aip.enaire.es/recursos/descargas/ZGUAS/{filename}"
    file = tmp_path / filename
    urllib.request.urlretrieve(url, file)
    with zipfile.ZipFile(file, "r") as zip_ref:
        json_files = [f for f in zip_ref.namelist() if f.endswith(".json")]
        if len(json_files) != 1:
            raise ValueError(f"Expected 1 JSON file in {filename}, got {len(json_files)}: {json_files}")
        content = zip_ref.read(json_files[0])

    collection = FeatureCollection.model_validate_json(content)
    assert isinstance(collection, FeatureCollection)


@pytest.mark.parametrize("path", sorted((data_path / "ENAIRE/features").glob("*.json")))
def test_parse_enaire_features(path: Path):
    feature = Feature.model_validate_json(path.read_text())
    assert isinstance(feature, Feature)


def test_parse_ALTER_feature_collection():
    path = data_path / "ALTER/UGZ_ED-318.json"
    collection = FeatureCollection.model_validate_json(path.read_text())
    assert isinstance(collection, FeatureCollection)

"""
Check that basic features work.

This file is called by the GitHub Actions workflow to ensure that the package is working.
"""

from ed318_pydantic.models import FeatureCollection

collection_json = """\
{
  "type": "FeatureCollection",
  "name": "Sample UAS GeoZones",
  "metadata": {"validFrom": "2018-12-31T15:59:59Z", "issued": "2018-12-01T15:59:59Z"},
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "GeometryCollection",
        "geometries": [
          {
            "type": "Polygon",
            "coordinates": [
              [
                [2.585866, 49.029301],
                [2.610414, 48.983358],
                [2.731263, 48.987301],
                [2.704141, 49.044704],
                [2.585866, 49.029301]
              ]
            ],
            "layer": {"upper": 150, "upperReference": "AGL", "lower": 50, "lowerReference": "AGL", "uom": "m"}
          },
          {
            "type": "LineString",
            "coordinates": [
              [2.701263, 49.007301],
              [2.664141, 49.034704],
              [2.595866, 49.024301]
            ],
            "layer": {"upper": 50, "upperReference": "AGL", "lower": 0, "lowerReference": "AGL", "uom": "m"}
          }
        ]
      },
      "properties": {
        "identifier": "NFZ6547",
        "country": "FRA",
        "name": [{"text": "LFPG-2", "lang": "en-GB"}],
        "variant": "COMMON",
        "type": "REQ_AUTHORIZATION",
        "reason": ["AIR_TRAFFIC", "OTHER"],
        "otherReasonInfo": [
          {"text": "Flying Whales - part 2", "lang": "en-GB"},
          {"text": "Baleines Volantes 2-\u00e8me partie", "lang": "fr-BE"}
        ],
        "limitedApplicability": [
          {
            "startDateTime": "2018-12-31T15:59:59Z",
            "endDateTime": "2019-12-31T15:59:59Z",
            "schedule": [
              {"day": ["ANY"], "startTime": "16:00:00Z", "endTime": "17:00:00Z"},
              {"day": ["SUN"], "startTime": "10:00:00Z", "endTime": "12:00:00Z"}
            ]
          }
        ],
        "zoneAuthority": [
          {
            "name": [{"text": "LFPG-UASZoneManager", "lang": "en-US"}],
            "email": "UASZoneManager@lfpg.fr",
            "purpose": "AUTHORIZATION"
          }
        ]
      }
    },
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [2.636866, 50.122901],
        "extent": {"subType": "Circle", "radius": 3500},
        "layer": {"upper": 150, "upperReference": "AGL", "lower": 50, "lowerReference": "AGL", "uom": "m"}
      },
      "properties": {
        "identifier": "ABC1234",
        "country": "FRA",
        "name": [{"text": "Fictitious circle", "lang": "en-GB"}],
        "variant": "COMMON",
        "type": "PROHIBITED",
        "reason": ["POPULATION", "NATURE"],
        "otherReasonInfo": [
          {"text": "Castle and nature reserve", "lang": "en-GB"},
          {"text": "Chateau et parc", "lang": "fr-BE"}
        ],
        "zoneAuthority": [
          {
            "name": [{"text": "LFPG-UASZoneManager", "lang": "en-US"}],
            "email": "UASZoneManager@lfpg.fr",
            "purpose": "INFORMATION"
          }
        ]
      }
    }
  ]
}
"""

if __name__ == "__main__":
    collection = FeatureCollection.model_validate_json(collection_json)
    print("🎉 JSON successfully validated, package is working")

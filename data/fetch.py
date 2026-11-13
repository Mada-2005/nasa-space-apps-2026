"""Lane C: download a SMALL real slice of the official challenge data and cache it.

Rules:
- Start with the smallest slice that tells the story (one region, one or two years).
- Cache everything in data/cache/ (gitignored). Never re-download in the demo.
- Write the tidy table to data/processed/features.parquet with at least:
  id, lat, lon, time, target, and feature columns. Lane A trains on it.
- Add every dataset you touch to docs/REFERENCES.md immediately.

Useful NASA access paths (pick what the challenge statement points to):
- earthaccess (pip install earthaccess): search + download from NASA Earthdata / CMR.
  Needs a free Earthdata Login; put credentials in .env, never in git.
- FIRMS (fire hot spots, MODIS + VIIRS): CSV downloads with a free MAP_KEY.
- IRSA (SPHEREx and other infrared sky data): astroquery / pyvo.
- NASA POWER (weather and solar for any lat/lon): simple JSON API, no key.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "data" / "cache"
PROCESSED = ROOT / "data" / "processed"


def fetch() -> None:
    CACHE.mkdir(parents=True, exist_ok=True)
    # TODO: implement for the chosen challenge.
    # Example with earthaccess:
    #   import earthaccess
    #   earthaccess.login(strategy="environment")
    #   results = earthaccess.search_data(short_name="...", bounding_box=(25, 22, 35, 31.5),
    #                                     temporal=("2024-01-01", "2024-12-31"))
    #   earthaccess.download(results[:20], CACHE)
    raise NotImplementedError("Lane C: implement fetch() for the chosen challenge")


def build_features() -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    # TODO: read from CACHE, build the tidy table, write PROCESSED / "features.parquet"
    raise NotImplementedError("Lane C: implement build_features()")


if __name__ == "__main__":
    fetch()
    build_features()

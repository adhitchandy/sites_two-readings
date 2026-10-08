# Two Readings

Thirty photographs, fifteen each by Allison and Adhit, every one edited by both. Published at https://two-readings.adhitchandy.com.

## What is where

- `site/` is the whole website as it is published: `index.html`, `og.jpg`, the icons, and `img/` (each picture three ways: `NN-original`, `NN-adhit`, `NN-allison`; `img/s/` small WebP copies, `img/xl/` large ones). There is no build step: change `site/index.html` and publish.
- `photos/` holds the full-size edits and the raw files (see `photos/README.txt`). It is left out of git and kept in Google Drive.
- `tools/` holds the scripts that made `site/img` from `photos/`. Run them from this folder: `python3 tools/rebuild.py 0 30` remakes the two edits of all thirty pairs, `python3 tools/originals.py 0 30` remakes the unedited versions from the raw files (needs `pip install pillow rawpy`). `meta.py` read details from an older working folder (`tools/pairs/`) that is not kept; its result is `meta.json`.

## Publishing

    npx wrangler deploy

publishes `site/` to two-readings.adhitchandy.com (the setting is in `wrangler.jsonc`).

## Saving a change to GitHub

    ~/Personal/sites/push.sh "what changed"

## On a new computer

1. `cd ~/Personal/sites && git clone https://github.com/adhitchandy/two-readings.git`
2. Download `photos` from Google Drive into `two-readings/photos` (only needed to remake pictures).

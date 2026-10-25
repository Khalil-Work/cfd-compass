# Build the reference

Python 3.10+ builds the catalogue and static directory using the standard library. The PDF additionally uses the pinned packages in `requirements.txt`. Node.js is used only for syntax-checking the client-side search script. No listed solver is installed or run.

```sh
python -m unittest discover -s tests
python tools/validate.py
python tools/design.py
python tools/build.py
python tools/build.py --check
node --check web/app.js
python -m pip install -r requirements.txt
python tools/build_pdf.py
python tools/check_pdf.py
python -m http.server 8080 --directory web
```

Open `http://localhost:8080` for the directory. The PDF is written to `output/pdf/CFD-Compass-Reference.pdf`. Render it with Poppler and inspect pages before releasing:

```sh
pdftoppm -scale-to 1100 -png output/pdf/CFD-Compass-Reference.pdf tmp/pdf/page
```

`tools/refresh_metadata.py` requires authenticated GitHub CLI, or a read-capable `GH_TOKEN`/`GITHUB_TOKEN` in the environment. It resolves redirects and refuses canonical duplicates. It updates the JSON source and metadata snapshot; review the diff, regenerate outputs and run checks before committing. Never store tokens in files.

The scheduled audit only publishes a workflow artifact for review. It does not rewrite catalogue entries, create external messages, or merge changes. GitHub Pages deploys only the static `web/` directory. Fork PRs run read-only catalogue checks; deployment occurs from `main`.

## Visual identity

`tools/design.py` creates the original `assets/hero.svg` and `assets/mark.svg`. They remain editable vector artwork suitable for Illustrator or Inkscape. The shapes are a compass/streamline identity, not a claimed CFD result. The PDF uses matching native vector shapes, fonts and colours.

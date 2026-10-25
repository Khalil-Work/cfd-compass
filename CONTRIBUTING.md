# Help improve CFD Compass

Useful additions, clear corrections and reproducible evidence matter more than list length.

## Suggest a resource

Use the **Suggest a resource** issue form. Include the canonical upstream repository, official documentation, what CFD task it helps with, the licence, and one material limitation. Prefer the original project over a personal fork. A small specialist tool can qualify; star count is not an inclusion threshold.

We accept public-source projects, but distinguish permissive/copyleft licences, source-available restrictions, unknown terms and official mirrors. A project with unclear rights is not described as unrestricted open source. Non-GitHub essentials belong in `data/external.json`.

## Make a catalogue change

1. Edit `data/catalogue.json`; keep one entry per canonical repository and select its main category. Use tags for overlaps.
2. Write a concise original summary, a concrete `best_for` use case, and primary `source_urls`. Describe limitations without repeating untested marketing claims.
3. Set `maturity` to `established`, `research` or `emerging`. This is an editorial classification, not a validation certificate.
4. Refresh repository metadata with `python tools/refresh_metadata.py` (authenticated `gh`, or `GH_TOKEN` for the current environment).
5. Run `python tools/validate.py`, `python -m unittest discover -s tests`, and `python tools/build.py`.
6. Submit a focused PR with the evidence you checked. Generated README, category pages, CSV and website data should match the source JSON.

Do not copy README paragraphs, rehost third-party code, strip authorship, invent benchmark results or add tracking links. Existing upstream names and ownership remain visible. Newly added or renamed repositories need a current metadata record; CI catches missing records and duplicates after canonicalization.

## Report a problem

Use **Correct a resource** for a broken link, licence mistake, inactive project, missing limitation or category error. Include the exact entry and a primary source. Use the repository's security policy for private security reports.

## Review process

Maintainers check scope, canonical ownership, documentation, licence visibility, duplication and the specificity of the description. Inclusion means a resource was catalogued, not that its solver was independently executed or validated. Changes to engineering claims need evidence, not popularity.

By contributing catalogue prose you agree to CC BY 4.0; tooling contributions use MIT. Listed projects retain their own licences and citation requirements.

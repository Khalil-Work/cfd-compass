"""Build Markdown, CSV and searchable static-site data from one catalogue."""
from __future__ import annotations
import argparse
import csv
from datetime import datetime
import html
import io
import json
from pathlib import Path
import shutil
from validate import load, validate, validate_external

ROOT=Path(__file__).resolve().parents[1]
BASE='https://github.com/Khalil-Work/cfd-compass'
SITE='https://khalil-work.github.io/cfd-compass/'


def md(value):return str(value).replace('|','\\|').replace('\n',' ')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    entries,categories,metadata=load()
    errors=validate(entries,categories,metadata)
    if errors:raise SystemExit('\n'.join(errors))
    external=json.loads((ROOT/'data/external.json').read_text(encoding='utf-8'))
    errors=validate_external(external,categories)
    if errors:raise SystemExit('\n'.join(errors))
    snapshot=metadata['checked_at'][:10]
    outputs={}
    enriched=[]
    grouped={c['id']:[] for c in categories}
    for e in entries:
        record=metadata['repositories'][e['repo'].casefold()]
        e={**e,'metadata':record}
        enriched.append(e);grouped[e['category']].append(e)
    for group in grouped.values():group.sort(key=lambda e:e['name'].casefold())
    intro=f'''<p align="center"><img src="assets/hero.svg" width="100%" alt="CFD Compass - an open reference for fluid dynamics"></p>

<p align="center"><strong>Find the right tools for your next flow problem.</strong></p>

<p align="center"><a href="{SITE}"><strong>Browse & filter ↗</strong></a> &nbsp; · &nbsp; <a href="{BASE}/releases/latest/download/CFD-Compass-Reference.pdf"><strong>Download the PDF ↓</strong></a> &nbsp; · &nbsp; <a href="#browse-by-topic">Explore the index</a> &nbsp; · &nbsp; <a href="{BASE}/issues/new/choose">Suggest a resource</a></p>

<p align="center"><a href="{BASE}/actions/workflows/quality.yml"><img src="{BASE}/actions/workflows/quality.yml/badge.svg" alt="Catalogue checks"></a> <a href="LICENSE"><img src="https://img.shields.io/badge/Catalogue-CC_BY_4.0-50ddc8?labelColor=102a3c" alt="Catalogue CC BY 4.0"></a></p>

**{len(entries)} canonical repositories · {len(categories)} topic areas · {len(external)} official external resources**  
Metadata snapshot: **{snapshot}** · [JSON](data/catalogue.json) · [CSV](data/catalogue.csv) · [How entries are checked](docs/METHODOLOGY.md)

CFD Compass brings together software and resources from their original teams: solvers, physical models, numerical methods, geometry, visualization, learning and reproducible workflows. Each entry explains what it helps with, links to upstream documentation, and records selection caveats. All project names and ownership remain with their creators.

## Start with a question

| What are you working on? | A useful route |
| --- | --- |
| A first CFD study | [Learning & benchmarks](#verification-learning) → [General solvers](#general-solvers) → [Selection guide](docs/SELECTION_GUIDE.md) |
| Turbulence or high-fidelity simulation | [DNS / LES / HPC](#turbulence-hpc) → [High-order methods](#high-order) |
| Ignition, combustion, droplets or sprays | [Reacting flows](#reacting-flows) → [Multiphase & spray](#multiphase-spray) |
| Complex geometry and useful results | [Meshing & CAD](#geometry-meshing) → [Visualization & I/O](#visualization) |
| Inverse design or learned models | [Scientific ML & ROM](#learning-rom) → [Optimization & UQ](#automation-uq) |
| Coupled or environmental physics | [Specialist coupling](#coupled-specialist) → [Ocean / atmosphere / wind](#environmental) |

## Browse by topic

'''
    nav=[]
    for c in categories:
        nav.append(f"- {c['icon']} **[{c['title']}](#{c['id']})** · {len(grouped[c['id']])} repositories")
    readme=intro+'\n'.join(nav)+'''

## Read the labels

**Established / research / emerging** are editorial context labels. **Archived** and last-push dates are GitHub metadata. **NOASSERTION** means automated licence identification is inconclusive. **Source-available restrictions and maintenance notices appear in the notes.** Inclusion and passing catalogue CI do not establish scientific accuracy or successful installation. Stars are dated discovery metadata in the searchable directory, not a solver ranking. [Methodology →](docs/METHODOLOGY.md)

---

'''
    for c in categories:
        section=f"<a id=\"{c['id']}\"></a>\n\n## {c['icon']} {c['title']}\n\n{c['description']}\n\n"
        section+='| Project / use case | What it offers | Selection notes |\n| --- | --- | --- |\n'
        for e in grouped[c['id']]:
            r=e['metadata']
            state=' · **archived**' if r['archived'] else ''
            use=f"**[{md(e['name'])}](https://github.com/{e['repo']})**<br>{md(e['best_for'])}"
            desc=md(e['summary'])+f"<br>[Docs]({e['docs_url']}) · `{md(r['license'])}`"
            notes=f"{e['maturity'].capitalize()}{state}"+(f" · {md(e['caveat'])}" if e['caveat'] else '')
            section+=f'| {use} | {desc} | {notes} |\n'
        section+='\n[Back to topics ↑](#browse-by-topic)\n\n'
        readme+=section
        outputs[f'docs/categories/{c["id"]}.md']=section.replace('](#browse-by-topic)',f']({BASE}#browse-by-topic)')+f'\nSnapshot: {snapshot}. [Full index]({BASE}).\n'
    readme+='''## Essential resources beyond GitHub

Some important projects and reference datasets have canonical homes elsewhere. These links avoid substituting unofficial GitHub forks.

| Resource | Role | Access / selection note |
| --- | --- | --- |
'''
    for e in external:readme+=f"| **[{md(e['name'])}]({e['url']})** | {md(e['summary'])} | {md(e['access_note'])} |\n"
    readme+='''
## Use this collection

- **Choose a stack:** [problem-first selection guide](docs/SELECTION_GUIDE.md).
- **Take it offline:** the [versioned PDF reference](https://github.com/Khalil-Work/cfd-compass/releases/latest/download/CFD-Compass-Reference.pdf) includes topic bookmarks, readable entries, selection notes and an alphabetical index.
- **Build on the index:** use the [JSON](data/catalogue.json), [metadata snapshot](data/metadata.json) or [CSV](data/catalogue.csv). See [licensing](LICENSE).
- **Keep it useful:** [suggest a resource or correction](https://github.com/Khalil-Work/cfd-compass/issues/new/choose) with primary evidence. See [contributing](CONTRIBUTING.md).
- **Cite the directory:** use [CITATION.cff](CITATION.cff), and cite the original software/papers separately when you use them.

## Credits & maintenance

Curated by [Khalil](https://github.com/Khalil-Work), with contributions welcome. The linked software is the work of its respective upstream contributors. CFD Compass contains original catalogue descriptions and discovery tools; it does not rehost those codebases or claim their authorship. Catalogue text is CC BY 4.0; repository tooling is MIT; upstream licences remain independent.

This is a growing reference, not an exhaustive inventory or a certification of any linked model. Read the [methodology](docs/METHODOLOGY.md), [security policy](SECURITY.md), and [changelog](CHANGELOG.md).
'''
    outputs['README.md']=readme
    stream=io.StringIO(newline='')
    writer=csv.writer(stream,lineterminator='\n');writer.writerow(['name','repository','category','summary','best_for','maturity','license','language','stars_snapshot','last_push','archived','docs','caveat','tags'])
    for e in enriched:
        r=e['metadata'];writer.writerow([e['name'],r['html_url'],e['category'],e['summary'],e['best_for'],e['maturity'],r['license'],r['language'],r['stargazers_count'],r['pushed_at'],r['archived'],e['docs_url'],e['caveat'],';'.join(e['tags'])])
    outputs['data/catalogue.csv']=stream.getvalue()
    outputs['web/data.json']=json.dumps({'snapshot':snapshot,'categories':categories,'entries':enriched,'external':external},ensure_ascii=False,separators=(',',':'))+'\n'
    outputs['web/catalogue.csv']=stream.getvalue()
    for name in ['hero.svg','mark.svg','social.svg']:outputs['web/assets/'+name]=(ROOT/'assets'/name).read_text(encoding='utf-8')
    stale=[]
    for relative, content in outputs.items():
        dest=ROOT/relative
        if args.check:
            if not dest.exists() or dest.read_text(encoding='utf-8')!=content:stale.append(relative)
        else:
            dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(content,encoding='utf-8',newline='\n')
    if stale:raise SystemExit('Generated files are stale: '+', '.join(stale))
    print(('Checked' if args.check else 'Built')+f' {len(outputs)} files for {len(entries)} repositories.')


if __name__=='__main__':main()

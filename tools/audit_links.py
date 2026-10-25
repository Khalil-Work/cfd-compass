"""Create a bounded read-only audit report; never auto-edit or execute upstreams."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
import json
from pathlib import Path
import urllib.error
import urllib.request
from refresh_metadata import query

ROOT=Path(__file__).resolve().parents[1]


def check(entry):
    result={'repo':entry['repo'],'documentation':entry['docs_url']}
    try:
        live=query(entry['repo'])
        result.update(canonical=live['full_name'],archived=live['archived'],license=live['license'],repository_status='reachable')
        if live['full_name'].casefold()!=entry['repo'].casefold():result['notice']='Repository moved; review its current scope before updating.'
    except Exception as error:result['repository_status']=type(error).__name__
    try:
        request=urllib.request.Request(entry['docs_url'],headers={'User-Agent':'CFD-Compass-link-audit/1.0','Range':'bytes=0-2047'})
        with urllib.request.urlopen(request,timeout=15) as response:
            result.update(documentation_status=response.status,documentation_final_url=response.url)
            response.read(2048)
    except urllib.error.HTTPError as error:result['documentation_status']=error.code
    except Exception as error:result['documentation_status']=type(error).__name__
    return result


def main():
    data=json.loads((ROOT/'data/catalogue.json').read_text(encoding='utf-8'))
    with ThreadPoolExecutor(max_workers=6) as pool:results=list(pool.map(check,data))
    output=ROOT/'output/audit';output.mkdir(parents=True,exist_ok=True)
    payload={'checked_at':datetime.now(timezone.utc).isoformat(),'scope':'Public GitHub API reachability and documentation HTTP access; no installation or numerical validation','results':results}
    (output/'upstream-audit.json').write_text(json.dumps(payload,indent=2),encoding='utf-8')
    uncertain=[r for r in results if r['repository_status']!='reachable' or r.get('notice') or r.get('documentation_status') not in (200,206)]
    text='# Upstream audit\n\nHTTP failures may reflect rate limits, bot filtering or transient TLS/network issues. Review the recorded endpoint; do not assume the project is abandoned.\n\n'
    text+=f'{len(results)} repository/documentation pairs checked; {len(uncertain)} need review.\n\n'
    for r in uncertain:text+=f"- {r['repo']}: repository={r['repository_status']}; docs={r.get('documentation_status')}; {r.get('notice','')}\n"
    (output/'README.md').write_text(text,encoding='utf-8')
    print(f'Audit report written: {len(results)} checked; {len(uncertain)} require review.')


if __name__=='__main__':main()

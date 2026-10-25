"""Create the original editable vector identity; no third-party logo assets."""
from pathlib import Path
import math

ROOT = Path(__file__).resolve().parents[1]


def main():
    paths=[]
    for i in range(16):
        y=60+i*26
        paths.append(f'<path d="M 930 {y} C 1100 {y-120}, 1190 {y+140}, 1600 {y-60}"/>')
    hero=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="460" viewBox="0 0 1600 460" role="img" aria-labelledby="title desc">
<title id="title">CFD Compass</title><desc id="desc">An original compass and streamline mark for the open fluid dynamics reference.</desc>
<defs><linearGradient id="bg"><stop stop-color="#071623"/><stop offset="1" stop-color="#102a3c"/></linearGradient><linearGradient id="fade"><stop stop-color="#50ddc8" stop-opacity=".08"/><stop offset="1" stop-color="#50ddc8" stop-opacity=".32"/></linearGradient></defs>
<rect width="1600" height="460" fill="url(#bg)"/>
<g fill="none" stroke="url(#fade)" stroke-width="1.5">{''.join(paths)}</g>
<g transform="translate(206 224)"><circle r="111" fill="#0c2132" stroke="#335466" stroke-width="2"/><path d="M-69 78 A104 104 0 1 1 79 67" fill="none" stroke="#50ddc8" stroke-width="13" stroke-linecap="round"/><path d="M-75 25 C-30 36,-26 -42,17 -43 C62 -44,42 35,84 23" fill="none" stroke="#f18c72" stroke-width="9" stroke-linecap="round"/><path d="M-20 22 L20-59 L33 18 L-20 22Z" fill="#f3f7f8"/><circle r="7" fill="#071623"/><path d="M0-136V-124 M0 124V136 M-136 0H-124 M124 0H136" stroke="#5c7b8b" stroke-width="3"/></g>
<text x="408" y="224" fill="#f3f7f8" font-family="Arial,Helvetica,sans-serif" font-size="87" font-weight="700" letter-spacing="3">CFD COMPASS</text>
<text x="412" y="283" fill="#b6d1dc" font-family="Arial,Helvetica,sans-serif" font-size="29">An open reference for fluid dynamics</text>
<rect x="412" y="325" width="74" height="4" rx="2" fill="#50ddc8"/>
</svg>'''
    assets=ROOT/'assets';assets.mkdir(exist_ok=True)
    (assets/'hero.svg').write_text(hero,encoding='utf-8')
    social='<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630"><rect width="1200" height="630" fill="#071623"/><svg x="0" y="110" width="1200" height="345" viewBox="0 0 1600 460">'+hero[hero.index('<defs>'):hero.rindex('</svg>')]+'</svg><text x="310" y="505" fill="#65e0cd" font-family="Arial,Helvetica,sans-serif" font-size="18" letter-spacing="2.8">DISCOVER · COMPARE · BUILD</text></svg>'
    (assets/'social.svg').write_text(social,encoding='utf-8')
    mark=hero[hero.index('<g transform="translate(206 224)">'):hero.index('<text x="408"')].replace('translate(206 224)','translate(160 160)')
    (assets/'mark.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="320" height="320" viewBox="0 0 320 320"><rect width="320" height="320" rx="64" fill="#071623"/>'+mark+'</svg>',encoding='utf-8')
    print('Original vector hero and mark created.')


if __name__=='__main__':main()

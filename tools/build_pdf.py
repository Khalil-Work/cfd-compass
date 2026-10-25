"""Build the linked, bookmarked reference edition from the catalogue snapshot."""
from __future__ import annotations
from collections import Counter
import html
import json
from pathlib import Path
import re
import reportlab
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak, KeepTogether, HRFlowable
from reportlab.platypus.tableofcontents import TableOfContents

ROOT=Path(__file__).resolve().parents[1]
NAVY=colors.HexColor('#071623');TEAL=colors.HexColor('#187e78');CORAL=colors.HexColor('#be6247')
INK=colors.HexColor('#183448');MUTED=colors.HexColor('#536d7d');PALE=colors.HexColor('#d8e6eb')
VERSION='1.0.0'


def clean(value):
    return str(value or '').translate(str.maketrans({'\u2011':'-','\u2013':'-','\u2014':'-','\u2212':'-','\u2019':"'",'\u2018':"'",'\u201c':'"','\u201d':'"','\u00a0':' '}))


def esc(value):return html.escape(clean(value))
def link(url,label):return f'<link href="{html.escape(url,quote=True)}" color="#187e78">{esc(label)}</link>'
def slug(repo):return re.sub('[^a-z0-9]+','-',repo.lower())


class ReferenceDoc(BaseDocTemplate):
    def afterFlowable(self,flowable):
        if isinstance(flowable,Paragraph) and hasattr(flowable,'bookmark'):
            key=flowable.bookmark;title=flowable.getPlainText()
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(title,key,level=0,closed=False)
            self.notify('TOCEntry',(0,title,self.page,key))


def main():
    data=json.loads((ROOT/'data/catalogue.json').read_text(encoding='utf-8'))
    cats=json.loads((ROOT/'data/categories.json').read_text(encoding='utf-8'))
    metadata=json.loads((ROOT/'data/metadata.json').read_text(encoding='utf-8'))
    external=json.loads((ROOT/'data/external.json').read_text(encoding='utf-8'))
    date=metadata['checked_at'][:10]
    fonts=Path(reportlab.__file__).parent/'fonts'
    for name,file in [('Compass','Vera.ttf'),('Compass-Bold','VeraBd.ttf'),('Compass-Italic','VeraIt.ttf')]:pdfmetrics.registerFont(TTFont(name,str(fonts/file)))
    pdfmetrics.registerFontFamily('Compass',normal='Compass',bold='Compass-Bold',italic='Compass-Italic',boldItalic='Compass-Bold')
    styles={
      'cover':ParagraphStyle('Cover',fontName='Compass-Bold',fontSize=48,leading=53,textColor=colors.white,spaceAfter=22),
      'coverSub':ParagraphStyle('CoverSub',fontName='Compass',fontSize=17,leading=25,textColor=colors.HexColor('#bad8e0'),spaceAfter=24),
      'coverMeta':ParagraphStyle('CoverMeta',fontName='Compass',fontSize=11,leading=18,textColor=colors.HexColor('#75e4d3')),
      'h1':ParagraphStyle('Chapter',fontName='Compass-Bold',fontSize=23,leading=29,textColor=INK,spaceAfter=17),
      'h2':ParagraphStyle('Subhead',fontName='Compass-Bold',fontSize=13,leading=18,textColor=TEAL,spaceBefore=13,spaceAfter=8),
      'body':ParagraphStyle('Body',fontName='Compass',fontSize=10,leading=15,textColor=INK,spaceAfter=9),
      'entry':ParagraphStyle('Entry',fontName='Compass-Bold',fontSize=12,leading=17,textColor=INK,spaceAfter=5),
      'small':ParagraphStyle('Small',fontName='Compass',fontSize=8.6,leading=13,textColor=MUTED,spaceAfter=5),
      'note':ParagraphStyle('Note',fontName='Compass',fontSize=8.7,leading=13,textColor=CORAL,spaceAfter=5),
      'index':ParagraphStyle('Index',fontName='Compass',fontSize=9,leading=14,textColor=INK,spaceAfter=5)
    }
    out=ROOT/'output/pdf/CFD-Compass-Reference.pdf';out.parent.mkdir(parents=True,exist_ok=True)
    doc=ReferenceDoc(str(out),pagesize=A4,leftMargin=44,rightMargin=44,topMargin=54,bottomMargin=48,
        title='CFD Compass: The Open Fluid Dynamics Reference',author='CFD Compass contributors; curated by Khalil',
        subject='A curated directory of CFD software, methods and research workflows',lang='en',pageCompression=1)
    width,height=A4

    def decorate(canvas,document):
        canvas.saveState()
        if document.page==1:
            canvas.setFillColor(NAVY);canvas.rect(0,0,width,height,fill=1,stroke=0)
            canvas.setStrokeColor(colors.HexColor('#294b60'));canvas.setLineWidth(.5)
            for i in range(12):
                y=110+i*36;path=canvas.beginPath();path.moveTo(width*.45,y);path.curveTo(width*.7,y+110,width*.8,y-100,width+50,y+45);canvas.drawPath(path)
            canvas.setStrokeColor(colors.HexColor('#65e0cd'));canvas.setLineWidth(6);canvas.circle(width-110,height-139,56,stroke=1,fill=0)
            path=canvas.beginPath();path.moveTo(width-146,height-144);path.curveTo(width-120,height-170,width-119,height-105,width-94,height-114);path.curveTo(width-75,height-117,width-90,height-152,width-68,height-147);canvas.setStrokeColor(colors.HexColor('#f18c72'));canvas.setLineWidth(4);canvas.drawPath(path)
            canvas.setFont('Compass',9);canvas.setFillColor(colors.HexColor('#a4c0cc'));canvas.drawString(44,52,'Curated by Khalil  |  github.com/Khalil-Work/cfd-compass')
            canvas.drawString(44,35,'Linked projects remain the work of their original contributors.')
        else:
            canvas.setFillColor(TEAL);canvas.rect(0,height-9,width,9,fill=1,stroke=0)
            canvas.setFont('Compass-Bold',8);canvas.setFillColor(MUTED);canvas.drawString(44,height-31,'CFD COMPASS')
            canvas.setFont('Compass',8);canvas.drawRightString(width-44,height-31,'REFERENCE EDITION  '+VERSION)
            canvas.setStrokeColor(PALE);canvas.setLineWidth(.6);canvas.line(44,35,width-44,35)
            canvas.setFont('Compass',8);canvas.setFillColor(MUTED);canvas.drawString(44,22,'Metadata snapshot '+date);canvas.drawRightString(width-44,22,str(document.page))
        canvas.restoreState()

    frame=Frame(doc.leftMargin,doc.bottomMargin,doc.width,doc.height,id='normal',leftPadding=0,bottomPadding=0,rightPadding=0,topPadding=0)
    doc.addPageTemplates(PageTemplate(id='reference',frames=[frame],onPage=decorate))
    story=[]
    def para(text,style='body'):return Paragraph(text,styles[style])
    def heading(title,key):
        p=para(esc(title),'h1');p.bookmark=key;return p
    story += [Spacer(1,135),para('CFD<br/>COMPASS','cover'),para('An open reference<br/>for fluid dynamics.','coverSub'),Spacer(1,18),para(f'{len(data)} canonical repositories<br/>{len(cats)} topic areas<br/>{len(external)} official external resources','coverMeta'),Spacer(1,30),para(f'Reference edition {VERSION}<br/>Snapshot: {date}','coverMeta'),PageBreak()]
    story += [para('Navigate the reference','h1'),para('Choose a topic below, use the PDF bookmarks, or jump from the alphabetical index to an individual project. Every repository name and documentation label is clickable.'),Spacer(1,12)]
    toc=TableOfContents();toc.levelStyles=[ParagraphStyle('TOC',fontName='Compass',fontSize=10,leading=16,textColor=INK,leftIndent=0,firstLineIndent=0,spaceBefore=6)]
    story += [toc,PageBreak(),heading('Read this first','read-first')]
    for title,text in [
      ('A problem-first directory','This collection helps you discover tools and compare their intended roles. Start with the physical regime, coupled physics, required outputs, geometry and evidence you need. Then consider discretization, compute budget, workflow and adoption constraints.'),
      ('What checking means','Entry scope was reviewed against primary upstream repositories or documentation. GitHub ownership, licence identifiers, archive flags and activity dates were fetched as a dated metadata snapshot. Listed solvers were not all installed, executed or independently validated.'),
      ('Understand the labels','Established, research and emerging are editorial context labels. Stars are dated discovery metadata, not accuracy rankings. A repository push is not necessarily a release. NOASSERTION means the API could not identify a standard licence; inspect the actual terms. Read caveats for official mirrors, maintenance notices and source-available restrictions.'),
      ('Use upstream credit','The software is the work of its original contributors. Follow their licences and cite their publications when using them. This directory provides original catalogue descriptions and discovery tools; it does not redistribute the listed codebases or claim their authorship.'),
      ('Keep the snapshot in context',f'This edition records metadata on {date}. Links, licences and maintenance can change. The live directory and reviewed corrections are available at github.com/Khalil-Work/cfd-compass. Catalogue text is CC BY 4.0; tooling is MIT; upstream terms remain separate.')]:
        story += [para(title,'h2'),para(esc(text))]
    story += [PageBreak(),heading('Choose a stack','choose-stack')]
    routes=[
      ('Learning and first studies','Start with verification/learning, then general solvers. Check dimensions, boundary conditions, stability and grid convergence.'),
      ('Aerodynamics and design','Compare general solvers, high-order methods and optimization tools. Confirm flow regime, turbulence modelling and adjoint consistency.'),
      ('Combustion, sprays and interfaces','Begin with reacting-flow or multiphase tools. Check chemical mechanism validity, stiffness, transport, phase-change assumptions and mass/energy coupling.'),
      ('Turbulence and scale','Inspect DNS/LES resolution, wall treatment, domain and statistical sampling. Compare memory requirements, parallel support and actual precision/hardware constraints.'),
      ('Coupled or environmental problems','Confirm the coupling interfaces, conservation, stability, forcing data, constitutive assumptions and domain/grid nesting.'),
      ('Learned models and inverse studies','Check differentiability assumptions, discrete gradients, training/test separation, out-of-distribution behavior and numerical baselines.')]
    for title,text in routes:story += [para(title,'h2'),para(esc(text))]
    story += [para('Save a reproducibility record','h2'),para('Record the upstream version, mesh, physical parameters and units, initial/boundary conditions, model choices, tolerances, time step or CFL, hardware/precision, environment, post-processing script, comparison data and uncertainty. Reproduce a quantity of interest, not only a visualization.')]
    catnames={c['id']:c['title'] for c in cats}
    for c in cats:
        group=sorted([e for e in data if e['category']==c['id']],key=lambda e:e['name'].casefold())
        story += [PageBreak(),heading(c['title'],c['id']),para(esc(c['description'])),para(f'{len(group)} repositories in this topic.','small'),Spacer(1,8)]
        for e in group:
            r=metadata['repositories'][e['repo'].casefold()]
            uri='https://github.com/'+e['repo']
            card=[para(f'<a name="resource-{slug(e["repo"])}"/>'+link(uri,e['name']),'entry'),para(esc(e['summary'])),para('<b>For:</b> '+esc(e['best_for']),'small')]
            terms=f'{e["maturity"].capitalize()} | {r["language"] or "Mixed / unspecified"} | {r["license"]} | Last push: {str(r["pushed_at"] or "unknown")[:10]}'
            if r['archived']:terms+=' | ARCHIVED'
            card += [para(esc(terms),'small'),para(link(uri,e['repo'])+' &nbsp; / &nbsp; '+link(e['docs_url'],'Documentation'),'small')]
            if e['caveat']:card.append(para('<b>Selection note:</b> '+esc(e['caveat']),'note'))
            card += [Spacer(1,5),HRFlowable(width='100%',thickness=.45,color=PALE),Spacer(1,12)]
            story.append(KeepTogether(card))
    story += [PageBreak(),heading('Essential resources beyond GitHub','external')]
    story += [para('Canonical software homes, experimental datasets and reference portals are included separately when GitHub is not their primary distribution point. Check current access and use terms.')]
    for e in external:
        story.append(KeepTogether([para(link(e['url'],e['name']),'entry'),para(esc(e['summary'])),para(esc(e['access_note']),'note'),para(link(e['url'],e['url']),'small'),Spacer(1,11)]))
    story += [PageBreak(),heading('Alphabetical project index','alphabetical-index'),para('Click a project name to jump to its entry. Category labels describe the main placement; tags in the searchable directory cover overlaps.'),Spacer(1,8)]
    for e in sorted(data,key=lambda e:e['name'].casefold()):
        story.append(para(f'<link href="#resource-{slug(e["repo"])}" color="#187e78"><b>{esc(e["name"])}</b></link> - {esc(catnames[e["category"]])}','index'))
    doc.multiBuild(story)
    print('Built reference PDF:',out)


if __name__=='__main__':main()

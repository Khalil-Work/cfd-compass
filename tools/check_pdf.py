"""Check the shipped PDF has all entries, navigation, links and sane pages."""
import json
from pathlib import Path
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]


def main():
    path=ROOT/'output/pdf/CFD-Compass-Reference.pdf'
    reader=PdfReader(path)
    assert not reader.is_encrypted
    assert len(reader.pages)>=15, 'Reference is unexpectedly short'
    texts=[page.extract_text() or '' for page in reader.pages]
    assert all(text.strip() for text in texts), 'Empty text page'
    # Reuse the PDF authoring normalizer so smart punctuation is compared fairly.
    from build_pdf import clean
    combined='\n'.join(texts)
    entries=json.loads((ROOT/'data/catalogue.json').read_text(encoding='utf-8'))
    missing=[e['name'] for e in entries if clean(e['name']) not in combined]
    assert not missing,missing
    links=0
    for page in reader.pages:
        for annotation in page.get('/Annots',[]):
            obj=annotation.get_object()
            if obj.get('/Subtype')=='/Link':links+=1
    assert links>=len(entries)*2, 'Expected repository and docs links'
    assert reader.outline, 'Expected topic bookmarks'
    print(f'PDF checked: {len(reader.pages)} pages, {links} links, all {len(entries)} entries and bookmarks present.')


if __name__=='__main__':main()

# Sammelt alle sichtbaren Texte und übersetzbaren Attribute aus index.html
from html.parser import HTMLParser
import json, sys
ATTRS = ('alt', 'aria-label', 'title', 'placeholder')
class P(HTMLParser):
    def __init__(s):
        super().__init__(convert_charrefs=True); s.skip = 0; s.out = []
    def handle_starttag(s, tag, attrs):
        if tag in ('script', 'style'): s.skip += 1
        d = dict(attrs)
        for a in ATTRS:
            if d.get(a, '').strip(): s.out.append(d[a].strip())
        if tag == 'meta' and d.get('name') == 'description': s.out.append(d['content'].strip())
    def handle_endtag(s, tag):
        if tag in ('script', 'style'): s.skip -= 1
    def handle_data(s, data):
        if not s.skip and data.strip(): s.out.append(' '.join(data.split()))
p = P(); p.feed(open(sys.argv[1]).read())
seen = []
for x in p.out:
    if x not in seen: seen.append(x)
print(json.dumps(seen, ensure_ascii=False, indent=0))

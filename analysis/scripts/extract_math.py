"""Extract the TeX actually sent to MathJax, including inline table math."""
from html.parser import HTMLParser
from pathlib import Path
import json
import sys
import urllib.request


class MathParser(HTMLParser):
    def __init__(self, page):
        super().__init__(convert_charrefs=True)
        self.page = page
        self.depth = 0
        self.active = None
        self.skip = 0
        self.items = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = attrs.get('class', '').split()
        if self.active is None and 'math' in classes:
            self.active = {'page': self.page, 'id': attrs.get('id'), 'text': ''}
            self.depth = 1
        elif self.active is not None:
            self.depth += 1
            if 'eqno' in classes:
                self.skip = self.depth

    def handle_endtag(self, tag):
        if self.active is not None:
            if self.skip == self.depth:
                self.skip = 0
            self.depth -= 1
            if self.depth == 0:
                text = self.active.pop('text').strip()
                if text.startswith(('\\[', '\\(')) and text.endswith(('\\]', '\\)')):
                    self.active.update(tex=text[2:-2], display=text.startswith('\\['))
                    self.items.append(self.active)
                else:
                    raise ValueError(f'Unrecognized math delimiters: {text}')
                self.active = None

    def handle_data(self, text):
        if self.active is not None and not self.skip:
            self.active['text'] += text


def main():
    repo, root, output = sys.argv[1:]
    manifest = json.loads((Path(repo) / 'analysis/supplement-v2/conversion-manifest.json').read_text())
    pages = [p['page'] for p in manifest['sections']]
    pages += ['intro', 'getting-started', 'references', 'reproducibility']
    items = []
    for page in pages:
        if root.startswith('https://'):
            html = urllib.request.urlopen(root.rstrip('/') + '/' + page + '.html').read().decode()
        else:
            html = (Path(root) / (page + '.html')).read_text()
        parser = MathParser(page)
        parser.feed(html)
        items.extend(parser.items)
    Path(output).write_text(json.dumps(items, indent=2) + '\n')
    print(f'Extracted {len(items)} expressions from {len(pages)} pages.')


if __name__ == '__main__':
    main()

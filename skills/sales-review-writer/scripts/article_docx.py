"""PARASITER article → Word (.docx) with real formatting (№31). Standard library only, no installs.

Usage:
  python3 article_docx.py article.html out.docx [--images DIR]
  python3 article_docx.py --self-test

article.html — the article as simple HTML (what you show in the chat):
  <h1> <h2> <h3> headings (Word styles Heading 1/2/3), <p>, <strong>/<b>, <em>/<i>, <a href> (real hyperlinks),
  <ul>/<ol> with <li> (real Word lists), <table> with <tr>, <th>, <td> (real Word tables), <br>,
  <img src="01-quick-facts.jpg"> (embedded from --images DIR or the HTML's folder; a missing file becomes a
  "[Image: name — insert here]" line), <blockquote> (indented), <hr> (a page-wide rule).
Every product name should already be an <a href="affiliate link"> in the HTML — this script keeps every link.
Prints the path of the .docx.
"""
import html
import os
import re
import struct
import sys
import zipfile
from html.parser import HTMLParser

W = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"'
MAX_EMU = 5486400  # 6 inches: an image never wider than the text column


def esc(t):
    return html.escape(t, quote=False)


def jpeg_size(data):
    """(width, height) of a JPEG from its SOF marker; PNG too. None if unknown."""
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", data[16:24])
    i = 2
    while i < len(data) - 9:
        if data[i] != 0xFF:
            i += 1
            continue
        m = data[i + 1]
        if m in (0xC0, 0xC1, 0xC2):
            h, w = struct.unpack(">HH", data[i + 5:i + 9])
            return w, h
        i += 2 + struct.unpack(">H", data[i + 2:i + 4])[0]
    return None


class Builder(HTMLParser):
    def __init__(self, img_dirs):
        super().__init__(convert_charrefs=True)
        self.body, self.rels, self.media, self.nums = [], [], [], []
        self.img_dirs = img_dirs
        self.para = None          # list of runs for the open paragraph
        self.pstyle = None
        self.bold = self.ital = 0
        self.link = None          # rel id of the open <a>
        self.lists = []           # stack of num ids
        self.table = None         # list of rows; row = list of cells; cell = list of paragraphs xml
        self.cell = None
        self.cell_head = False
        self.quote = 0

    # ---------- paragraphs
    def open_p(self, style=None):
        self.close_p()
        self.para, self.pstyle = [], style

    def close_p(self):
        if self.para is None:
            return
        ppr = ""
        if self.pstyle == "list":
            lvl = len(self.lists) - 1
            ppr = f'<w:pPr><w:pStyle w:val="ListParagraph"/><w:numPr><w:ilvl w:val="{max(lvl, 0)}"/><w:numId w:val="{self.lists[-1][0]}"/></w:numPr></w:pPr>'
        elif self.pstyle:
            ppr = f'<w:pPr><w:pStyle w:val="{self.pstyle}"/></w:pPr>'
        elif self.quote:
            ppr = '<w:pPr><w:ind w:left="567"/></w:pPr>'
        xml = f"<w:p>{ppr}{''.join(self.para)}</w:p>"
        if self.cell is not None:
            self.cell.append(xml)
        else:
            self.body.append(xml)
        self.para, self.pstyle = None, None

    def run(self, text):
        if self.para is None:
            if not text.strip():
                return
            self.open_p()
        rpr = ""
        if self.bold or self.cell_head:
            rpr += "<w:b/>"
        if self.ital:
            rpr += "<w:i/>"
        if self.link:
            rpr += '<w:rStyle w:val="Hyperlink"/>'
        r = f'<w:r>{"<w:rPr>" + rpr + "</w:rPr>" if rpr else ""}<w:t xml:space="preserve">{esc(text)}</w:t></w:r>'
        if self.link:
            r = f'<w:hyperlink r:id="{self.link}" w:history="1">{r}</w:hyperlink>'
        self.para.append(r)

    # ---------- relationships
    def rel(self, typ, target, external=False):
        rid = f"rId{len(self.rels) + 10}"
        self.rels.append((rid, typ, target, external))
        return rid

    def image(self, src):
        name = os.path.basename(src.split("?")[0])
        data = None
        for d in self.img_dirs:
            p = os.path.join(d, name)
            if os.path.isfile(p):
                data = open(p, "rb").read()
                break
        if data is None:
            self.open_p()
            self.run(f"[Image: {name} — insert here]")
            self.close_p()
            return
        size = jpeg_size(data) or (700, 394)
        cx = min(MAX_EMU, size[0] * 9525)
        cy = int(cx * size[1] / size[0])
        ext = os.path.splitext(name)[1].lower() or ".jpg"
        idx = len(self.media) + 1
        target = f"media/image{idx}{ext}"
        self.media.append((target, data))
        rid = self.rel("http://schemas.openxmlformats.org/officeDocument/2006/relationships/image", target)
        drawing = (f'<w:r><w:drawing><wp:inline><wp:extent cx="{cx}" cy="{cy}"/><wp:docPr id="{idx}" name="{esc(name)}"/>'
                   f'<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:pic>'
                   f'<pic:nvPicPr><pic:cNvPr id="{idx}" name="{esc(name)}"/><pic:cNvPicPr/></pic:nvPicPr>'
                   f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
                   f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
                   f'</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r>')
        self.close_p()
        xml = f"<w:p>{drawing}</w:p>"
        (self.cell if self.cell is not None else self.body).append(xml)

    # ---------- parser
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("h1", "h2", "h3", "h4"):
            self.open_p({"h1": "Heading1", "h2": "Heading2", "h3": "Heading3", "h4": "Heading4"}[tag])
        elif tag == "p":
            if self.para is None or self.para:
                self.open_p()
        elif tag in ("strong", "b"):
            self.bold += 1
        elif tag in ("em", "i"):
            self.ital += 1
        elif tag == "a" and a.get("href"):
            href = a["href"]
            if href.startswith("#"):
                self.link = None
            else:
                self.link = self.rel("http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink", href, True)
        elif tag in ("ul", "ol"):
            self.close_p()
            num_id = len(self.nums) + 1
            self.nums.append(tag)
            self.lists.append((num_id, tag))
        elif tag == "li":
            self.open_p("list")
        elif tag == "br":
            if self.para is not None:
                self.para.append("<w:r><w:br/></w:r>")
        elif tag == "img":
            self.image(a.get("src", ""))
        elif tag == "table":
            self.close_p()
            self.table = []
        elif tag == "tr" and self.table is not None:
            self.table.append([])
        elif tag in ("td", "th") and self.table is not None:
            self.cell, self.cell_head = [], tag == "th"
            self.open_p()
        elif tag == "blockquote":
            self.close_p()
            self.quote += 1
        elif tag == "hr":
            self.close_p()
            self.body.append('<w:p><w:pPr><w:pBdr><w:bottom w:val="single" w:sz="6" w:space="1" w:color="999999"/></w:pBdr></w:pPr></w:p>')

    def handle_endtag(self, tag):
        if tag in ("h1", "h2", "h3", "h4", "p", "li"):
            self.close_p()
        elif tag in ("strong", "b"):
            self.bold = max(0, self.bold - 1)
        elif tag in ("em", "i"):
            self.ital = max(0, self.ital - 1)
        elif tag == "a":
            self.link = None
        elif tag in ("ul", "ol"):
            self.close_p()
            if self.lists:
                self.lists.pop()
        elif tag in ("td", "th") and self.cell is not None:
            self.close_p()
            if self.table:
                self.table[-1].append((self.cell or ["<w:p/>"], self.cell_head))
            self.cell, self.cell_head = None, False
        elif tag == "table" and self.table is not None:
            self.body.append(self.table_xml(self.table))
            self.table = None
        elif tag == "blockquote":
            self.close_p()
            self.quote = max(0, self.quote - 1)

    def handle_data(self, data):
        if self.table is not None and self.cell is None:
            return
        text = re.sub(r"\s+", " ", data)
        if text:
            self.run(text)

    @staticmethod
    def table_xml(rows):
        cols = max((len(r) for r in rows), default=1)
        width = 9000 // cols
        out = ['<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/><w:tblW w:w="5000" w:type="pct"/></w:tblPr><w:tblGrid>'
               + "".join(f'<w:gridCol w:w="{width}"/>' for _ in range(cols)) + "</w:tblGrid>"]
        for r in rows:
            out.append("<w:tr>")
            for cell, head in r + [(["<w:p/>"], False)] * (cols - len(r)):
                shade = '<w:shd w:val="clear" w:color="auto" w:fill="E8EDF4"/>' if head else ""
                out.append(f'<w:tc><w:tcPr><w:tcW w:w="{width}" w:type="dxa"/>{shade}</w:tcPr>{"".join(cell)}</w:tc>')
            out.append("</w:tr>")
        out.append("</w:tbl><w:p/>")
        return "".join(out)


STYLES = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles {W}><w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/><w:sz w:val="22"/></w:rPr></w:rPrDefault>
<w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="276" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/><w:spacing w:before="240" w:after="120"/><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:b/><w:sz w:val="40"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/><w:spacing w:before="240" w:after="80"/><w:outlineLvl w:val="1"/></w:pPr><w:rPr><w:b/><w:sz w:val="32"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/><w:spacing w:before="160" w:after="60"/><w:outlineLvl w:val="2"/></w:pPr><w:rPr><w:b/><w:sz w:val="26"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading4"><w:name w:val="heading 4"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:outlineLvl w:val="3"/></w:pPr><w:rPr><w:b/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="ListParagraph"><w:name w:val="List Paragraph"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:after="40"/></w:pPr></w:style>
<w:style w:type="character" w:styleId="Hyperlink"><w:name w:val="Hyperlink"/><w:rPr><w:color w:val="1F57E6"/><w:u w:val="single"/></w:rPr></w:style>
<w:style w:type="table" w:styleId="TableGrid"><w:name w:val="Table Grid"/><w:tblPr><w:tblBorders><w:top w:val="single" w:sz="4" w:color="BFC7D2"/><w:left w:val="single" w:sz="4" w:color="BFC7D2"/><w:bottom w:val="single" w:sz="4" w:color="BFC7D2"/><w:right w:val="single" w:sz="4" w:color="BFC7D2"/><w:insideH w:val="single" w:sz="4" w:color="BFC7D2"/><w:insideV w:val="single" w:sz="4" w:color="BFC7D2"/></w:tblBorders><w:tblCellMar><w:left w:w="100" w:type="dxa"/><w:right w:w="100" w:type="dxa"/></w:tblCellMar></w:tblPr></w:style>
</w:styles>'''


def numbering(nums):
    absn = []
    for i, kind in enumerate(nums, 1):
        lvls = []
        for lv in range(3):
            if kind == "ol":
                lvls.append(f'<w:lvl w:ilvl="{lv}"><w:start w:val="1"/><w:numFmt w:val="decimal"/><w:lvlText w:val="%{lv + 1}."/><w:lvlJc w:val="left"/><w:pPr><w:ind w:left="{720 * (lv + 1)}" w:hanging="360"/></w:pPr></w:lvl>')
            else:
                lvls.append(f'<w:lvl w:ilvl="{lv}"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="•"/><w:lvlJc w:val="left"/><w:pPr><w:ind w:left="{720 * (lv + 1)}" w:hanging="360"/></w:pPr></w:lvl>')
        absn.append(f'<w:abstractNum w:abstractNumId="{i}"><w:multiLevelType w:val="hybridMultilevel"/>{"".join(lvls)}</w:abstractNum>')
    nums_xml = "".join(f'<w:num w:numId="{i}"><w:abstractNumId w:val="{i}"/></w:num>' for i in range(1, len(nums) + 1))
    return f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:numbering {W}>{"".join(absn)}{nums_xml}</w:numbering>'


def build(html_text, out, img_dirs):
    b = Builder(img_dirs)
    b.feed(html_text)
    b.close()
    b.close_p()
    doc = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document {W}><w:body>{"".join(b.body)}'
           '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134" w:header="708" w:footer="708" w:gutter="0"/></w:sectPr></w:body></w:document>')
    rels = ['<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>',
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>']
    for rid, typ, target, ext in b.rels:
        rels.append(f'<Relationship Id="{rid}" Type="{typ}" Target="{html.escape(target)}"' + (' TargetMode="External"' if ext else "") + "/>")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                   '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>'
                   '<Default Extension="jpg" ContentType="image/jpeg"/><Default Extension="jpeg" ContentType="image/jpeg"/><Default Extension="png" ContentType="image/png"/>'
                   '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
                   '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
                   '<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/></Types>')
        z.writestr("_rels/.rels", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                   '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>')
        z.writestr("word/document.xml", doc)
        z.writestr("word/styles.xml", STYLES)
        z.writestr("word/numbering.xml", numbering(b.nums or ["ul"]))
        z.writestr("word/_rels/document.xml.rels", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' + "".join(rels) + "</Relationships>")
        for target, data in b.media:
            z.writestr("word/" + target, data)
    return out


def main(argv):
    if "--self-test" in argv:
        import tempfile
        sample = ('<h1>D-Bal Max vs <a href="https://example.com/aff/crazybulk">CrazyBulk D-Bal</a></h1><p>Intro with <b>bold</b> and '
                  '<a href="https://example.com/aff/dbal">D-Bal Max</a>.</p><h2>Quick facts</h2><ul><li>Price: $64.99</li><li>Guarantee: 60 days</li></ul>'
                  '<ol><li>One</li><li>Two</li></ol><table><tr><th>Product</th><th>Price</th></tr><tr><td><a href="https://example.com/aff/dbal">D-Bal Max</a></td>'
                  '<td>$64.99</td></tr></table><img src="01-quick-facts.jpg">')
        d = tempfile.mkdtemp()
        out = build(sample, os.path.join(d, "t.docx"), [d])
        with zipfile.ZipFile(out) as z:
            doc = z.read("word/document.xml").decode()
            rels = z.read("word/_rels/document.xml.rels").decode()
        assert 'w:val="Heading1"' in doc and "<w:tbl>" in doc and "w:numId" in doc and "w:hyperlink" in doc
        assert rels.count('TargetMode="External"') == 3 and "[Image: 01-quick-facts.jpg" in doc
        import xml.dom.minidom
        xml.dom.minidom.parseString(doc)          # well-formed
        print("self-test ok")
        return 0
    if len(argv) < 2:
        print(__doc__)
        return 2
    src, out = argv[0], argv[1]
    dirs = [argv[argv.index("--images") + 1]] if "--images" in argv else []
    dirs.append(os.path.dirname(os.path.abspath(src)))
    with open(src, encoding="utf-8") as f:
        build(f.read(), out, dirs)
    print(os.path.abspath(out))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

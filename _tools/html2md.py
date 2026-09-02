#!/usr/bin/env python3
"""Convert exported HTML posts (VSCode / Notion / pdf-embed shells) back to Markdown.

Display math rule: every $$ delimiter sits on its own line, with a newline
before and after the block.
"""
import html
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ANNOT_RE = re.compile(
    r'<annotation encoding="application/x-tex">(.*?)</annotation>', re.S
)


def find_span_end(s, start):
    """Given index of a '<span' opening tag, return index just past its matching </span>."""
    depth = 0
    tag_re = re.compile(r'<(/?)span\b[^>]*>')
    for m in tag_re.finditer(s, start):
        if m.group(1):
            depth -= 1
            if depth == 0:
                return m.end()
        else:
            depth += 1
    raise ValueError("unbalanced spans")


def extract_math(body):
    """Replace math spans with placeholders; return (new_body, {placeholder: (kind, latex)})."""
    math_map = {}
    counter = [0]

    def take(kind, latex):
        key = f"\x00MATH{counter[0]}\x00"
        counter[0] += 1
        math_map[key] = (kind, latex.strip())
        return key

    def scan(text, open_re, kind_of, latex_of):
        out, i = [], 0
        while True:
            m = open_re.search(text, i)
            if not m:
                out.append(text[i:])
                break
            out.append(text[i:m.start()])
            end = find_span_end(text, m.start())
            chunk = text[m.start():end]
            out.append(take(kind_of(m), latex_of(m, chunk)))
            i = end
        return "".join(out)

    # 1. Notion inline equation tokens: latex lives in the data attribute
    notion_re = re.compile(r'<span data-notion-inline-equation="((?:[^"\\]|\\.)*)"[^>]*>')
    body = scan(
        body, notion_re,
        lambda m: "inline",
        lambda m, chunk: html.unescape(m.group(1)),
    )
    # 2. KaTeX display / inline spans: latex lives in the MathML annotation
    katex_re = re.compile(r'<span class="(katex-display|katex)"[^>]*>')

    def katex_latex(m, chunk):
        am = ANNOT_RE.search(chunk)
        return html.unescape(am.group(1)) if am else ""

    body = scan(
        body, katex_re,
        lambda m: "display" if m.group(1) == "katex-display" else "inline",
        katex_latex,
    )
    return body, math_map


PLACEHOLDER_RE = re.compile(r"[ \t]*\x00MATH\d+\x00[ \t]*")
KEY_RE = re.compile(r"\x00MATH\d+\x00")
RAW_DISPLAY_RE = re.compile(r"[ \t]*\$\$\s*(.+?)\s*\$\$[ \t]*", re.S)
# raw KaTeX-auto-render delimiters (md2html.py emits these): back to $ form
RAW_BRACKET_RE = re.compile(r"[ \t]*\\\[\s*(.+?)\s*\\\][ \t]*", re.S)
RAW_PAREN_RE = re.compile(r"\\\((.+?)\\\)", re.S)


class MDConverter(HTMLParser):
    SKIP_TAGS = ("svg", "script", "style", "button", "nav")

    def __init__(self, math_map):
        super().__init__(convert_charrefs=True)
        self.math_map = math_map
        self.blocks = []
        self.buf = []
        self.list_stack = []
        self.ol_counters = []
        self.href = None
        self.skip_depth = 0
        # code blocks
        self.in_pre = False
        self.pre_buf = []
        self.code_lang = ""
        # blockquotes: stack of block-list lengths at open time
        self.quote_starts = []
        # tables
        self.in_table = False
        self.rows = []
        self.cur_row = None
        self.n_header_rows = 0
        self.in_thead = False

    # ---- inline/block text assembly -------------------------------------

    def render_inline(self, text, in_cell=False):
        """Substitute math placeholders into flowing text."""
        def sub(m):
            key = KEY_RE.search(m.group(0)).group(0)
            kind, latex = self.math_map[key]
            if in_cell:
                latex = latex.replace("\n", " ").replace("|", r"\vert ")
                return " $" + latex + "$ "
            if kind == "display":
                return "\n$$\n" + latex + "\n$$\n"
            return " $" + latex.replace("\n", " ") + "$ "

        text = PLACEHOLDER_RE.sub(sub, text)
        if in_cell:
            return RAW_PAREN_RE.sub(
                lambda m: " $" + m.group(1).strip().replace("\n", " ") + "$ ", text)
        # raw $$...$$ / \[...\] / \(...\) that survived in the source text
        text = RAW_DISPLAY_RE.sub(lambda m: "\n$$\n" + m.group(1) + "\n$$\n", text)
        text = RAW_BRACKET_RE.sub(lambda m: "\n$$\n" + m.group(1) + "\n$$\n", text)
        text = RAW_PAREN_RE.sub(lambda m: " $" + m.group(1).strip() + "$ ", text)
        return text

    def finish_text(self, in_cell=False):
        text = "".join(self.buf)
        self.buf = []
        text = self.render_inline(text, in_cell=in_cell)
        # tidy spaces the inline joins introduced
        text = re.sub(r"[ \t]{2,}", " ", text)
        text = re.sub(r"[ \t]+([,.;:!?)\]])", r"\1", text)
        text = re.sub(r"\(\s+", "(", text)
        text = re.sub(r"(?m)[ \t]+$", "", text)
        text = re.sub(r"(?m)^[ \t]+(?!\-|\d+\. )", "", text)
        return text.strip()

    def flush(self, prefix=""):
        text = self.finish_text()
        if text:
            self.blocks.append(prefix + text)

    def emit_li(self):
        indent = "  " * (len(self.list_stack) - 1)
        if self.list_stack and self.list_stack[-1] == "ol":
            self.ol_counters[-1] += 1
            marker = f"{self.ol_counters[-1]}. "
        else:
            marker = "- "
        text = self.finish_text()
        if text:
            pad = " " * len(indent + marker)
            lines = text.split("\n")
            body = lines[0] + "".join(
                "\n" + (pad + ln if ln else "") for ln in lines[1:]
            )
            self.blocks.append(indent + marker + body)

    # ---- tag handlers ----------------------------------------------------

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP_TAGS:
            self.skip_depth += 1
            return
        if self.skip_depth:
            return
        attrs = dict(attrs)
        if self.in_pre:
            if tag == "code" and not self.pre_buf:
                m = re.search(r"language-([\w+-]+)", attrs.get("class", "") or "")
                if m:
                    self.code_lang = m.group(1)
            return  # hljs spans etc: keep only their text
        if tag == "pre":
            self.flush()
            self.in_pre = True
            self.pre_buf = []
            self.code_lang = ""
        elif tag == "code":
            self.buf.append("`")
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.flush()
        elif tag == "p":
            if not self.list_stack:
                self.flush()
        elif tag in ("ul", "ol"):
            if self.list_stack:
                self.emit_li()  # parent <li> text, before descending
            else:
                self.flush()
            self.list_stack.append(tag)
            if tag == "ol":
                self.ol_counters.append(0)
        elif tag == "li":
            self.buf = []
        elif tag == "strong" or tag == "b":
            self.buf.append("**")
        elif tag == "em" or tag == "i":
            self.buf.append("*")
        elif tag in ("del", "s"):
            self.buf.append("~~")
        elif tag == "a":
            self.href = attrs.get("href", "")
            self.buf.append("[")
        elif tag == "img":
            src = attrs.get("src", "")
            alt = attrs.get("alt", "") or ""
            alt = re.sub(r"</?(em|i)>", "*", alt)
            alt = re.sub(r"</?(strong|b)>", "**", alt)
            alt = re.sub(r"<[^>]+>", "", alt)
            alt = re.sub(r"[\[\]]", "", alt)
            self.buf.append(f"![{alt}]({src})")
        elif tag == "hr":
            self.flush()
            self.blocks.append("---")
        elif tag == "br":
            self.buf.append("\n")
        elif tag == "blockquote":
            self.flush()
            self.quote_starts.append(len(self.blocks))
        elif tag == "details":
            self.flush()
            self.blocks.append("<details>")
        elif tag == "summary":
            self.flush()
        elif tag == "figcaption":
            self.flush()
        elif tag == "table":
            self.flush()
            self.in_table = True
            self.rows = []
            self.n_header_rows = 0
        elif tag == "thead":
            self.in_thead = True
        elif tag == "tr":
            self.cur_row = []
        elif tag in ("td", "th"):
            self.buf = []

    def handle_endtag(self, tag):
        if tag in self.SKIP_TAGS:
            if self.skip_depth:
                self.skip_depth -= 1
            return
        if self.skip_depth:
            return
        if self.in_pre:
            if tag == "pre":
                self.in_pre = False
                code = "".join(self.pre_buf).strip("\n")
                self.blocks.append(f"```{self.code_lang}\n{code}\n```")
            return
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.flush("#" * int(tag[1]) + " ")
        elif tag == "p":
            if not self.list_stack:
                self.flush()
        elif tag in ("ul", "ol"):
            if self.list_stack:
                popped = self.list_stack.pop()
                if popped == "ol":
                    self.ol_counters.pop()
        elif tag == "li":
            self.emit_li()
        elif tag == "strong" or tag == "b":
            self.buf.append("**")
        elif tag == "em" or tag == "i":
            self.buf.append("*")
        elif tag in ("del", "s"):
            self.buf.append("~~")
        elif tag == "code":
            self.buf.append("`")
        elif tag == "a":
            self.buf.append(f"]({self.href})")
            self.href = None
        elif tag == "blockquote":
            start = self.quote_starts.pop()
            inner, self.blocks = self.blocks[start:], self.blocks[:start]
            quoted = "\n>\n".join(
                "\n".join("> " + ln if ln else ">" for ln in blk.split("\n"))
                for blk in inner
            )
            if quoted:
                self.blocks.append(quoted)
        elif tag == "details":
            self.flush()
            self.blocks.append("</details>")
        elif tag == "summary":
            text = self.finish_text()
            self.blocks.append(f"<summary>{text}</summary>")
        elif tag == "figcaption":
            text = self.finish_text()
            if text:
                self.blocks.append(f"*{text}*")
        elif tag == "thead":
            self.in_thead = False
        elif tag in ("td", "th"):
            if self.cur_row is not None:
                text = self.finish_text(in_cell=True)
                text = re.sub(r"\s+", " ", text).strip()
                self.cur_row.append(text.replace("|", r"\|") if tag != "x" else text)
        elif tag == "tr":
            if self.cur_row is not None:
                self.rows.append(self.cur_row)
                if self.in_thead:
                    self.n_header_rows += 1
                self.cur_row = None
        elif tag == "table":
            self.in_table = False
            if self.rows:
                width = max(len(r) for r in self.rows)
                rows = [r + [""] * (width - len(r)) for r in self.rows]
                lines = ["| " + " | ".join(rows[0]) + " |",
                         "|" + "---|" * width]
                for r in rows[1:]:
                    lines.append("| " + " | ".join(r) + " |")
                self.blocks.append("\n".join(lines))

    def handle_data(self, data):
        if self.skip_depth:
            return
        if self.in_pre:
            if not self.code_lang:
                pass
            self.pre_buf.append(data)
            return
        self.buf.append(re.sub(r"\s+", " ", data))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in ("img", "hr", "br"):
            self.handle_endtag(tag)

    def result(self):
        self.flush()
        return "\n\n".join(b for b in self.blocks if b.strip())


def convert(path: Path, out_dir: Path):
    src = path.read_text(encoding="utf-8")
    tm = re.search(r"<h1>(.*?)</h1>", src, re.S)
    title = html.unescape(re.sub(r"<[^>]+>", "", tm.group(1))).strip() if tm else path.stem
    em = re.search(r'<p class="eyebrow">(.*?)</p>', src, re.S)
    eyebrow = html.unescape(em.group(1)).strip() if em else ""
    date = eyebrow.split("·")[0].strip() if eyebrow else ""
    am = re.search(r"<article[^>]*>(.*?)</article>", src, re.S)
    body = am.group(1) if am else src

    out = out_dir / (path.stem + ".md")

    # pdf-embed shells have no convertible prose: link to the pdf instead
    if 'data-src="pdf"' in src:
        pm = re.search(r'<a href="([^"]+\.pdf)"', body)
        pdf = pm.group(1) if pm else ""
        md = f"# {title}\n\n*{date}*\n\nThis post is a PDF document: [{pdf.split('/')[-1]}]({pdf})\n"
        out.write_text(md, encoding="utf-8")
        print(f"{path.name} -> {out.name} (pdf link only)")
        return

    body = re.sub(r'<span id="markdown-mermaid".*?</span>', "", body, flags=re.S)
    body, math_map = extract_math(body)

    conv = MDConverter(math_map)
    conv.feed(body)
    md = conv.result()

    # final tidy: collapse 3+ newlines, trailing spaces
    md = md.replace("﻿", "").replace("​", "")
    # raw math whose _ was eaten as <em> by the exporter: "p*{max}" -> "p_{max}"
    md = re.sub(r"\$[^$\n]+\$", lambda m: m.group(0).replace("*{", "_{"), md)
    md = re.sub(r"(?<!\*)\*\*\*\*(?!\*)", "", md)
    md = re.sub(r"(?m)[ \t]+$", "", md)
    md = re.sub(r"\n{3,}", "\n\n", md)

    header = f"# {title}\n\n"
    if date:
        header += f"*{date}*\n\n"
    out.write_text(header + md + "\n", encoding="utf-8")
    n_disp = sum(1 for k, (kind, _) in math_map.items() if kind == "display")
    print(f"{path.name} -> {out.name} ({len(md)} chars, {len(math_map)} math, {n_disp} display)")


if __name__ == "__main__":
    out_dir = Path(sys.argv[1])
    out_dir.mkdir(exist_ok=True)
    for p in sys.argv[2:]:
        try:
            convert(Path(p), out_dir)
        except Exception as e:
            print(f"FAILED {p}: {e}")

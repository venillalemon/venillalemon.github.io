#!/usr/bin/env python3
"""Build a styled post in files/ from a Markdown source in md/.

Inverse of html2md.py: understands exactly the Markdown dialect that tool
emits (and that the notes in md/ are written in) — `# Title` + `*date*`
header, *em* / **strong** / ~~del~~, inline `code`, fenced code blocks,
nested `-` / `1.` lists, `> ` blockquotes, pipe tables, images, links,
`---` rules, raw HTML blocks (<details> etc.), and math left as
$...$ / $$...$$ for KaTeX to render in the browser.

The document shell (head, masthead, footer, theme toggle, analytics) comes
from restyle_posts.build(), so a change to the chrome there flows into
posts built from Markdown too.

Usage:  python3 _tools/md2html.py md/foo.md [more.md ...]
        writes files/<same-stem>.html for each input.
Options: --out PATH (single input only), --title T, --date "Month D, YYYY"
"""

import argparse
import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from restyle_posts import ROOT, build, date_from_basename  # noqa: E402

# ---- placeholder protection ------------------------------------------------
# Code and math are lifted out before any parsing, restored at the end.

FENCE_RE = re.compile(r"(?m)^```([\w+-]*)[ \t]*\n(.*?)\n```[ \t]*$", re.S)
INLINE_CODE_RE = re.compile(r"`([^`\n]+)`")
DISPLAY_RE = re.compile(r"\$\$(.+?)\$\$", re.S)
BRACKET_DISPLAY_RE = re.compile(r"\\\[(.+?)\\\]", re.S)
# content must not start/end with whitespace, so a literal $ in prose
# (e.g. a stack symbol) cannot pair up with a real math delimiter
INLINE_MATH_RE = re.compile(r"\$(?![\s$])([^$\n]*?)(?<!\s)\$")
PAREN_MATH_RE = re.compile(r"\\\((.+?)\\\)")

KEY_RE = re.compile(r"\x00(\d+)\x00")


def unquote(latex):
    """Display math written inside a blockquote (`> $$ ... > $$`) captures the
    `> ` prefixes into the latex; strip them when every line carries one."""
    lines = latex.split("\n")
    if len(lines) > 1 and all(ln.startswith(">") or not ln.strip() for ln in lines[1:]):
        lines = [lines[0]] + [re.sub(r"^> ?", "", ln) for ln in lines[1:]]
    return "\n".join(lines)


class Stash:
    """Numbered placeholders for spans that must not be parsed as Markdown."""

    def __init__(self):
        self.items = []

    def put(self, kind, *payload):
        self.items.append((kind, payload))
        return f"\x00{len(self.items) - 1}\x00"

    def protect(self, text):
        text = FENCE_RE.sub(lambda m: self.put("fence", m.group(1), m.group(2)), text)
        text = INLINE_CODE_RE.sub(lambda m: self.put("code", m.group(1)), text)
        for pat, kind in ((DISPLAY_RE, "display"), (BRACKET_DISPLAY_RE, "display"),
                          (INLINE_MATH_RE, "inline"), (PAREN_MATH_RE, "inline")):
            text = pat.sub(lambda m, k=kind: self.put(k, unquote(m.group(1))), text)
        return text

    def restore(self, htext):
        def sub(m):
            kind, payload = self.items[int(m.group(1))]
            if kind == "fence":
                lang, code = payload
                cls = f' class="language-{lang}"' if lang else ""
                return f"<pre><code{cls}>{html.escape(code)}\n</code></pre>"
            if kind == "code":
                return f"<code>{html.escape(payload[0])}</code>"
            # \(..\) / \[..\] delimiters, so a stray literal $ in the prose
            # can never pair with a math delimiter when KaTeX auto-renders
            latex = html.escape(payload[0].strip(), quote=False)
            if kind == "display":
                return f"\\[\n{latex}\n\\]"
            return f"\\({latex}\\)"

        return KEY_RE.sub(sub, htext)


# ---- inline markdown -> html ----------------------------------------------

IMG_RE = re.compile(r"!\[([^\]]*)\]\(([^()\s]+)\)")
# Link labels may contain one balanced bracket pair, as in ``[[GPV08]](url)``.
LINK_RE = re.compile(r"\[((?:[^\[\]]|\[[^\[\]]*\])+)\]\(([^()\s]+)\)")
STRONG_RE = re.compile(r"\*\*(.+?)\*\*", re.S)
EM_RE = re.compile(r"(?<!\*)\*([^*\n]+)\*(?!\*)")
DEL_RE = re.compile(r"~~(.+?)~~", re.S)


def inline(text):
    text = html.escape(text, quote=False)
    text = IMG_RE.sub(r'<img src="\2" alt="\1">', text)
    text = LINK_RE.sub(r'<a href="\2">\1</a>', text)
    text = STRONG_RE.sub(r"<strong>\1</strong>", text)
    text = EM_RE.sub(r"<em>\1</em>", text)
    text = DEL_RE.sub(r"<del>\1</del>", text)
    return text.strip()


# ---- block structure -------------------------------------------------------

LIST_ITEM_RE = re.compile(r"^(\s*)(-|\d+\.)\s+(.*)$", re.S)
TABLE_SEP_RE = re.compile(r"^\|(?:\s*:?-+:?\s*\|)+\s*$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")


def split_row(line):
    """Cells of a pipe-table row, honouring the \\| escape."""
    cells = re.split(r"(?<!\\)\|", line.strip())
    return [c.replace(r"\|", "|").strip() for c in cells[1:-1]]


def parse_list(lines, i, indent):
    items, tag = [], None
    while i < len(lines):
        m = LIST_ITEM_RE.match(lines[i])
        if not m or len(m.group(1)) < indent:
            break
        depth = len(m.group(1))
        if depth > indent:                       # nested list inside last item
            sub, i = parse_list(lines, i, depth)
            items[-1] += sub
            continue
        tag = tag or ("ol" if m.group(2) != "-" else "ul")
        pad = depth + len(m.group(2)) + 1
        body = [m.group(3)]
        i += 1
        while i < len(lines) and LIST_ITEM_RE.match(lines[i]) is None:
            ln = lines[i]
            if ln.strip() == "" or len(ln) - len(ln.lstrip()) >= pad:
                if ln.strip():
                    body.append(ln.strip())
                i += 1
            else:
                break
        items.append("<li>" + inline("\n".join(body)) + "</li>")
        if i < len(lines):
            nxt = LIST_ITEM_RE.match(lines[i])
            if nxt and len(nxt.group(1)) < indent:
                break
    return f"<{tag}>\n" + "\n".join(items) + f"\n</{tag}>", i


def parse_blocks(text):
    lines = text.split("\n")
    out, i = [], 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        m = HEADING_RE.match(line)
        if m:
            out.append(f"<h{len(m.group(1))}>{inline(m.group(2))}</h{len(m.group(1))}>")
            i += 1
        elif line.strip() == "---":
            out.append("<hr>")
            i += 1
        elif LIST_ITEM_RE.match(line) and not line.startswith((" ", "\t")):
            block, i = parse_list(lines, i, 0)
            out.append(block)
        elif line.lstrip().startswith(">"):
            quoted = []
            while i < len(lines) and lines[i].lstrip().startswith(">"):
                quoted.append(re.sub(r"^\s*> ?", "", lines[i]))
                i += 1
            out.append("<blockquote>\n" + parse_blocks("\n".join(quoted)) + "\n</blockquote>")
        elif line.startswith("|") and i + 1 < len(lines) and TABLE_SEP_RE.match(lines[i + 1]):
            header = split_row(line)
            i += 2
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append(split_row(lines[i]))
                i += 1
            thead = "<tr>" + "".join(f"<th>{inline(c)}</th>" for c in header) + "</tr>"
            tbody = "\n".join(
                "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in rows
            )
            out.append(f"<table>\n<thead>{thead}</thead>\n<tbody>\n{tbody}\n</tbody>\n</table>")
        elif line.startswith("<"):               # raw HTML block, verbatim
            raw = []
            while i < len(lines) and lines[i].strip():
                raw.append(lines[i])
                i += 1
            out.append("\n".join(raw))
        else:                                    # paragraph
            para = [lines[i]]
            i += 1
            while i < len(lines) and lines[i].strip() and not (
                HEADING_RE.match(lines[i]) or lines[i].strip() == "---"
                or LIST_ITEM_RE.match(lines[i]) or lines[i].lstrip().startswith(">")
                or lines[i].startswith("<")
            ):
                para.append(lines[i])
                i += 1
            out.append(f"<p>{inline(' '.join(para))}</p>")
    return "\n".join(out)


# ---- document header -------------------------------------------------------

FRONT_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)
DATE_LINE_RE = re.compile(r"^\*([A-Z][a-z]+ \d{1,2}, \d{4})\*$")
MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]


def take_header(text):
    """Strip frontmatter / leading `# title` / `*date*` line; return (title, date, body)."""
    title = date = ""
    fm = FRONT_RE.match(text)
    if fm:
        text = text[fm.end():]
        for key, val in re.findall(r"(?m)^(title|date)\s*:\s*(.+)$", fm.group(1)):
            val = val.strip().strip("\"'")
            if key == "title":
                title = val
            else:
                m = re.match(r"(\d{4})-(\d{2})-(\d{2})", val)
                date = f"{MONTHS[int(m.group(2)) - 1]} {int(m.group(3))}, {m.group(1)}" if m else val
    lines = text.lstrip("\n").split("\n")
    if lines and lines[0].startswith("# "):
        title = title or lines[0][2:].strip()
        lines = lines[1:]
    while lines and not lines[0].strip():
        lines = lines[1:]
    if lines:
        dm = DATE_LINE_RE.match(lines[0].strip())
        if dm:
            date = date or dm.group(1)
            lines = lines[1:]
    return title, date, "\n".join(lines)


def convert(path, out_path=None, title=None, date=None):
    src = open(path, encoding="utf-8").read()
    basename = os.path.splitext(os.path.basename(path))[0]
    doc_title, doc_date, body_md = take_header(src)
    title = title or doc_title or " ".join(basename.split("_")[3:]) or basename
    iso_date, human_date = date_from_basename(basename)
    human_date = date or doc_date or human_date

    stash = Stash()
    body = stash.restore(parse_blocks(stash.protect(body_md)))
    # a fence that formed a paragraph of its own: <pre> may not sit inside <p>
    body = re.sub(r"<p>(<pre>.*?</pre>)</p>", r"\1", body, flags=re.S)
    page = build(basename, title, iso_date, human_date, "markdown", "\n" + body + "\n")

    out_path = out_path or os.path.join(ROOT, "files", basename + ".html")
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(page)
    print(f"built {os.path.relpath(out_path, ROOT)}  ({len(body)} chars)", flush=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("sources", nargs="+")
    ap.add_argument("--out", help="output path (single source only)")
    ap.add_argument("--title")
    ap.add_argument("--date", help='override date, e.g. "May 11, 2026"')
    args = ap.parse_args()
    if args.out and len(args.sources) > 1:
        ap.error("--out only makes sense with a single source")
    for src in args.sources:
        convert(src, out_path=args.out, title=args.title, date=args.date)


if __name__ == "__main__":
    main()

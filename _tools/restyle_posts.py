#!/usr/bin/env python3
"""Re-shell the exported blog posts in files/ with the site's editorial style.

Each post in files/ is a standalone HTML export (VS Code markdown preview, or
Notion).  This script keeps the exported *body* verbatim and swaps the
surrounding document — head, stylesheets, masthead, footer — for the shared
look defined in assets/css/post.css.

Idempotent: a file that already carries the new shell is rewritten from its
existing article body, so it can be re-run after the CSS or chrome changes.

Usage:  python3 _tools/restyle_posts.py [files/foo.html ...]
"""

import glob
import html
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KATEX_CSS = "https://cdn.jsdelivr.net/npm/katex@0.16/dist/katex.min.css"
KATEX_JS = "https://cdn.jsdelivr.net/npm/katex@0.16/dist/katex.min.js"
KATEX_AUTORENDER = "https://cdn.jsdelivr.net/npm/katex@0.16/dist/contrib/auto-render.min.js"

# posts whose math is still written as $...$ (i.e. built by md_to_post.py)
# get KaTeX's auto-render pass; exports already ship rendered spans.
AUTO_MATH_FLAVOURS = {"markdown"}
# an export can opt in too, by carrying this marker in its body (used where a
# screenshot of a theorem was transcribed back into $...$ by hand)
KATEX_MARK = "<!--katex-->"
KIND = {"notion": "Notion export", "vscode": "Markdown notes",
        "markdown": "Markdown notes", "pdf": "PDF"}

BODY_RE = re.compile(r"<body[^>]*>(.*)</body>", re.S | re.I)
TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
NOTION_ARTICLE_RE = re.compile(r"<article[^>]*class=\"[^\"]*\bpage\b[^\"]*\"[^>]*>(.*)</article>", re.S | re.I)
NOTION_HEADER_RE = re.compile(r"<header\b.*?</header>", re.S | re.I)
PAGE_TITLE_RE = re.compile(r"<h1[^>]*class=\"[^\"]*page-title[^\"]*\"[^>]*>(.*?)</h1>", re.S | re.I)
# An export can open with invisible scaffolding before the real first heading
# (VS Code injects a <span id="markdown-mermaid">), so skip over that first.
LEADING_JUNK_RE = re.compile(
    r"\A(?:\s*(?:<!--.*?-->|<span\b[^>]*>\s*</span>|<script\b.*?</script>"
    r"|<style\b.*?</style>))*\s*",
    re.S | re.I,
)
H1_RE = re.compile(r"<h1\b[^>]*>(.*?)</h1>", re.S | re.I)
# on a re-run, the heading we lifted last time lives here
POST_HEAD_H1_RE = re.compile(r'<div class="post-head">.*?<h1>(.*?)</h1>', re.S)
# our own shell, for idempotent re-runs
NEW_ARTICLE_RE = re.compile(r"<article class=\"prose[^\"]*\" data-src=\"([a-z]+)\">(.*)</article>", re.S)
NEW_MARKER = 'data-shell="venillalemon"'

MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]


def text_of(fragment):
    """Plain text of an HTML fragment, entities resolved."""
    return html.unescape(re.sub(r"<[^>]+>", "", fragment)).strip()


def title_from_basename(basename):
    words = basename.split("_")[3:]
    if not words:
        words = basename.split("_")
    return " ".join(w[:1].upper() + w[1:] for w in words if w)


def date_from_basename(basename):
    m = re.match(r"(\d{4})_(\d{2})_(\d{2})", basename)
    if not m:
        return "", ""
    y, mo, d = m.groups()
    return f"{y}-{mo}-{d}", f"{MONTHS[int(mo) - 1]} {int(d)}, {y}"


def build(basename, title, iso_date, human_date, flavour, body, title_html=None):
    esc_title = html.escape(title, quote=False)
    # the <h1> keeps the heading's own markup (KaTeX spans and all); the
    # <title> tag needs flat text
    head_title = title_html or esc_title
    eyebrow = " · ".join(x for x in (human_date, KIND.get(flavour, "Notes")) if x)
    auto_math = ""
    if flavour in AUTO_MATH_FLAVOURS or KATEX_MARK in body:
        auto_math = f"""
<script defer src="{KATEX_JS}"></script>
<script defer src="{KATEX_AUTORENDER}" onload="renderMathInElement(document.body, {{
  delimiters: [
    {{left: '$$', right: '$$', display: true}},
    {{left: '\\\\[', right: '\\\\]', display: true}},
    {{left: '$', right: '$', display: false}},
    {{left: '\\\\(', right: '\\\\)', display: false}}
  ],
  ignoredClasses: ['katex'],
  throwOnError: false
}})"></script>"""
    return f"""<!doctype html>
<html lang="en" {NEW_MARKER}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<title>{esc_title} &middot; venillalemon</title>
<link rel="icon" href="/images/favicon.ico">
<script>
  (function () {{
    try {{
      var t = localStorage.getItem('theme');
      if (t === 'light' || t === 'dark') document.documentElement.setAttribute('data-theme', t);
    }} catch (e) {{}}
  }})();
</script>
<link rel="stylesheet" href="{KATEX_CSS}">
<link rel="stylesheet" href="/assets/css/post.css">{auto_math}
</head>
<body>

<header class="site-head">
  <div class="col site-head__bar">
    <a class="brand" href="/">venillalemon</a>
    <nav class="site-nav">
      <a href="/">About</a>
      <a href="/blog/">Blog Posts</a>
      <button class="theme-toggle" type="button" data-theme-toggle aria-label="Toggle light / dark theme">&#9689; theme</button>
    </nav>
  </div>
</header>

<main class="site-main">
  <div class="col">
    <div class="post-head">
      <p class="eyebrow">{html.escape(eyebrow, quote=False)}</p>
      <h1>{head_title}</h1>
      <hr class="rule">
    </div>

    <article class="prose {flavour}" data-src="{flavour}">{body}</article>
  </div>
</main>

<footer class="site-foot">
  <div class="col">
    <div class="site-foot__links">
      <a href="/blog/">&larr; All posts</a>
      <a href="https://github.com/venillalemon">GitHub</a>
      <a href="mailto:lifangke@sjtu.edu.cn">Email</a>
    </div>
    <div>Fangke Li{' &middot; ' + human_date if human_date else ''}</div>
  </div>
</footer>

<script>
  (function () {{
    var root = document.documentElement;
    function current() {{
      return root.getAttribute('data-theme') ||
        (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    }}
    document.querySelectorAll('[data-theme-toggle]').forEach(function (btn) {{
      btn.addEventListener('click', function () {{
        var next = current() === 'dark' ? 'light' : 'dark';
        root.setAttribute('data-theme', next);
        try {{ localStorage.setItem('theme', next); }} catch (e) {{}}
      }});
    }});
  }})();
</script>

</body>
</html>
"""


def convert(path):
    src = open(path, encoding="utf-8").read()
    basename = os.path.splitext(os.path.basename(path))[0]
    iso_date, human_date = date_from_basename(basename)

    body_match = BODY_RE.search(src)
    if not body_match:
        raise SystemExit(f"{path}: no <body> found")
    body = body_match.group(1)

    already_new = NEW_MARKER in src
    if already_new:
        art = NEW_ARTICLE_RE.search(body)
        if not art:
            raise SystemExit(f"{path}: restyled file without an article body")
        flavour, body = art.group(1), art.group(2)
        title = text_of(TITLE_RE.search(src).group(1)).replace(" · venillalemon", "")
        kept = POST_HEAD_H1_RE.search(src)
        title_html = kept.group(1).strip() if kept else None
        return build(basename, title, iso_date, human_date, flavour, body,
                     title_html=title_html)

    title = ""
    tm = TITLE_RE.search(src)
    if tm:
        title = text_of(tm.group(1))

    title_html = None
    notion = NOTION_ARTICLE_RE.search(body)
    if notion:
        flavour = "notion"
        inner = notion.group(1)
        pt = PAGE_TITLE_RE.search(inner)
        if pt:
            title_html = pt.group(1).strip() or None
            title = text_of(pt.group(1)) or title
        # the export's own <header> becomes our .post-head — drop it once
        inner = NOTION_HEADER_RE.sub("", inner, count=1)
        body = inner
    else:
        flavour = "vscode"
        start = LEADING_JUNK_RE.match(body).end()
        h1 = H1_RE.match(body, start)      # the first heading, scaffolding aside
        if h1:
            title_html = h1.group(1).strip() or None
            # <title> is already flat text; only fall back to the heading
            title = title or text_of(h1.group(1))
            body = body[: h1.start()] + body[h1.end():]

    if not title:
        title = title_from_basename(basename)

    return build(basename, title, iso_date, human_date, flavour, body,
                 title_html=title_html)


def main():
    targets = sys.argv[1:] or sorted(glob.glob(os.path.join(ROOT, "files", "*.html")))
    for path in targets:
        out = convert(path)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(out)
        print(f"restyled {os.path.relpath(path, ROOT)}")


if __name__ == "__main__":
    main()

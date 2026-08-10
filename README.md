# venillalemon.github.io

Personal site of Fangke Li — Jekyll, hosted on GitHub Pages.

## Layout

| Path | What it is |
| --- | --- |
| `_pages/about.md` | home page (`/`) |
| `_pages/year-archive.html` | blog index (`/blog/`), built from the files in `files/` |
| `files/*.html` | the posts themselves — standalone HTML exports |
| `assets/css/site.css` | theme for the Jekyll pages |
| `assets/css/post.css` | theme for the exported posts |
| `_tools/restyle_posts.py` | re-shells `files/*.html` into the site style |
| `markdown_generator/`, `talkmap.py` | generators kept from the original template |

## Adding a post

Drop the export in `files/` named `YYYY_MM_DD_some_title.html`, then run:

```bash
python3 _tools/restyle_posts.py
```

It keeps the exported body verbatim and swaps the surrounding document for the
site's header, footer and stylesheet. It is idempotent — re-run it after any
change to `post.css` or the post chrome. Both VS Code Markdown and Notion
exports are handled. The blog index picks the file up automatically.

## Writing a post in Markdown

```bash
pip install markdown pygments
```

```bash
python3 _tools/md_to_post.py notes/turan.md
```

Front matter is optional and only `title` / `date` are read:

```markdown
---
title: Turán's Theorem
date: 2026-08-09
---
```

Otherwise the title comes from the first `# heading` (which is then lifted into
the post header, not repeated in the body), and the date from a `YYYY_MM_DD_`
filename prefix, else today. `--title`, `--date` and `--out` override.

Supported: headings (with anchor ids), `*em*` `**strong**` `~~del~~`, links and
reference links, images, nested lists, task lists (`- [ ]` / `- [x]`), pipe
tables, fenced and indented code (highlighted by Pygments), blockquotes, `---`
rules, footnotes, definition lists, abbreviations, `{: #id }` on headings, raw
HTML, two-space hard line breaks, and smart quotes/dashes. Math stays as
`$...$`, `$$...$$`, `\(...\)`, `\[...\]` and is rendered by KaTeX in the browser.

Not supported — these stay literal: bare-URL autolinking (write `[text](url)`),
GitHub `> [!NOTE]` alerts, `:emoji:` shortcodes, and LaTeX macro preambles
(`\def` / `\newcommand` definitions do not carry from one `$…$` to the next).
Image paths must be site-absolute (`/images/x.png`), since posts are served
from `/files/`.

## Running locally

The system Ruby is too old for this Gemfile; use a modern one (e.g.
`brew install ruby@3.1`):

```bash
export PATH="/opt/homebrew/opt/ruby@3.1/bin:$PATH" && bundle install
```

```bash
export PATH="/opt/homebrew/opt/ruby@3.1/bin:$PATH" && bundle exec jekyll serve --config _config.yml,_config.dev.yml --livereload
```

`_config.dev.yml` points `url` at `localhost:4000`; without it the local build
loads its CSS from the production domain.

## Credit

Started from [academicpages](https://github.com/academicpages/academicpages.github.io),
a fork of [Minimal Mistakes](https://github.com/mmistakes/minimal-mistakes)
(MIT). The theme's own stylesheets and layouts have since been replaced.

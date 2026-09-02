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
| `md/` | Markdown sources kept as backups — excluded from the build, never published |

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

No dependencies — the converter is stdlib-only:

```bash
python3 _tools/md2html.py md/2026_08_31_some_title.md
```

writes `files/<same-stem>.html`, shelled by `restyle_posts.build()` so the
chrome (header, footer, theme toggle, analytics) always matches the site.
`--out`, `--title` and `--date` override the defaults.

The title comes from the first `# heading` (lifted into the post header, not
repeated in the body), the date from a `*March 15, 2026*` line under it or the
`YYYY_MM_DD_` filename prefix. Frontmatter with `title:` / `date:` also works.
The dialect is exactly what `html2md.py` emits (the two are inverses, verified
by round-tripping every file in `md/`): headings, `*em*` `**strong**` `~~del~~`,
links, images, inline `code`, fenced code blocks, nested `-` / `1.` lists,
`> ` blockquotes, pipe tables (`\|` escapes a pipe in a cell), `---` rules, and
raw HTML blocks (`<details>` etc.). Math stays as `$...$` / `$$...$$` (also
`\(...\)` / `\[...\]`) and is rendered by KaTeX in the browser; a literal `$`
in prose is left alone as long as it isn't glued to non-space text on both
sides. Not supported: underscore emphasis (a literal `_` stays literal),
footnotes, task lists, autolinking. Image paths must be site-absolute
(`/images/x.png`), since posts are served from `/files/`.

## Backing up posts as Markdown

`md/` holds Markdown versions of the posts, reconstructed from the restyled
HTML (LaTeX recovered from the KaTeX annotations). Regenerate with:

```bash
python3 _tools/html2md.py md files/*.html
```

First argument is the output directory; the rest are the posts to convert.
PDF-embed posts become a stub linking to the PDF. `md/` is excluded from the
Jekyll build — these files never appear on the site.

## Running locally

### Install (once)

The macOS system Ruby (2.6) is too old for this Gemfile — it can't even run the
required bundler. Install a modern Ruby via Homebrew and let bundler fetch the
gems:

```bash
brew install ruby@3.1
export PATH="/opt/homebrew/opt/ruby@3.1/bin:$PATH"
bundle install
```

### Run

```bash
export PATH="/opt/homebrew/opt/ruby@3.1/bin:$PATH"
bundle exec jekyll serve --config _config.yml,_config.dev.yml --livereload
```

Then open <http://127.0.0.1:4000>. The `export PATH` line is needed in every
new shell (or add it to `~/.zshrc` to make it permanent).

`_config.dev.yml` points `url` at `localhost:4000`; without it the local build
loads its CSS from the production domain. Drop `--livereload` if you don't want
auto-refresh; use `bundle exec jekyll build` to just build into `_site/`.

## Credit

Started from [academicpages](https://github.com/academicpages/academicpages.github.io),
a fork of [Minimal Mistakes](https://github.com/mmistakes/minimal-mistakes)
(MIT). The theme's own stylesheets and layouts have since been replaced.

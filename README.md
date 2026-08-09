# venillalemon.github.io

Personal site of Fangke Li (Mike Li) — Jekyll, hosted on GitHub Pages.

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

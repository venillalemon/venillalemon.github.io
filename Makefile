.PHONY: run

# Rebuild every note in files/ from its Markdown source in md/.
# Filenames contain ':' and quotes, so this uses a shell glob instead of Make targets.
run:
	python3 _tools/md2html.py md/*.md

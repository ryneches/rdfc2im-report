# Build the lightning talk.  XeLaTeX runs twice: the footer, seal and logo strip are placed
# relative to the page, which needs a second pass.
slides.pdf: slides.tex ecosystem.pdf ../paper/figure3-gwas-template.png $(wildcard logos/*)
	xelatex -interaction=nonstopmode -halt-on-error slides.tex
	xelatex -interaction=nonstopmode -halt-on-error slides.tex

# ecosystem.pdf is drawn by the report's figure script.
ecosystem.pdf: ../tools/make_figures.py
	cd .. && python3 tools/make_figures.py

clean:
	rm -f slides.aux slides.log slides.nav slides.out slides.snm slides.toc slides.vrb

.PHONY: clean

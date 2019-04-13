# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = mobility_pipeline
SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Run sphinx-apidoc to generate the API documentation skeleton files
apidoc:
	@sphinx-apidoc -fo "$(SOURCEDIR)" "../$(SPHINXPROJ)"

copy-rst:
	@cp -f "../CONTRIBUTING.rst" "$(SOURCEDIR)/generated/CONTRIBUTING.rst"
	@cp -f "../GETTING_STARTED.rst" "$(SOURCEDIR)/generated/GETTING_STARTED.rst"

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile apidoc copy-rst
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
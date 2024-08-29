## Process this file with automake to produce Makefile.in
## Created by Anjuta


uidir = $(pkgdatadir)/ui
ui_DATA = cornell_grape_bud_tester.ui


## The main script
bin_SCRIPTS = cornell_grape_bud_tester.py

## Directory where .class files will be installed
cornell_grape_bud_testerdir = $(pythondir)/cornell_grape_bud_tester


cornell_grape_bud_tester_PYTHON = \
	cornell_grape_bud_tester.py


EXTRA_DIST = $(ui_DATA)


# Remove ui directory on uninstall
uninstall-local:

	-rm -r $(uidir)

	-rm -r $(pkgdatadir)

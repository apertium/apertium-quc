###############################################################################
## Makefile for apertium-quc
###############################################################################

LANG1=quc
BASENAME=apertium-$(LANG1)

TARGETS_COMMON =			\
	$(LANG1).automorf.hfst		\
	$(LANG1).automorf.bin		\
	$(LANG1).automorf.att.gz	\
	$(LANG1).autogen.hfst		\
	$(LANG1).autophon.hfst		\
	$(LANG1).autogen.bin		\
	$(LANG1).autogen.att.gz		\
	$(LANG1).autoseg.hfst		\
	$(LANG1).autoseg.bin		\
	$(LANG1).rlx.bin

TARGETS_INTERMEDIATE = $(LANG1).mor.hfst $(LANG1).seg.hfst $(LANG1).gen.hfst

# This include defines goals for install-modes, .deps/.d and .mode files:
@ap_include@

###############################################################################

quc.automorf.hfst: quc.mor.hfst quc.spellrelax.hfst
	hfst-invert $< |  hfst-compose -F -1 - -2 quc.spellrelax.hfst  | hfst-invert | hfst-fst2fst -w -o $@

quc.autogen.hfst: quc.gen.hfst
	hfst-fst2fst -w $< -o $@

quc.autoseg.hfst: quc.seg.hfst 
	hfst-fst2fst -w $< -o $@

quc.mor.hfst: quc.gen.hfst quc.mor.twol.hfst
	hfst-compose-intersect -1 quc.gen.hfst -2 quc.mor.twol.hfst | hfst-invert -o $@

# <impf><o_pl1><s_pl3>tʼis<v><tv>+o<mark>:k>oj>ki>tʼis>o
quc.gen.hfst: quc.lexc.hfst quc.twol.hfst
	hfst-compose-intersect -1 quc.lexc.hfst -2 quc.twol.hfst -o $@

quc.twol.hfst: apertium-quc.quc.twol
	hfst-twolc $< -o $@

# <impf><o_pl1><s_pl3>tʼis<v><tv>+o<mark>:k>{o}j>k{i}>tʼis>o
quc.lexc.hfst: apertium-quc.quc.lexc
	hfst-lexc -A --Werror $< -o $@

quc.mor.twol.hfst: apertium-quc.quc.mor.twol
	hfst-twolc apertium-quc.quc.mor.twol -o quc.mor.twol.hfst

# kojkitʼiso:k>oj>ki>tʼis>o
quc.seg.hfst: quc.mor.hfst quc.gen.hfst
	hfst-compose -F -1 quc.mor.hfst -2 quc.gen.hfst -o quc.seg.hfst 

quc.phon.hfst: apertium-quc.quc.phon
	hfst-regexp2fst -S apertium-quc.quc.phon | hfst-repeat -o quc.phon.hfst

quc.autophon.hfst: quc.mor.hfst quc.phon.hfst
	hfst-fst2fst -w quc.phon.hfst -o quc.autophon.hfst
#	hfst-project -p upper quc.mor.hfst | hfst-compose -1 - -2 quc.phon.hfst | hfst-fst2fst -w -o quc.autophon.hfst

quc.spellrelax.hfst: apertium-quc.quc.spellrelax 
	hfst-regexp2fst -S -o $@ < $<

quc.rlx.bin: apertium-quc.quc.rlx
	cg-comp $< $@

$(LANG1).autogen.att.gz: $(LANG1).gen.hfst
	hfst-fst2txt $< | gzip -9 -c > $@

$(LANG1).automorf.att.gz: $(LANG1).mor.hfst quc.spellrelax.hfst
	hfst-invert $< |  hfst-compose -F -1 - -2 quc.spellrelax.hfst  | hfst-invert | hfst-fst2txt | gzip -9 -c > $@

$(LANG1).autoseg.att.gz: $(LANG1).seg.hfst
	hfst-fst2txt $< | gzip -9 -c > $@

$(LANG1).autogen.bin: $(LANG1).autogen.att.gz .deps/.d
	zcat < $< > .deps/$(LANG1).autogen.att
	lt-comp lr .deps/$(LANG1).autogen.att $@

$(LANG1).automorf.bin: $(LANG1).automorf.att.gz .deps/.d
	zcat < $< > .deps/$(LANG1).automorf.att
	lt-comp lr .deps/$(LANG1).automorf.att $@

$(LANG1).autoseg.bin: $(LANG1).autoseg.att.gz .deps/.d
	zcat < $< > .deps/$(LANG1).autoseg.att
	lt-comp lr .deps/$(LANG1).autoseg.att $@

###############################################################################
## Distribution
###############################################################################

EXTRA_DIST=$(BASENAME).$(LANG1).lexc		\
		$(BASENAME).$(LANG1).twol	\
		$(BASENAME).$(LANG1).spellrelax \
		$(BASENAME).$(LANG1).rlx	\
		modes.xml

###############################################################################
## Installation stuff
###############################################################################
#
#   apertium_quc_dir: This is where the compiled binaries go
#   apertium_quc_srcdir: This is where the source files go

apertium_qucdir=$(prefix)/share/apertium/$(BASENAME)/
apertium_quc_srcdir=$(prefix)/share/apertium/$(BASENAME)/

EXTRA_TARGETS=

if HAVE_HFSTOSPELL
EXTRA_TARGETS += $(LANG1).zhfst
endif # HAVE_HFSTOSPELL

apertium_quc_DATA=$(TARGETS_COMMON) $(EXTRA_TARGETS) 

pkgconfigdir = $(prefix)/share/pkgconfig
pkgconfig_DATA = $(BASENAME).pc

noinst_DATA=modes/$(LANG1)-morph.mode

install-data-local: install-modes
	$(INSTALL_DATA) $(BASENAME).$(LANG1).lexc $(DESTDIR)$(apertium_quc_srcdir)
	$(INSTALL_DATA) $(BASENAME).$(LANG1).twol $(DESTDIR)$(apertium_quc_srcdir)
	$(INSTALL_DATA) $(BASENAME).$(LANG1).rlx $(DESTDIR)$(apertium_quc_srcdir)


###############################################################################
## Cleanup
###############################################################################

CLEANFILES = $(TARGETS_COMMON) $(TARGETS_INTERMEDIATE)
clean-local:
	-rm -rf .deps modes

###############################################################################

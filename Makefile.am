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
	$(LANG1).autogen.bin		\
	$(LANG1).autogen.att.gz		\
	$(LANG1).autoseg.hfst		\
	$(LANG1).autoseg.bin		\
	$(LANG1).rlx.bin

# This include defines goals for install-modes, .deps/.d and .mode files:
@ap_include@

###############################################################################

quc.mor.hfstol: quc.mor.hfst 
	hfst-fst2fst -w $< -o $@

quc.gen.hfstol: quc.gen.hfst
	hfst-fst2fst -w $< -o $@

quc.seg.hfstol: quc.seg.hfst 
	hfst-fst2fst -w $< -o $@

quc.mor.hfst: quc.gen.hfst quc.mor.twol.hfst quc.spellrelax.hfst
	hfst-compose-intersect -1 quc.gen.hfst -2 quc.mor.twol.hfst | hfst-compose -F -1 - -2 quc.spellrelax.hfst | hfst-invert -o $@

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

quc.spellrelax.hfst: apertium-quc.quc.spellrelax 
	hfst-regexp2fst -S -o $@ < $<

quc.rlx.bin: apertium-quc.quc.rlx
	cg-comp $< $@

quc.automorf.att.gz: quc.mor.hfst
	hfst-fst2txt quc.mor.hfst | gzip -9 > $@

quc.autogen.att.gz: quc.gen.hfst
	hfst-fst2txt quc.gen.hfst | gzip -9 > $@

quc.autogen.bin: quc.autogen.att.gz

modes/quc-morph.mode: modes.xml
	apertium-gen-modes modes.xml

###############################################################################
## Cleanup
###############################################################################

CLEANFILES = $(TARGETS_COMMON)
clean-local:
	-rm -rf .deps modes

###############################################################################


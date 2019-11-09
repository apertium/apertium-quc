all: quc.mor.hfst quc.mor.hfstol
quc.lexc.hfst: apertium-quc.quc.lexc
	hfst-lexc --Werror $< -o $@
quc.twol.hfst: apertium-quc.quc.twol
	hfst-twolc -i $< -o $@
quc.gen.hfst: quc.lexc.hfst quc.twol.hfst
	hfst-compose-intersect -1 quc.lexc.hfst -2 quc.twol.hfst -o $@
quc.mor.hfst: quc.gen.hfst
	hfst-invert $< -o $@
quc.mor.hfstol: quc.mor.hfst
	hfst-fst2fst -w $< -o $@

clean:
	rm -f *.hfst *.hfstol

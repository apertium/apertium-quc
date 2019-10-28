all: quc.mor.hfst
quc.lexc.hfst: apertium-quc.quc.lexc
	hfst-lexc $< -o $@
quc.twol.hfst: apertium-quc.quc.twol
	hfst-twolc -i $< -o $@
quc.gen.hfst: quc.lexc.hfst quc.twol.hfst
	hfst-compose-intersect -1 quc.lexc.hfst -2 quc.twol.hfst -o $@
quc.mor.hfst: quc.gen.hfst
	hfst-invert $< -o $@

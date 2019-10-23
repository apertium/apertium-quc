all: quc.lexc.hfst
quc.lexc.hfst: apertium-quc.quc.lexc
	hfst-lexc $< -o $@

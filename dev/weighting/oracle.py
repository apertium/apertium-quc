import sys

refl = open(sys.argv[1]).read()

ws = []
dico = {}

for line in refl.split('\n'):
	line = line.strip()
	if line == '':
		continue
	(surface, analysis) = line[1:-1].split('/')
	
	if surface not in dico:
		dico[surface] = {}
	if analysis not in dico[surface]:
		dico[surface][analysis] = 0
	dico[surface][analysis] += 1
	ws.append(surface)

for surf in ws:
	m = max(dico[surf])

	print('^%s/%s$' % ( surf, m))

import sys 

refl = open(sys.argv[1]).readlines()
tstl = open(sys.argv[2]).readlines()

if len(refl) != len(tstl):
	print(refl,'!=',tstl)
	sys.exit(-1)

dico = {}

for line in refl:
	line = line.strip()
	row = line[1:-1].split('/')
	surface = row[0]
	analyses = row[1:]
	if len(row) != 2:
		print(row,file=sys.stderr)
	if surface not in dico:
		dico[surface] = []
	dico[surface] = list(set(dico[surface] + analyses))

tp = 0 # analysis in output & in reference
fp = 0 # analysis in output ! in reference
tn = 0 # 
fn = 0 # analysis in reference ! in output

analyser = {}

missing = []

for line in tstl:
	line = line.strip()
	row = line[1:-1].split('/')
	surface = row[0]
	analyses = row[1:]
	if surface not in analyser:
		analyser[surface] = []

	for ta in analyses:
		if ta in dico[surface]:
			tp += 1	
		else:
			fp += 1
		if ta not in analyser[surface]:
			analyser[surface] = list(set(analyser[surface] + analyses))

for surface in dico:
	for ra in dico[surface]:
		if ra not in analyser[surface]:
			fn += 1	
			missing.append((surface, ra))

print('= TOKEN ==================================================================================')

print('TP:',tp)
print('TN:',tn)
print('FP:',fp)
print('FN:',fn)

P = tp / (tp + fp)
R = tp / (tp + fn)
F = 2 * ((P*R) / (P+R))
print('P:',P)
print('R:',R)
print('F:',F)

for m in missing:
	print(m)

print('= TYPE ==================================================================================')

tp = 0 # analysis in output & in reference
fp = 0 # analysis in output ! in reference
tn = 0 # 
fn = 0 # analysis in reference ! in output

for surface in analyser:
	for ta in analyser[surface]:
		if ta in dico[surface]:
			tp += 1	
		else:
			fp += 1
	for ra in dico[surface]:
		if ra not in analyser[surface]:
			fn += 1

print('TP:',tp)
print('TN:',tn)
print('FP:',fp)
print('FN:',fn)

P = tp / (tp + fp)
R = tp / (tp + fn)
F = 2 * ((P*R) / (P+R))
print('P:',P)
print('R:',R)
print('F:',F)


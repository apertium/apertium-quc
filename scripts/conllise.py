"""
	This script creates a CoNLL-U file from two input files:
	1) DEP_FILE ... This is a list of sentences in VISLCG3 format
	2) SEG_FILE ... This is a list of sentences in Apertium format
"""
import sys

# comments
# "<chawe>"
#	"chi" pr @case #3->4
#		"awe" prn pers p2 sg @obl #4->2

def get_surface_cg(line):
	return line[2:-2]

def get_lemma_cg(line):
	beg = line.find('"') + 1
	end = line.rfind('"')
	return line[beg:end]

def get_deps_cg(line): 
	return [int(i) for i in line.split('#')[1].split('->')]

def get_func_cg(line):
	for i in line.strip().split(' '):
		if len(i) > 1 and i[0] == '@':
			return i[1:]

# forms = {}
# forms[0] = ("chawe", [(3, "_", "chi", "_", "_", "_", 4), (4, "_", "awe", "_", "_", "_", 2)])
def get_tokens(sent):
	tokens = {}
	counter = -1	
	for line in sent.split('\n'):
		line = line.strip('\n ')
		if line == '': continue
		if line[0] == '"':
			counter += 1
			tokens[counter] = (get_surface_cg(line), [])
		elif line[0] == '\t':
			deps = get_deps_cg(line)
			tokens[counter][1].append((deps[0], '_', get_lemma_cg(line), '_', '_', '_', deps[1], get_func_cg(line), '_', '_'))
		else:
			continue
	return tokens	

# segs[0] = ("chawe", ["ch", "awe"])
def get_segmentations(sent):
	segmentations = {}
	counter = 0
	for line in sent.split('\n'):
		line = line.strip()
		if line == '': continue
		if line[0] != '^':
			continue
		(surface, segmentation) = line[1:-1].split('/')	
		segmentations[counter] = (surface, segmentation.split('>')) 
		counter += 1	
	return segmentations

def get_comments(sent):
	comments = []
	for line in sent.strip().split('\n'):
		if line[0] == '#':
			comments.append(line)
	return '\n'.join(comments)

###############################################################################

if len(sys.argv) != 3:
	print(sys.argv, file=sys.stderr)
	print('conllise.py DEP_FILE SEG_FILE', file=sys.stderr)
	sys.exit(-1)

sents_dep = open(sys.argv[1]).read().split('\n\n')
sents_seg = open(sys.argv[2]).read().split('\n\n')

if len(sents_dep) != len(sents_seg):
	print('ERROR:', sys.argv, file=sys.stderr)
	print('ERROR:', len(sents_dep), len(sents_seg), file=sys.stderr)
	sys.exit(-1)

for i in range(0, len(sents_dep)):
	comments = get_comments(sents_dep[i])
	segmentations = get_segmentations(sents_seg[i])
	tokens = get_tokens(sents_dep[i])
#	print(tokens)

	if len(tokens) != len(segmentations):
		print('ERROR:',tokens, file=sys.stderr)	
		print('ERROR:',segmentations, file=sys.stderr)	
		continue

	print(comments)
	for j in range(0, len(tokens)):
		token = tokens[j]
		if len(token[1]) > 1:
			# {2: ('chawe', [(3, '_', 'chi', '_', '_', '_', 4, '_', '_', '_'), (4, '_', 'awe', '_', '_', '_', 2, '_', '_', '_')])
			print('%d-%d\t%s\t_\t_\t_\t_\t_\t_\t_\t_' % (token[1][0][0], token[1][-1][0], token[0]))
			for (k, word) in enumerate(token[1]):
				print('%d\t%s\t%s\t%s\t%s\t%s\t%d\t%s\t%s\t%s' % (word[0], segmentations[j][1][k],word[2],'_','_','_',word[6],word[7],'_','_'))
				
		else:
			# {0: ('Rajawaxik', [(1, '_', 'rajawaxik', '_', '_', '_', 0, '_', '_', '_')])
			word = token[1][0]
			print('%d\t%s\t%s\t%s\t%s\t%s\t%d\t%s\t%s\t%s' % (word[0], token[0],word[2],'_','_','_',word[6],word[7],'_','_'))
#		print('@',tokens[j], segmentations[j])	
	print()

	
	

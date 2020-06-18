"""
	This script creates a CoNLL-U file from three input files:
	1) UDX_FILE ... This is a tab separated file with tagset correspondences
	2) DEP_FILE ... This is a list of sentences in VISLCG3 format
	3) SEG_FILE ... This is a list of sentences in Apertium format

	TODO:
		- Maybe mark the POS/lemma/dep differently from other tags?
"""

###############################################################################
import sys, re

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

def get_tags_cg(line):
	tags = []
	for i in line.strip().split(' '):
		if i[0] not in ['@', '"', '#']:
			tags.append(i)
	return '|'.join(tags)

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
			tags = get_tags_cg(line)
			tokens[counter][1].append((deps[0], '_', get_lemma_cg(line), '_', tags, '_', deps[1], get_func_cg(line), '_', '_'))
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

def merge_segmentations(segs, n):
	if n == 2:
		return [segs[0], ''.join(segs[1:])]
	return segs

def get_comments(sent):
	comments = []
	for line in sent.strip().split('\n'):
		if line[0] == '#':
			comments.append(line)
	return '\n'.join(comments)

def load_rules(f):
	rules = []
	for line in f:
		if line[0] == '#':
			continue
		row = line.strip().split('\t')
		if len(row) != 8:
			print('WARNING: Broken rule', file=sys.stderr)
			print(line, '||', row, file=sys.stderr)
			continue
		score = sum([i for (i, j) in enumerate(reversed(row[:4])) if j is not '_'])
		rule = (score, set([i for i in row[:4] if i is not '_']), row[4:])
#		print('RULE:',rule)
		rules.append(rule)
	rules.sort()
	rules.reverse()

	return rules

def apply_rules(rules, analysis):
	o = ['_', '_', [], '_']

	# (2, '_', 'kʼamanik', '_', 'v|iv|impf|s_sg3', '_', 1, 'x', '_', '_')
	msd = set([analysis[2], analysis[7]] + analysis[4].split('|'))

	remainder = msd
	for rule in rules:
		remainder = msd - rule[1]
		intersect = msd.intersection(rule[1])
		if intersect == rule[1]:
			for (i, j) in enumerate(rule[2]):
				if j == '_': continue
				if type(o[i]) == list:
					for k in j.split('|'):
						o[i].append(k)
				else:
					o[i] = j
			msd = remainder

	o[2].sort()
	o[2] = '|'.join(o[2])
	for i in range(0, len(o)):
		if o[i] == '':
			o[i] = '_'

	return (o, remainder)

def format_conllu_line(line):
	#       1   2   3   4   5   6   7   8   9   10
        return '%d\t%s\t%s\t%s\t%s\t%s\t%d\t%s\t%s\t%s' % line


###############################################################################

if len(sys.argv) != 4:
	print(sys.argv, file=sys.stderr)
	print('conllise.py UDX_FILE DEP_FILE SEG_FILE', file=sys.stderr)
	sys.exit(-1)

tag_rules = open(sys.argv[1]).readlines()
sents_dep = open(sys.argv[2]).read().split('\n\n')
sents_seg = open(sys.argv[3]).read().split('\n\n')

#if len(sents_dep) != len(sents_seg):
#	print('ERROR:', sys.argv, file=sys.stderr)
#	print('ERROR:', len(sents_dep), len(sents_seg), file=sys.stderr)
#	sys.exit(-1)
#
rules = load_rules(tag_rules)

sents_depseg = {}


# Loop through each of the sentences
for i in range(0, len(sents_dep)):
	sent_id_match = re.match('# sent_id = .*', sents_dep[i])
	if not sent_id_match:
		continue
	if sents_dep[i].count('->') != len(re.findall('\n\t', sents_dep[i])):
		print('WARNING: Unannotated sentence,', sent_id_match[0], file=sys.stderr)
		continue
	sent_id = sent_id_match[0]
	if sent_id not in sents_depseg:
		sents_depseg[sent_id] = {}
	sents_depseg[sent_id][0] = sents_dep[i]

for i in range(0, len(sents_seg)):
	sent_id_match = re.match('# sent_id = .*', sents_seg[i])
	if not sent_id_match:
		continue
	sent_id = sent_id_match[0]
	if sent_id not in sents_depseg:
		sents_depseg[sent_id] = {}
	sents_depseg[sent_id][1] = sents_seg[i]


for depseg in sents_depseg:
	#print('-->', depseg, file=sys.stderr)
	if len(sents_depseg[depseg]) != 2:
		if 0 not in sents_depseg[depseg]:
			print(depseg, '| WARNING: Empty parse', file=sys.stderr)
		if 1 not in sents_depseg[depseg]:
			print(depseg, '| WARNING: Empty segmentation', file=sys.stderr)
		continue

	parse = sents_depseg[depseg][0]
	comments = get_comments(parse)
	tokens = get_tokens(parse)
	segmentations = get_segmentations(sents_depseg[depseg][1])

#	print(tokens)

	if len(tokens) != len(segmentations):
		print('ERROR:',tokens, file=sys.stderr)
		print('ERROR:',segmentations, file=sys.stderr)
		continue

	print(comments)
	for j in range(0, len(tokens)):
		token = tokens[j]
		if len(token[1]) > 1: # This is a multi-token word
			# {2: ('chawe', [(3, '_', 'chi', '_', '_', '_', 4, '_', '_', '_'), (4, '_', 'awe', '_', '_', '_', 2, '_', '_', '_')])}
			segs = segmentations[j][1]
			if len(tokens[1]) != len(segmentations[j][1]):
				segs = merge_segmentations(segmentations[j][1], len(token[1]))
			print('%d-%d\t%s\t_\t_\t_\t_\t_\t_\t_\t_' % (token[1][0][0], token[1][-1][0], token[0]))
			for (k, word) in enumerate(token[1]):
				(analysis, misc) = apply_rules(rules, word)
				#       1        2                       3        4            5    6            7        8        9    10
				line = (word[0], segs[k], word[2], analysis[1], '_', analysis[2], word[6], word[7], '_', '_')
				print(format_conllu_line(line))
		else:
			# {0: ('Rajawaxik', [(1, '_', 'rajawaxik', '_', '_', '_', 0, '_', '_', '_')])}
			word = token[1][0]
			(analysis, misc) = apply_rules(rules, word)
			#       1        2         3        4            5    6            7        8        9    10
			line = (word[0], token[0], word[2], analysis[1], '_', analysis[2], word[6], word[7], '_', '_')
			print(format_conllu_line(line))
	print()

###############################################################################


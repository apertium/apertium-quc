import sys, random

for line in sys.stdin.readlines():
	x = line.strip()[1:-1].split('/')
	y = x[1:]
	random.shuffle(y)
	print('^%s/%s$' % (x[0], y[0]))



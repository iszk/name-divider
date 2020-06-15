import sys

def parse_name(filename):
	with open(filename) as f:
		lines = f.readlines()
		cnt = 0
		for l in lines:
			cnt = cnt + 1
			names = l.strip().split('\t')
			family = names[0]
			given = names[1]
			f_chars = list(family)
			g_chars = list(given)
			for i, c in enumerate(f_chars):
				word_idx = i+1
				length = len(family)
				print('{}\tfamily\t{}\t{}'.format(c, word_idx, length))
			for i, c in enumerate(g_chars):
				word_idx = i+1
				length = len(given)
				print('{}\tgiven\t{}\t{}'.format(c, word_idx, length))

def max4(i: int) -> int:
	if i < 4:
		return i
	return 4

def len4(s: str) -> int:
	return max4(len(s))

if __name__ == '__main__':
	argv = sys.argv
	if len(argv) != 2:
		print("usage\n\tpython {} filename".format(argv[0]))
		sys.exit(-1)
	parse_name(argv[1])

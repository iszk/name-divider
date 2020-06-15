import sys

def chars2map(filename):
	all_chars = {}
	with open(filename) as f:
		lines = f.readlines()
		for l in lines:
			c, tp, at, ln = l.strip().split('\t')
			target = all_chars.get(c) or {
				'char': c,
				'fidx': [0, 0, 0],
				'gidx': [0, 0, 0],
				'flen': [0, 0, 0, 0],
				'glen': [0, 0, 0, 0],
				'all': 0,
			}
			target['all'] = target['all'] + 1
			klen = tp[0] + 'len'
			if tp == 'family':
				if at == ln:
					target['fidx'][2] = target['fidx'][2] + 1
				elif at == '1':
					target['fidx'][0] = target['fidx'][0] + 1
				else:
					target['fidx'][1] = target['fidx'][1] + 1

			else:
				if at == '1':
					target['gidx'][0] = target['gidx'][0] + 1
				elif at == ln:
					target['gidx'][2] = target['gidx'][2] + 1
				else:
					target['gidx'][1] = target['gidx'][1] + 1

			lng = int(ln) - 1
			if lng > 3:
				lng = 3
			target[klen][lng] = target[klen][lng] + 1
			all_chars[c] = target

	to_del = []
	for c, v in all_chars.items():
		if v['all'] < 1:
			to_del.append(c)

	for c in to_del:
		del all_chars[c]

	print("CHARS_MAP = " + repr(all_chars))

if __name__ == '__main__':
	argv = sys.argv
	if len(argv) != 2:
		print("usage\n\tpython {} filename".format(argv[0]))
		sys.exit(-1)
	chars2map(argv[1])


import chars_map
from typing import List

CMAP = chars_map.CHARS_MAP

def get_cmap(name: str, char_at: int) -> dict:
	chars = list(name)
	c = chars[char_at]
	cmap = CMAP.get(c)
	if not cmap:
		cmap = {
			'fidx': [1, 0, 1],
			'gidx': [3, 1, 3],
			'flen': [1, 3, 1, 0],
			'glen': [1.5, 2, 0.5, 0],
		}
	return cmap

def scores_by_idx(name: str) -> List[int]:

	def name_detail_by_charat(name, char_at) -> List[int]:
		"""
		名前のchar_at番目の文字について、苗字が1...n文字だった場合にどれを使うかの一覧を出している
		"""
		length = len(name)
		cmap = get_cmap(name, char_at)
		ret = []
		xs = []
		if char_at == 0:
			xs = ['f2']
			ret.append(cmap['fidx'][2])
			for _ in range(0, length - 2):
				xs.append('f0')
				ret.append(cmap['fidx'][0])
		if char_at == length - 1:
			xs = ['g2'] * (length-2)
			xs.append('g0')
			ret.append(cmap['gidx'][0])
		count_g1 = char_at - 1
		if count_g1 > 0:
			for _ in range(0, count_g1):
				xs.append('g1')
				ret.append(cmap['gidx'][1])
		if len(xs) < length - 1:
			xs.append('g0')
			ret.append(cmap['gidx'][0])
		if len(xs) < length - 1:
			xs.append('f2')
			ret.append(cmap['fidx'][2])
		if len(xs) < length - 1:
			for _ in range(len(xs), length - 1):
				ret.append(cmap['fidx'][1])
				xs.append('f1')
		return ret

	word_x = []
	for i in range(0, len(name)):
		x = name_detail_by_charat(name, i)
		word_x.append(x)

	bumbos = []
	for i in range(0, len(word_x)):
		bumbo = 0
		for j in range(0, len(word_x[i])):
			bumbo = bumbo + word_x[i][j]
		if bumbo == 0:
			bumbo = 1
		bumbos.append(bumbo)
	scores = []
	for j in range(0, len(word_x[0])):
		score = 0
		for i in range(0, len(name)):
			score = score + (word_x[i][j] / bumbos[i])
		scores.append(score / len(name))
	return scores

def scores_by_len(name: str) -> List[int]:
	"""
	この苗字/名前に利用されている字が長さの面からありえそうかを出す
	"""

	def name_detail_by_charat(name, char_at) -> List[int]:
		"""
		名前のchar_at番目の文字について、苗字が1...n文字だった場合にどれを使うかの一覧を出している
		"""
		cmap = get_cmap(name, i)
		xxx = []
		ret = []
		for flen in range(1, len(name)):
			target = 'flen'
			idx = flen - 1
			if char_at >= flen:
				target = 'glen'
				idx = len(name) - flen - 1
			if idx > 3:
				idx = 3
			xxx.append(target + str(idx + 1))
			ret.append(cmap[target][idx])
		return ret

	word_x = []
	for i in range(0, len(name)):
		x = name_detail_by_charat(name, i)
		word_x.append(x)

	bumbos = []
	for i in range(0, len(word_x)):
		bumbo = 0
		for j in range(0, len(word_x[i])):
			bumbo = bumbo + word_x[i][j]
		if bumbo == 0:
			bumbo = 1
		bumbos.append(bumbo)
	scores = []
	for j in range(0, len(word_x[0])):
		score = 0
		for i in range(0, len(name)):
			score = score + (word_x[i][j] / bumbos[i])
		scores.append(score / len(name))
	return scores

def scores_by_rate(name: str) -> List[int]:
	"""
	単に苗字/名前に対する出現率だけを見る
	"""

	f_rates = []
	for char_at in range(0, len(name)):
		cmap = get_cmap(name, char_at)
		f_all = cmap['fidx'][0] + cmap['fidx'][1] + cmap['fidx'][2]
		fg_all = f_all + cmap['gidx'][0] + cmap['gidx'][1] + cmap['gidx'][2]
		f_rates.append(f_all / fg_all)

	scores = []
	for idx in range(1, len(name)):
		score = 0
		for i in range(0, len(f_rates)):
			if idx > i:
				score = score + f_rates[i]
			else:
				score = score + 1 - f_rates[i]
		scores.append(score / len(name))
	return scores

def divide(name):
	ssi = scores_by_idx(name)
	ssl = scores_by_len(name)
	ssr = scores_by_rate(name)
	idx = 0
	pmax = 0
	score = []
	for i in range(0, len(name) - 1):
		tp = ssi[i] + ssl[i] + ssr[i]
		score.append(tp)
		if pmax < tp:
			idx = i
			pmax = tp
	return name[:idx+1], name[idx+1:]

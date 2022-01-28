
def realCentre(s: str, size: int) :
	diff = max(0, size - len(s))
	left_pad = diff // 2
	right_pad = diff - left_pad
	return (" " * left_pad) + s + (" " * right_pad)

def createTable(ll: "list[list]", title=None) -> "list[str]" :
	res = []
	maxlen = max([len(l) for l in ll], default=0)
	ll = [[str(e) for e in l] + ([''] * (maxlen - len(l))) for l in ll]
	max_col = [max([len(l[i]) for l in ll]) for i in range(maxlen)]
	sep = "+" + "+".join(['-' * (c+2) for c in max_col]) + "+"
	if title is not None :
		res.append("+" + '-' * (len(sep) - 2) + "+")
		res.append("|" + realCentre(title, len(sep) - 2) + "|")
	res.append(sep)
	for l in ll :
		res.append("| " + " | ".join([str(l[i]).ljust(max_col[i]) for i in range(maxlen)]) + " |")
		res.append(sep)
	return res
	
def printTable(ll: "list[list]", title=None) :
	for l in createTable(ll, title) :
		print(l)

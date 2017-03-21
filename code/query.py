import music, language

_debug_ = False
replacements = [('full note', 'semibreve'), ('whole note', 'semibreve'), ('half note', 'minim'), ('quarter note', 'crotchet'), ('eighth note', 'quaver'), ('sixteenth note', 'semiquaver'), ('32nd note', 'demisemiquaver'), ('sharp', '#'), ('flat', 'b')]
translatetimes = {'semibreve': 4, 'minim': 2, 'crotchet': 1, 'quaver': 0.5, 'semiquaver': 0.25, 'demisemiquaver': 0.125}
prematch = lambda thing: thing.lower() if type(thing) == str else thing
match = lambda expectation, reality: not expectation or prematch(expectation) == prematch(reality)

def preprocess(line):
	for replacement in replacements:
		line = line.replace(*replacement)
	return line

def lookup(query, context):
	time, note, octave, meter, clef, instrument, initialposition, answerlist = None, None, None, None, None, None, 1, list()
	if query[2]: time = translatetimes[query[2][1]]
	if query[3]:
		note = query[3][0]
		if query[3][1]: note += query[3][1][0]
		if query[3][2]: octave = int(query[3][2][0])
	if query[8]:
		initialposition = int(query[8][1]) - 1
		for i in xrange(len(context)):
			context[i] = context[i][int(query[8][1]) - 1: int(query[8][3])]
	if query[9]: meter = ''.join(query[9][1: 4])
	if query[10]: clef = query[10][1]
	if query[11]: instrument = query[11][1]
	if _debug_: print time, note, octave, meter, clef, instrument, initialposition
	for part in context:
		position = initialposition
		for bar in part:
			for descriptor in bar:
				if match(time, descriptor[3]) and match(note, descriptor[0]) and match(meter, descriptor[6]) and match(clef, descriptor[7]) and match(instrument, descriptor[4]):
					answerlist.append([descriptor[6], 1 / descriptor[3], position, descriptor[2] / descriptor[3] + 1])
			position += 1
	return answerlist

if __name__ == '__main__':
	query = preprocess('quarter note G in bars 2-2 in 4/4 time in the bass')
	query = language.parse(query)
	context = 'data/f01.xml'
	context = music.parse(context)
	print lookup(query, context)

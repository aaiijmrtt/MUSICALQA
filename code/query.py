import music, language

replacements = [('full', 'semibreve'), ('whole note', 'semibreve'), ('half note', 'minim'), ('quarter note', 'crotchet'), ('eighth note', 'quaver'), ('sixteenth note', 'semiquaver'), ('32nd note', 'demisemiquaver'), ('sharp', '#'), ('flat', 'b')]
translatetimes = {'semibreve': 4, 'minim': 2, 'crotchet': 1, 'quaver': 0.5, 'semiquaver': 0.25, 'demisemiquaver': 0.125}

def preprocess(line):
	for replacement in replacements:
		line = line.replace(*replacement)
	return line

def checklist(string, iterableofstring):
	for checkstring in iterableofstring:
		if string.lower() == checkstring.lower(): return checkstring
	return False

def lookup(query, context):
	instruments = [query[11][1]] if query[11] else context.keys()
	for instrument in instruments:
		instrument = checklist(instrument, context)
		if not instrument: continue
		if query[9] and ''.join(query[9][1: 4]) != context[instrument]['meter']: continue
		if query[8]: bars = context[instrument]['bars'][int(query[8][1]): int(query[8][3]) + 1]
		else: bars = context[instrument]['bars']
		if query[3]:
			for bar in context[instrument]['bars']:
				for note in bar:
					if query[3][0] != note[0]: continue
					if query[2]:
						if translatetimes[query[2][0]] != note[3]: continue
					return True
	return False

if __name__ == '__main__':
	query = preprocess('quarter note G in bars 2-2 in 4/4 time in the bass')
	query = language.parse(query)
	context = 'data/f01.xml'
	context = music.parse(context)
	print lookup(query, context)

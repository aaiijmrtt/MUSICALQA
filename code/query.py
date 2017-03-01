replacements = [('full', 'semibreve'), ('whole', 'semibreve'), ('half', 'minim'), ('quater', 'crotchet'), ('eighth', 'quaver'), ('sixteenth', 'semiquaver'), ('32nd', 'demisemiquaver'), ('sharp', '#'), ('flat', 'b')]

def preprocess(line):
	for replacement in replacements:
		line = line.replace(*replacement)
	return line

print preprocess('half note D sharp')

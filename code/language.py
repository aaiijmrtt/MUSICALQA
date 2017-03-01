import pyparsing

def literals(literallist):
	return pyparsing.Or([pyparsing.Literal(literal) for literal in literallist])

times = literals(['breve', 'semibreve', 'minim', 'crotchet', 'quaver', 'semiquaver', 'demisemiquaver'])
augmentedtimes = literals(['dotted', 'double dotted'])
notes = literals(['B', 'C', 'D', 'E', 'F', 'G', 'Do', 'Re', 'Mi', 'Fa', 'Sol', 'La', 'Ti', 'do', 're', 'mi', 'fa', 'sol', 'la', 'ti'])
augmentednotes = literals(['#', 'b'])
octave = literals(['1', '2', '3', '4', '5', '6', '7'])
instruments = literals(['flute', 'oboe', 'violin', 'violin I', 'violin II', 'timpani', 'double basses', 'cello', 'bass', 'horn', 'piano', 'harpsichord'])
hands = literals(['right', 'left'])
conjunction = literals(['against', 'followed by'])

query = pyparsing.And([
	pyparsing.Optional(
		pyparsing.Or([
			pyparsing.Literal('chord'),
			pyparsing.Literal('melody')
		])
	),
	pyparsing.Group(
		pyparsing.ZeroOrMore(
			pyparsing.And([	
				pyparsing.Optional(augmentedtimes),
	   			times
			])
		)
	),
	pyparsing.Group(
		pyparsing.ZeroOrMore(
			pyparsing.And([
				notes,
				pyparsing.Optional(augmentednotes),
				pyparsing.Optional(octave)
	   		 ])
		)
	),
	pyparsing.Group(pyparsing.Optional(pyparsing.Literal('rest'))),
	pyparsing.Group(
		pyparsing.Optional(
			pyparsing.And([
				pyparsing.Literal('in bars'),
				pyparsing.OneOrMore(pyparsing.Word(pyparsing.nums)),
				pyparsing.Literal('-'),
				pyparsing.OneOrMore(pyparsing.Word(pyparsing.nums))
			])
		)
	),
	pyparsing.Group(
		pyparsing.Optional(
			pyparsing.And([
				pyparsing.Literal('in'),
				pyparsing.OneOrMore(pyparsing.Word(pyparsing.nums)),
				pyparsing.Literal('/'),
				pyparsing.OneOrMore(pyparsing.Word(pyparsing.nums)),
				pyparsing.Literal('time')
			]),
		)
	),
	pyparsing.Group(
		pyparsing.Optional(
			pyparsing.And([
				pyparsing.Literal('in the'),
				instruments
			])
		)
	)
])

compound = pyparsing.And([
	query,
	pyparsing.ZeroOrMore(
		pyparsing.And([
			conjunction,
			query
		])
	)
])

print query.parseString('dotted crotchet G6').asList()

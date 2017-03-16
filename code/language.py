import pyparsing

literals = lambda literallist: pyparsing.Or([pyparsing.Literal(literal) for literal in literallist])
times = literals(['breve', 'breves', 'semibreve','semibreves', 'minim', 'minims', 'crotchets', 'crotchet', 'quavers', 'quaver', 'semiquaver','semiquavers', 'demisemiquaver', 'demisemiquavers'])
augmentedtimes = literals(['dotted', 'double dotted'])
notes = literals(['B', 'C', 'D', 'E', 'F', 'G', 'Do', 'Re', 'Mi', 'Fa', 'Sol', 'La', 'Ti', 'do', 're', 'mi', 'fa', 'sol', 'la', 'ti'])
augmentednotes = literals(['#', 'b'])
octave = literals(['1', '2', '3', '4', '5', '6', '7'])
instruments = literals(['flute', 'oboe', 'violin', 'violin I', 'violin II', 'timpani', 'double basses', 'cello', 'bass', 'horn', 'piano', 'harpsichord'])
hands = literals(['right', 'left'])
conjunction = literals(['against', 'followed by'])
clef = literals(['bass', 'treble'])
alphanumerals = literals(['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve'])
passage = literals(['homophonic', 'monophonic', 'polyphonic'])

query = pyparsing.And([

	pyparsing.Group(
		pyparsing.Optional(
			pyparsing.Or([
				alphanumerals,
				pyparsing.OneOrMore(pyparsing.Word(pyparsing.nums))
			])
		)
	),

	pyparsing.Group(
		pyparsing.Optional(
			pyparsing.Or([
				pyparsing.Literal('chord'),
				pyparsing.Literal('melody')
			])
		)
	),
	pyparsing.Group(
		pyparsing.ZeroOrMore(
			pyparsing.And([	
				pyparsing.Group(pyparsing.Optional(augmentedtimes)),
	   			times
			])
		)
	),
	pyparsing.Group(
		pyparsing.ZeroOrMore(
			pyparsing.And([
				notes,
				pyparsing.Group(pyparsing.Optional(augmentednotes)),
				pyparsing.Group(pyparsing.Optional(octave))
	   		 ])
		)
	),

	pyparsing.Group(
		pyparsing.Optional(
			pyparsing.Or([
				pyparsing.Literal('rest'),
				pyparsing.Literal('notes'),
				pyparsing.Literal('note'),
				pyparsing.Literal('melody')
			])
		)
	),

	pyparsing.Group(
		pyparsing.Optional(
			pyparsing.And([
				alphanumerals,
				pyparsing.Or([
					pyparsing.Literal('note'),
					pyparsing.Literal('notes')
				]),
				pyparsing.Literal('melody')
			])
		)
	),

	pyparsing.Group(
		pyparsing.Optional(
			pyparsing.And([
				pyparsing.Literal("on the word &quot;"),
				pyparsing.ZeroOrMore(pyparsing.Word(pyparsing.alphas)),
				pyparsing.Literal("!&quot;")
			])
		)
	),

	pyparsing.Group(
		pyparsing.Optional(
			pyparsing.And([
				passage,
				pyparsing.Literal('passage')
			])
		)
	),

	pyparsing.Group(
		pyparsing.Optional(
			pyparsing.And([
				pyparsing.Or([
					pyparsing.Literal('in bars'),
					pyparsing.Literal('in measures')
                                ]),
				pyparsing.OneOrMore(pyparsing.Word(pyparsing.nums)),
				pyparsing.Or([
					pyparsing.Literal('-'),
					pyparsing.Literal('to')
				]),
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
				clef,
				pyparsing.Literal('clef')
			])
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

def parse(question):
	return query.parseString(question).asList()

if __name__ == '__main__':
	print parse('dotted crotchet G6')

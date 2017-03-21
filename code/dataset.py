import xml.etree.ElementTree

_debug_ = False

beatcorrect = lambda expectation, prediction: expectation[1] * expectation[3] == prediction[1] * prediction[3]
measurecorrect = lambda expectation, prediction: expectation[2] == prediction[2]
count = lambda listoflists: [len(sublist) for sublist in listoflists]

def prepare(inputfile, outputfile):
	printables = ['%s_%s' %(prefix, suffix) for prefix in ['start', 'end'] for suffix in ['beats', 'beat_type', 'bar', 'offset', 'divisions']]
	root = xml.etree.ElementTree.parse(inputfile).getroot()
	with open(outputfile, 'w') as fileout:
		for question in root:
			line = '%s\t%s\t' %(question.attrib['number'], question.attrib['music_file'])
			for part in question:
				if part.tag == 'text': line += '%s\t' %part.text
				else: line += '%s\n' %','.join([' '.join([answer.attrib[printable] for printable in printables]) for answer in part])
			fileout.write(line)
			if _debug_: print line.strip()


def metrics(expectations, predictions):
	beatslist, measureslist = list(), list()
	expectcount, predictcount = count(expectations), count(predictions)
	for expectation, prediction in zip(expectations, predictions):
		beatscorrect, measurescorrect = 0., 0.
		for predict in prediction:
			mcorrect, bcorrect = False, False
			for expect in expectation:
				if measurecorrect(expect, predict):
					mcorrect = True
					if beatcorrect(expect, predict):
						bcorrect = True
			if mcorrect: measurescorrect += 1
			if bcorrect: beatscorrect += 1
		beatslist.append(beatscorrect)
		measureslist.append(measurescorrect)
	if _debug_: print beatslist
	if _debug_: print measureslist
	return [beats / expects for beats, expects in zip(beatslist, expectcount)],\
		[beats / predicts for beats, predicts in zip(beatslist, predictcount)],\
		[measures / expects for measures, expects in zip(measureslist, expectcount)],\
		[measures / predicts for measures, predicts in zip(measureslist, predictcount)]

if __name__ == '__main__':
	prepare('data/dataset.xml', 'data/dataset')
	print metrics([[['4/4', 1., 1, 1.], ['4/4', 1., 2, 1.]], [['4/4', 1., 2, 2.]]], [[['4/4', 1., 1, 1.], ['4/4', 1., 2, 1.]], [['4/4', 1., 2, 2.]]])
	print metrics([[['4/4', 1., 1, 1.], ['4/4', 1., 2, 1.]], [['4/4', 1., 2, 2.]]], [[['4/4', 1., 1, 1.]], [['4/4', 1., 2, 2.]]])

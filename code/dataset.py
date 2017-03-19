import xml.etree.ElementTree

_debug_ = False

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

if __name__ == '__main__':
	prepare('data/dataset.xml', 'data/dataset')

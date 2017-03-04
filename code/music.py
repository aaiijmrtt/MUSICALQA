import inspect
import music21

def checkmodule(obj, mod):
	return isinstance(obj, tuple([cl for nm, cl in inspect.getmembers(mod, inspect.isclass)]))

music21.environment.set('musicxmlPath', '/usr/bin/musescore')

def parse(xmlfile):
	music, parsedmusic = music21.converter.parse(xmlfile, format = 'musicxml'), dict()
	for part in music:
		if checkmodule(part, music21.metadata): metadata = part
		elif checkmodule(part, music21.stream):
			for measure in part:
				if checkmodule(measure, music21.instrument):
					instrument = measure.partName
					parsedmusic[instrument] = {'bars': list()}
				elif checkmodule(measure, music21.stream):
					parsedmusic[instrument]['bars'].append(list())
					for note in measure:
						if checkmodule(note, music21.clef): parsedmusic[instrument]['clef'] = note
						elif checkmodule(note, music21.key): parsedmusic[instrument]['key'] = note
						elif checkmodule(note, music21.meter): parsedmusic[instrument]['meter'] = note.ratioString
						elif checkmodule(note, music21.bar): continue
						elif checkmodule(note, music21.layout): continue
						elif checkmodule(note, music21.note): parsedmusic[instrument]['bars'][-1].append((note.name, note.octave, note.offset, note.duration.quarterLength))
						else: print 'type not recognized', type(note)
				else: print 'type not recognized', type(measure)
		else: print 'type not recognized', type(part)
	return parsedmusic

if __name__ == '__main__':
	print parse('data/f01.xml')

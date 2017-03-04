import inspect
import music21

def checkmodule(obj, mod):
	return isinstance(obj, tuple([cl for nm, cl in inspect.getmembers(mod, inspect.isclass)]))

music21.environment.set('musicxmlPath', '/usr/bin/musescore')

def parse(music):
	parsedmusic = dict()
	for part in music:
		if checkmodule(part, music21.metadata): metadata = part
		elif checkmodule(part, music21.stream):
			for measure in part:
				if checkmodule(measure, music21.instrument):
					instrument = measure
					parsedmusic[instrument] = {'bars': [[]]}
				elif checkmodule(measure, music21.stream):
					for note in measure:
						if checkmodule(note, music21.clef): parsedmusic[instrument]['clef'] = note
						elif checkmodule(note, music21.key): parsedmusic[instrument]['key'] = note
						elif checkmodule(note, music21.meter): parsedmusic[instrument]['meter'] = note
						elif checkmodule(note, music21.bar): parsedmusic[instrument]['bars'].append(list())
						elif checkmodule(note, music21.layout): continue
						elif checkmodule(note, music21.note): parsedmusic[instrument]['bars'][-1].append((note.name, note.octave, note.offset, note.duration.quarterLength))
						else: print 'type not recognized', type(note)
				else: print 'type not recognized', type(measure)
		else: print 'type not recognized', type(part)
	return parsedmusic

if __name__ == '__main__':
	music = music21.converter.parse('data/f01.xml', format = 'musicxml')
	print parse(music)
	music.show()

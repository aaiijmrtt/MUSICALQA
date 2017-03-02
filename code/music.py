import inspect
import music21

def checkmodule(obj, mod):
	return isinstance(obj, tuple([cl for nm, cl in inspect.getmembers(mod, inspect.isclass)]))

music21.environment.set('musicxmlPath', '/usr/bin/musescore')
music = music21.converter.parse('data/f01.xml', format='musicxml')

for part in music:
	if checkmodule(part, music21.metadata): metadata = part
	elif checkmodule(part, music21.stream):
		for measure in part:
			if checkmodule(measure, music21.instrument): instrument = measure
			elif checkmodule(measure, music21.stream):
				for note in measure:
					if checkmodule(note, music21.clef): clef = note
					elif checkmodule(note, music21.key): key = note
					elif checkmodule(note, music21.meter): meter = note
					elif checkmodule(note, music21.bar): continue
					elif checkmodule(note, music21.layout): continue
					elif checkmodule(note, music21.note): print note.name, note.octave, note.offset, note.duration.quarterLength
					else: print 'type not recognized', type(note)
			else: print 'type not recognized', type(measure)
	else: print 'type not recognized', type(part)

music.show()

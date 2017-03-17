import inspect
import music21

_debug_ = False
music21.environment.set('musicxmlPath', '/usr/bin/musescore')
checkmodule = lambda obj, mod: isinstance(obj, tuple([cl for nm, cl in inspect.getmembers(mod, inspect.isclass)]))

def parse(xmlfile):
	music, parsedmusic = music21.converter.parse(xmlfile, format = 'musicxml'), list()
	for part in music:
		if checkmodule(part, music21.metadata): metadata = part
		elif checkmodule(part, music21.stream):
			for measure in part:
				if checkmodule(measure, music21.instrument):
					instrument = measure.partName
					parsedmusic.append(list())
				elif checkmodule(measure, music21.stream):
					parsedmusic[-1].append(list())
					for note in measure:
						if checkmodule(note, music21.clef): clef = note
						elif checkmodule(note, music21.key): key = note
						elif checkmodule(note, music21.meter): meter = note.ratioString
						elif checkmodule(note, music21.bar): parsedmusic[-1].append(list())
						elif checkmodule(note, music21.layout): continue
						elif checkmodule(note, music21.chord): continue
						elif checkmodule(note, music21.note):
							if note.isRest: continue
							parsedmusic[-1][-1].append((note.name, note.octave, note.offset, note.duration.quarterLength, instrument, key, meter, clef))
						elif _debug_: print 'type not recognized', type(note)
				elif _debug_: print 'type not recognized', type(measure)
		elif _debug_: print 'type not recognized', type(part)
	if _debug_: music.show()
	return parsedmusic

if __name__ == '__main__':
	print parse('data/f01.xml')

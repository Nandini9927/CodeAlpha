import glob
import pickle

from music21 import converter, instrument, note, chord

notes = []

for file in glob.glob("dataset/*.mid"):
    try:
        print("Reading:", file)

        midi = converter.parse(file)

        parts = instrument.partitionByInstrument(midi)

        if parts is not None and len(parts.parts) > 0:
            notes_to_parse = parts.parts[0].recurse()
        else:
            notes_to_parse = midi.flatten().notes

        for element in notes_to_parse:
            if isinstance(element, note.Note):
                notes.append(str(element.pitch))
            elif isinstance(element, chord.Chord):
                notes.append(".".join(str(n) for n in element.normalOrder))

    except Exception as e:
        print(f"Skipping {file}: {e}")

pickle.dump(notes, open("notes.pkl", "wb"))

print("Total Notes:", len(notes))
print("Preprocessing Completed!")
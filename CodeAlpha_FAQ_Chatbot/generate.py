import pickle
import random
import argparse
import numpy as np

from tensorflow.keras.models import load_model
from music21 import instrument as m21instrument
from music21 import note as m21note
from music21 import chord as m21chord
from music21 import stream

# ---------------- ARGUMENTS ---------------- #

parser = argparse.ArgumentParser()

parser.add_argument("--notes", type=int, default=500)
parser.add_argument("--temperature", type=float, default=1.0)
parser.add_argument("--instrument", type=str, default="Piano")

args = parser.parse_args()

NUM_NOTES = args.notes
TEMPERATURE = args.temperature
INSTRUMENT = args.instrument

# ---------------- LOAD MODEL ---------------- #

print("Loading model...")
model = load_model("music_model.keras")

notes_data = pickle.load(open("notes.pkl", "rb"))

pitchnames = sorted(set(notes_data))

n_vocab = len(pitchnames)

note_to_int = {n: i for i, n in enumerate(pitchnames)}
int_to_note = {i: n for i, n in enumerate(pitchnames)}

sequence_length = 100

start = random.randint(0, len(notes_data) - sequence_length - 1)

pattern = [note_to_int[n] for n in notes_data[start:start + sequence_length]]

output_notes = []

# ---------------- INSTRUMENT ---------------- #

def get_instrument():
    mapping = {
        "Piano": m21instrument.Piano(),
        "Guitar": m21instrument.Guitar(),
        "Violin": m21instrument.Violin(),
        "Flute": m21instrument.Flute(),
        "Trumpet": m21instrument.Trumpet()
    }
    return mapping.get(INSTRUMENT, m21instrument.Piano())

selected_instrument = get_instrument()

# ---------------- SAMPLING ---------------- #

def sample(predictions, temperature=1.0):
    predictions = np.asarray(predictions).astype("float64")

    predictions = np.log(predictions + 1e-8) / temperature
    exp_preds = np.exp(predictions)

    predictions = exp_preds / np.sum(exp_preds)

    top_k = 10
    top_indices = predictions.argsort()[-top_k:]
    top_probs = predictions[top_indices]

    top_probs = top_probs / np.sum(top_probs)

    return np.random.choice(top_indices, p=top_probs)

# ---------------- GENERATION ---------------- #

print("Generating music...")

for _ in range(NUM_NOTES):

    input_seq = np.reshape(pattern, (1, len(pattern), 1))
    input_seq = input_seq / float(n_vocab)

    prediction = model.predict(input_seq, verbose=0)[0]

    index = sample(prediction, TEMPERATURE)

    result = int_to_note[index]

    # ❗ SAFE CHECK (IMPORTANT FIX)
    if result is None or result == "":
        continue

    output_notes.append(result)

    pattern.append(index)
    pattern = pattern[1:]

# ---------------- CONVERT TO MIDI ---------------- #

offset = 0
midi_notes = []

for element in output_notes:

    # CHORD
    if "." in str(element):

        notes_in_chord = element.split(".")
        chord_notes = []

        for n in notes_in_chord:
            try:
                new_note = m21note.Note(int(n))
                new_note.storedInstrument = selected_instrument
                chord_notes.append(new_note)
            except:
                continue

        if len(chord_notes) > 0:
            new_chord = m21chord.Chord(chord_notes)
            new_chord.offset = offset
            midi_notes.append(new_chord)

    # SINGLE NOTE
    else:
        try:
            new_note = m21note.Note(element)
            new_note.offset = offset
            new_note.storedInstrument = selected_instrument
            midi_notes.append(new_note)
        except:
            continue

    offset += 0.5

# ---------------- STREAM ---------------- #

midi_stream = stream.Stream()
part = stream.Part()
part.insert(0, selected_instrument)

for n in midi_notes:
    part.append(n)

midi_stream.insert(0, part)

# ---------------- SAVE ---------------- #

midi_stream.write("midi", fp="generated_music.mid")

print("\n🎵 Music Generated Successfully!")
print("Instrument:", INSTRUMENT)
print("Notes:", NUM_NOTES)
print("Temperature:", TEMPERATURE)
print("Output: generated_music.mid")
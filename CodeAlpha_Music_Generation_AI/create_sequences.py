import pickle
import numpy as np

sequence_length = 100

notes = pickle.load(open("notes.pkl", "rb"))

pitchnames = sorted(set(notes))

note_to_int = {note: number for number, note in enumerate(pitchnames)}

network_input = []
network_output = []

for i in range(len(notes) - sequence_length):
    seq_in = notes[i:i + sequence_length]
    seq_out = notes[i + sequence_length]

    network_input.append([note_to_int[char] for char in seq_in])
    network_output.append(note_to_int[seq_out])

n_patterns = len(network_input)

network_input = np.reshape(network_input, (n_patterns, sequence_length, 1))
network_input = network_input / float(len(pitchnames))

pickle.dump(network_input, open("network_input.pkl", "wb"))
pickle.dump(network_output, open("network_output.pkl", "wb"))

print("Total Patterns:", n_patterns)
print("Unique Notes:", len(pitchnames))
print("Sequences Created Successfully!")
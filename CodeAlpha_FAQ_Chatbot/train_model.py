import pickle
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dropout, Dense
from tensorflow.keras.utils import to_categorical

network_input = pickle.load(open("network_input.pkl", "rb"))
network_output = pickle.load(open("network_output.pkl", "rb"))

n_vocab = len(np.unique(network_output))

network_output = to_categorical(network_output)

model = Sequential()

model.add(LSTM(256, input_shape=(network_input.shape[1], network_input.shape[2]), return_sequences=True))
model.add(Dropout(0.3))

model.add(LSTM(256))
model.add(Dropout(0.3))

model.add(Dense(256, activation="relu"))
model.add(Dense(n_vocab, activation="softmax"))

model.compile(loss="categorical_crossentropy", optimizer="adam")

model.summary()

model.fit(
    network_input,
    network_output,
    epochs=20,
    batch_size=64
)

model.save("music_model.keras")

print("Model Training Completed!")
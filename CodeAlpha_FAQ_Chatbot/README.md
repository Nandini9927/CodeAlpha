#  AI Music Generator (LSTM + Python)
##  About the Project
AI Music Generator is a Python-based deep learning project that uses an LSTM neural network to generate original MIDI music.
It learns patterns from musical sequences and generates new compositions automatically. The project also includes a Tkinter GUI for easy interaction.
Users can:
-  Select different instruments
-  Adjust creativity (temperature)
-  Generate AI-composed music in real time

##  Features
-  AI-generated MIDI music using LSTM model
-  Multiple instrument support (Piano, Guitar, Violin, Flute, Trumpet)
-  Temperature control for creativity tuning
-  Simple and interactive Tkinter GUI
-  Fast music generation 
-  Output saved as playable MIDI file

##  Tech Stack
- Python 
- TensorFlow / Keras 
- Music21 
- NumPy 
- Tkinter 

##  How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run GUI
python gui.py
🎵 Output
After generation, music is saved as:
generated_music.mid
You can open it in any MIDI player or DAW software.

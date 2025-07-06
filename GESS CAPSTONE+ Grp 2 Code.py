''' NOISE DETECTOR PROGRAM FOR GRP 2 CAPSTONE+
Annotations may not be the most in detailed.'''

# Import necessary modules
import pyaudio  # for audio input/output
import numpy as np  # for numerical operations
import matplotlib.pyplot as plt  # for plotting
import time  # for time-related functions
from IPython.display import display, clear_output  # for interactive output

# Define constants

# Prompt for classroom name, noise threshold and length of time to add points
CLASS = str(input("What classroom is this laptop in right now?"))
THRESHOLD = int(input("What should be the unacceptable noise level? Default is 70"))
countermax = int(input("What should the amount of time for counter needed to add 1 to the point be?"))

# Other constants
CHUNK = 1024  # Number of audio samples per chunk
RATE = 44100  # Sampling rate in Hz
FORMAT = pyaudio.paInt16  # Format of audio data (16-bit PCM)
CHANNELS = 1  # Number of audio channels (mono)
MAX_TIME = int(input("How long will there be no teacher for?")) * 1000000000  # Maximum recording time in nanoseconds

# Variables for tracking noise score
score = 0
counter = 0
title = "Decibel level, score:"

# Create PyAudio object
audio = pyaudio.PyAudio()

# Create audio stream object
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

# Create figure and axis objects for plotting
fig = plt.figure()
plt.ion()  # Enable interactive mode
ax = fig.add_subplot(1, 1, 1)

# Initialize time-related variables
start_time = time.time_ns()
current_time = 0

# Variables for plotting
x = px = 0
recording = False

# Open an output text file
f = open('output.txt', 'wt')
output = "Class:" + CLASS + "\n"
f.write(output)

# Main loop
while current_time < MAX_TIME:
    # Read audio data from the stream
    data = stream.read(CHUNK)

    # Convert audio data to a numpy array
    data = np.frombuffer(data, np.int16)

    # Calculate decibel level from RMS value
    rms = np.linalg.norm(data) / np.sqrt(CHUNK)
    db = 20 * np.log10(rms)
    px = x
    x = current_time % (60 * 1000000000)

    # Plot decibel level on the graph
    ax.set_title(title)
    ax.set_xlabel("Time")
    ax.set_ylabel("dB")
    ax.plot(db)
    ax.set_xlim(0, 60 * 1000000000)
    ax.set_ylim(0, 100)

    if x < px:
        ax.cla()
    ax.plot(x, db, marker="o")
    clear_output(wait=True)
    plt.pause(0.01)

    # Check if the decibel level exceeds the threshold
    if db > THRESHOLD:
        fig.patch.set_facecolor('red')
        counter = counter + 1

    else:
        fig.patch.set_facecolor('green')
        recording = False
        counter = 0

    if counter == countermax:
        counter = 0
        score = score + 1
        output = time.ctime() + ": " + str(score) + "\n"
        f.write(output)
        title = "Decibel level, score: {0}".format(score)

    current_time = (time.time_ns()) - start_time

# Close audio stream and audio objects
stream.stop_stream()
stream.close()
audio.terminate()

# Close the figure
plt.close(fig)

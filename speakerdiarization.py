# -*- coding: utf-8 -*-
"""SpeakerDiarization.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1zBak9-XFQrczOFZdwxpZ1OQU_qU_kUdh
"""

!pip install resemblyzer

from resemblyzer import VoiceEncoder, preprocess_wav
from pathlib import Path
import numpy as np

fpath = Path("/content/99500-2-0-2.wav")
wav = preprocess_wav(fpath)

encoder = VoiceEncoder()
embed = encoder.embed_utterance(wav)
np.set_printoptions(precision=3, suppress=True)
print(embed)

!pip install pydub

from pydub import AudioSegment

# Replace 'input.mp3' with the path to your MP3 file
# Replace 'output.wav' with the desired path for the WAV file
sound = AudioSegment.from_mp3("/content/audio_data_donald_trump_fake_1bB5db0Srrw.mp3")
sound.export("/content/audio_data_donald_trump_fake_1bB5db0Srrw.wav", format="wav")

sound = AudioSegment.from_mp3("/content/audio_data_donald_trump_real_9BkOf5LQQBQ.mp3")
sound.export("/content/audio_data_donald_trump_real_9BkOf5LQQBQ.wav", format="wav")

from resemblyzer import VoiceEncoder, preprocess_wav
from pathlib import Path
import numpy as np

fpath = Path("/content/audio_data_donald_trump_fake_1bB5db0Srrw.wav")
wav = preprocess_wav(fpath)

encoder = VoiceEncoder()
embed_fake = encoder.embed_utterance(wav)
np.set_printoptions(precision=3, suppress=True)
print(embed_fake)

from resemblyzer import VoiceEncoder, preprocess_wav
from pathlib import Path
import numpy as np

fpath = Path("/content/audio_data_donald_trump_real_9BkOf5LQQBQ.wav")
wav = preprocess_wav(fpath)

encoder = VoiceEncoder()
embed_real = encoder.embed_utterance(wav)
np.set_printoptions(precision=3, suppress=True)
print(embed_real)

type(embed_fake)

def cosine_similarity(a, b):
       return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

similarity = cosine_similarity(embed_fake, embed_real)
print(similarity)

sound = AudioSegment.from_mp3("/content/audio_data_donald_trump_real_4glfwiMXgwQ.mp3")
sound.export("/content/audio_data_donald_trump_real_4glfwiMXgwQ.wav", format="wav")

from resemblyzer import VoiceEncoder, preprocess_wav
from pathlib import Path
import numpy as np

fpath = Path("/content/audio_data_donald_trump_real_4glfwiMXgwQ.wav")
wav = preprocess_wav(fpath)

encoder = VoiceEncoder()
embed_real1 = encoder.embed_utterance(wav)
np.set_printoptions(precision=3, suppress=True)
print(embed_real)

similarity = cosine_similarity(embed_real1, embed_real)
print(similarity)

!git clone https://github.com/resemble-ai/Resemblyzer

!python /content/Resemblyzer/demo05_fake_speech_detection.py

# Commented out IPython magic to ensure Python compatibility.
# %cd Resemblyzer

!pip install -r /content/Resemblyzer/requirements_package.txt

!pip install -r /content/Resemblyzer/requirements_demos.txt

from resemblyzer import preprocess_wav, VoiceEncoder
from demo_utils import *
from pathlib import Path
from tqdm import tqdm
import numpy as np


# DEMO 05: In this demo we'll show how we can achieve a modest form of fake speech detection with
# Resemblyzer. This method assumes you have some reference audio for the target speaker that you
# know is real, so it is not a universal fake speech detector on its own.
# In the audio data directory we have 18 segments of Donald Trump. 12 are real and extracted from
# actual speeches, while the remaining 6 others are fake and generated by various users on
# youtube, with a high discrepancy of voice cloning quality and naturalness achieved. We will
# take 6 segments of real speech as ground truth reference and compare those against the 12
# remaining. Those segments are selected at random, so will run into different results every time
# you run the script, but they should be more or less consistent.
# Using the voice of Donald Trump is merely a matter of convenience, as several fake speeches
# with his voice were already put up on youtube. This choice was not politically motivated.


## Load and preprocess the audio
data_dir = Path("audio_data", "donald_trump")
wav_fpaths = list(data_dir.glob("**/*.mp3"))
wavs = [preprocess_wav(wav_fpath) for wav_fpath in \
        tqdm(wav_fpaths, "Preprocessing wavs", len(wav_fpaths), unit=" utterances")]


## Compute the embeddings
encoder = VoiceEncoder()
embeds = np.array([encoder.embed_utterance(wav) for wav in wavs])
speakers = np.array([fpath.parent.name for fpath in wav_fpaths])
names = np.array([fpath.stem for fpath in wav_fpaths])


# Take 6 real embeddings at random, and leave the 6 others for testing
gt_indices = np.random.choice(*np.where(speakers == "real"), 6, replace=False)
mask = np.zeros(len(embeds), dtype=bool)
mask[gt_indices] = True
gt_embeds = embeds[mask]
gt_names = names[mask]
gt_speakers = speakers[mask]
embeds, speakers, names = embeds[~mask], speakers[~mask], names[~mask]


## Compare all embeddings against the ground truth embeddings, and compute the average similarities.
scores = (gt_embeds @ embeds.T).mean(axis=0)

# Order the scores by decreasing order
sort = np.argsort(scores)[::-1]
scores, names, speakers = scores[sort], names[sort], speakers[sort]


## Plot the scores
fig, _ = plt.subplots(figsize=(6, 6))
indices = np.arange(len(scores))
plt.axhline(0.84, ls="dashed", label="Prediction threshold", c="black")
plt.bar(indices[speakers == "real"], scores[speakers == "real"], color="green", label="Real")
plt.bar(indices[speakers == "fake"], scores[speakers == "fake"], color="red", label="Fake")
plt.legend()
plt.xticks(indices, names, rotation="vertical", fontsize=8)
plt.xlabel("Youtube video IDs")
plt.ylim(0.7, 1)
plt.ylabel("Similarity to ground truth")
fig.subplots_adjust(bottom=0.25)
plt.show()


## Real Time Speaker Diarization
- This system is built on top of the [Pyannote Audio](https://github.com/pyannote/pyannote-audio) and [Diart](https://github.com/juanmc2005/diart) Systems.
- Speaker Diarization detect the speakers and label them in an audio.
- Real-time when the diarization is performed on a streaming data with minimal latency
- Solvec 'who spoke when' problem in Speech to Text Transcription aka ASR
- Applications: Call centres, Meetings, Doctor-patient, Human-robot conversation, etc.,

## Steps for inference
### 1. Clone the repository
```
git clone https://github.com/BNarayanaReddy/RealTimeSpeakerDiarization.git 
```
### 2. Change the directory
```
cd RealTimeSpeakerDiarization
```
### 3. Run the script
```
chmod +x run.sh
./run.sh
```
### 4. Change the trained/pre-trained model checkpoint mode
- Alter the line 27 in >main.py with the checkpoint model path
### 5. Run the real-time speaker diarization system
```
python3 main.py
```

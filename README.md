## Real Time Speaker Diarization
- This system is built on top of the [Pyannote Audio](https://github.com/pyannote/pyannote-audio) and [Diart](https://github.com/juanmc2005/diart) Systems.
- Speaker Diarization detects the speakers and label them in an audio.
- Real-time when the diarization is performed on a streaming data with minimal latency
- Solvec 'who spoke when' problem in Speech to Text Transcription aka ASR
- Applications: Call centres, Meetings, Doctor-patient, Human-robot conversation, etc.,

- Trained model can be found here: [SSeRiouSS_MFCC.ckpt](https://drive.google.com/file/d/1-TY2mgWJL77jRZyerYNMrRbLn2Dsw3Ae/view?usp=drive_link)

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

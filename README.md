# Real-Time and Offline Speaker Diarization Through Robust Feature Fusion

[![Hugging Face model](https://img.shields.io/badge/Hugging_Face-Model-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/BNarayanaReddy/wavlm-mfcc-speaker-segmentation)
[![Paper: CICN 2025](https://img.shields.io/badge/Paper-CICN_2025-00629B?style=for-the-badge)](https://doi.org/10.1109/CICN67655.2025.11368116)
[![Checkpoint license: CC BY 4.0](https://img.shields.io/badge/Checkpoint_License-CC_BY_4.0-22A7F0?style=for-the-badge)](https://creativecommons.org/licenses/by/4.0/)

Up to **20.7% relative DER improvement over baseline** on AMI Headset-Mix: offline DER falls from **25.90% to 20.55%** with fine-tuned WavLM + MFCC feature fusion.

This repo contains the code and checkpoints for our CICN 2025 paper, "Real-Time and Offline Speaker Diarization Through Robust Feature Fusion". We combine acoustic and self-supervised features for speaker segmentation in the [Pyannote-Audio offline](https://www.isca-archive.org/interspeech_2023/bredin23_interspeech.html) and [Diart online](https://arxiv.org/abs/2109.06483) diarization pipelines to answer "who spoke when".

[Paper / DOI](https://doi.org/10.1109/CICN67655.2025.11368116) | [Hugging Face model](https://huggingface.co/BNarayanaReddy/wavlm-mfcc-speaker-segmentation)

## Approach

**Baseline:** the [Pyannote speaker segmentation model](https://arxiv.org/abs/2104.04045), trained on AMI Headset-Mix and Vox Converse, is our baseline. The 25.90% offline DER is for this trained baseline within the offline diarization pipeline, not an unspecified off-the-shelf model. The Diart rows in the online table are a separate pipeline comparison.

Our proposed segmentation model concatenates self-supervised speech representations and MFCCs before the Bi-LSTM and classification networks (early fusion). We use WavLM-Base and Wav2Vec2-Base feature extractors and 60-dimensional MFCC features. We also study an ECAPA-TDNN Based variant that reuses frame-level features from the embedding extractor rather than loading a dedicated segmentation feature extractor.

The multi-stage pipelines combine speaker segmentation, embedding extraction, and clustering. Pyannote-Audio uses global agglomerative clustering offline; Diart uses incremental clustering online. We perform local segmentation over a 5-second window every 0.5 seconds, predicting frame-wise activity for up to three speakers with sigmoid outputs to handle overlap. These local speaker slots are not a three-speaker limit for the full recording.

## Results

DER is diarization error rate; lower is better. We evaluate on AMI Headset-Mix with strict scoring and no forgiveness collar. These are our reported pipeline results, not a new evaluation of this release or a standalone segmentation metric.

### Offline: AMI Headset-Mix test set

| System | False alarm (%) | Missed speech (%) | Speaker confusion (%) | DER (%) |
| --- | ---: | ---: | ---: | ---: |
| Baseline | 7.39 | 9.15 | 9.35 | 25.90 |
| MFCCs | 7.00 | 10.30 | 9.69 | 26.99 |
| Wav2Vec2-Base | 7.07 | 6.57 | 11.68 | 25.34 |
| WavLM-Base | 5.84 | 7.53 | 10.42 | 23.79 |
| Wav2Vec2-Base, MFCC | 5.00 | 9.06 | 9.08 | 23.14 |
| WavLM-Base, MFCC | 6.04 | 7.32 | 9.15 | 22.52 |
| WavLM, Wav2Vec2 | 6.06 | 7.25 | 10.57 | 23.88 |
| WavLM, Wav2Vec2, MFCC | 6.53 | 6.50 | 10.61 | 23.64 |
| WavLM (Finetuned), MFCC | 4.91 | 6.75 | 8.88 | **20.55** |
| ECAPA-TDNN Based | 6.38 | 8.63 | 8.43 | 23.45 |

Source: complete Table I. Comma-separated extractors represent early feature fusion. Relative DER reduction is `(baseline DER - system DER) / baseline DER`: 13.1% for WavLM-Base + MFCC and 20.7% for fine-tuned WavLM + MFCC. The 20.7% result belongs to the offline pipeline, not every streaming configuration. Rounded table components may not sum exactly to the reported DER.

### Real-time: AMI Headset-Mix, Diart pipeline

| System | Latency | False alarm (%) | Missed speech (%) | Speaker confusion (%) | DER (%) |
| --- | --- | ---: | ---: | ---: | ---: |
| [Diart](https://arxiv.org/abs/2109.06483) | 0.5 s | 8.10 | 10.20 | 15.80 | 34.10 |
| [Diart](https://arxiv.org/abs/2109.06483) | 5 s | 5.00 | 10.00 | 12.40 | 27.50 |
| [SSPaValDo](https://arxiv.org/abs/2402.00067) | 5 s | 1.8 | 18.4 | 7.0 | 27.2 |
| −WavLM, MFCC | 0.5 s | 6.93 | 9.12 | 17.25 | 33.30 |
| −WavLM, MFCC | 5 s | 3.62 | 12.90 | 7.69 | **24.20** |
| −* WavLM, MFCC | 0.5 s | 5.96 | 11.31 | 12.12 | **29.39** |
| −* WavLM, MFCC | 5 s | 2.81 | 12.55 | 9.36 | 24.70 |

Source: complete Table II, using its system names. `−` denotes a fine-tuned feature extractor; `*` denotes tuned hyperparameters. The online pipeline parameters are `tau-active` (speech/non-speech threshold), `rho-update` (cluster-centroid update threshold), and `delta-new` (new-speaker threshold). The best configuration differs by latency.

## Checkpoints

These are segmentation models, not complete diarization pipelines. Speaker embedding extraction and clustering are also needed. Download the matching checkpoint rather than choosing by the validation metric embedded in its filename.

| Configuration | Exact checkpoint filename / download | File size | Paper system DER (%) |
| --- | --- | ---: | ---: |
| Baseline (trained Pyannote segmentation model) | [`Baseline_segmentation SincNet based=49.ckpt`](https://drive.google.com/file/d/1cbrFz_H9Z0WD06ys7UhARYW4zuzmw7yn/view) | 8.2 MB | 25.90 |
| WavLM-Base | [`WavLM--epoch=10.ckpt`](https://drive.google.com/file/d/1l4BAjrOTPkUO1Ovt9agnB33zeVqVoRZy/view) | 403.5 MB | 23.79 |
| ECAPA-TDNN frame-level features | [`Ecapa_tdnn_frameLevelFeatures--epoch=24-DiarizationErrorRate=0.155420.ckpt`](https://drive.google.com/file/d/1-VIhTHuAaqO94qh94c-rWurasPk1FptU/view) | 133.6 MB | 23.45 |
| Fine-tuned WavLM + MFCC | [`WavLM+MFCC_fintunedwavlm--epoch=25-DiarizationErrorRate=0.118334.ckpt`](https://drive.google.com/file/d/1-TY2mgWJL77jRZyerYNMrRbLn2Dsw3Ae/view) | 1.16 GB | **20.55** |
| WavLM + Wav2Vec2 + MFCC | [`Wav2Vec_base+WavLLM+MFCC--epoch=28-DiarizationErrorRate=0.135178.ckpt`](https://drive.google.com/file/d/1-RlDV_4I_0CEuYYQOvTO12gZxSBlCCwS/view) | 791.4 MB | 23.64 |
| WavLM + Wav2Vec2 | [`Wav2Vec_base+WavLM_base--epoch=38-DiarizationErrorRate=0.135567.ckpt`](https://drive.google.com/file/d/1-EVLIdz40diB57Tg5VGHdpREwQuHK5RR/view) | 790.5 MB | 23.88 |
| WavLM-Base + MFCC | [`WavLM_base+MFCC--epoch=62-DiarizationErrorRate=0.136872.ckpt`](https://drive.google.com/file/d/1-8m1i8_ebgWD-bDuFGcKpQxaUXpdo4h6/view) | 404.4 MB | 22.52 |
| Wav2Vec2-Base + MFCC | [`Wav2Vec_base+MFCC--epoch=37-DiarizationErrorRate=0.154341.ckpt`](https://drive.google.com/file/d/1-8knXepR-iMEg2WGpaz1pSBKJ4qgWRqH/view) | 404.3 MB | 23.14 |
| Wav2Vec2-Base | [`Wav2Vec_base--epoch=61-DiarizationErrorRate=0.144130.ckpt`](https://drive.google.com/file/d/1DylOR3fummM0lQoeTzlpmYLdtVTUP6Za/view) | 403.5 MB | 25.34 |

Only checkpoint variants corresponding to systems reported in Table I are listed. DER values are our reported results for each system, not a new evaluation of these downloadable files. Our MFCCs system is included in the results table above; a corresponding MFCC-only checkpoint is not included in this checkpoint collection.

**Recommended checkpoint:** fine-tuned WavLM + MFCC, epoch 25, the best offline configuration at 20.55% DER. The [Hugging Face repository](https://huggingface.co/BNarayanaReddy/wavlm-mfcc-speaker-segmentation) is dedicated to this checkpoint; its weights upload is pending. The other eight remain listed as Drive downloads. The current custom implementation targets WavLM + MFCC, so the other architectures may need their matching implementation before loading.

The checkpoint previously labeled `SSeRiouSS_MFCC.ckpt` in this README is the fine-tuned WavLM + MFCC epoch-25 checkpoint above. It is not a separate model. Its filename's `DiarizationErrorRate=0.118334` is not the paper's offline test DER.

In the current code, `SSeRiouSSWithMFCC.py` implements the WavLM + MFCC segmentation architecture. The code sets 16 kHz mono input and includes MFCC frame alignment specific to 5 s chunks. These implementation details are checked against the repository, not presented as extra paper claims.

## Setup and streaming inference

Use an isolated Python environment. The current code pins Diart to `0.9.2`; a fully tested lockfile is not included.

```bash
git clone https://github.com/BNarayanaReddy/RealTimeSpeakerDiarization.git
cd RealTimeSpeakerDiarization
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install python-dotenv huggingface_hub
```

On Debian/Ubuntu, the audio libraries used by the setup script are:

```bash
sudo apt-get update
sudo apt-get install -y libportaudio2 libasound-dev
```

### Install the custom segmentation implementation

Read `run.sh` before running it. It installs dependencies and replaces the installed file `pyannote/audio/models/segmentation/SSeRiouSS.py` with `SSeRiouSSWithMFCC.py`, retaining a `.bak` copy. Run it only inside the isolated environment:

```bash
chmod +x run.sh
./run.sh
```

This is a package patch, not a normal plugin installation. It can affect other uses of pyannote.audio in that environment.

### Configure the checkpoint and access

1. Download the fine-tuned WavLM + MFCC epoch-25 checkpoint.
2. Replace the machine-specific `model_path` in `main.py` with its local path.
3. Set `HF_API_KEY` in your shell for any Hugging Face dependencies that require authentication. Keep the token out of code and version control. The script reads the environment variable; it does not load a `.env` file automatically.
4. Check any access conditions for the pipeline's pretrained dependencies.

### Run

```bash
python3 main.py
```

The current entry point uses the microphone, plots streaming output, and writes RTTM speaker timestamps. It sets `step=0.5`, `latency=1`, and the original Diart thresholds. This 1 s demo is not either of the 0.5 s / 5 s paper configurations.

For file input, replace `MicrophoneAudioSource()` with `FileAudioSource(audio_path, sample_rate=16000)` using the example already in `main.py`.

To explore latency settings, change `latency` in `SpeakerDiarizationConfig`. Do not assume that changing latency alone reproduces Table II: checkpoint selection, thresholds, dataset preparation, and scoring must also match.

## Included code

We provide the custom segmentation model and streaming inference entry point. The full training and offline evaluation scripts are not included.

## Data and training

- Training used AMI Headset-Mix and Vox Converse, following the AMI-Diarization-setup protocol cited in the paper. The Vox Converse development set was split alphabetically: `abjxc` through `qouur` for training, with remaining files for validation.
- We report 37 hours of training data and extraction of 10 minutes of audio from each AMI WAV file. Evaluation used the AMI Headset-Mix test set.
- The baseline was trained for 100 epochs with Adam, early stopping, and dropout. The proposed models used a similar training setup.
- Fine-tuning used `1e-5` for the pretrained WavLM-Base model and `1e-3` for the rest of the network. Both used cosine annealing learning-rate schedulers.
- All models were trained on an NVIDIA RTX 3060 with 12 GB memory.

These summarize our experimental setup in Section IV; they are not a replacement for the missing training and evaluation scripts.

## Citation

```bibtex
@inproceedings{basireddy2025featurefusion,
  author = {Basireddy, L. N. R. and Rafi, BSM and Shireesha, G. Lakshmi},
  title = {Real-Time and Offline Speaker Diarization Through Robust Feature Fusion},
  booktitle = {2025 IEEE 17th International Conference on Computational Intelligence and Communication Networks (CICN)},
  year = {2025},
  pages = {2067--2071},
  doi = {10.1109/CICN67655.2025.11368116}
}
```

## Use and limitations

The models were evaluated on meeting audio. Performance on other languages, devices, noise levels, and speaker populations is not established by these results. Speaker labels are local labels, not verified identities. Use recordings only with appropriate consent and protect sensitive audio and transcripts.

## License

The released checkpoint is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Attribution is required. This checkpoint license does not assign a license to the repository code. Upstream models, libraries, and datasets retain their own terms; this license does not replace them.

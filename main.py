from huggingface_hub import login
from diart import SpeakerDiarization, SpeakerDiarizationConfig
from diart.sources import FileAudioSource, MicrophoneAudioSource
from diart.inference import StreamingInference
from diart.sinks import RTTMWriter
from pyannote.audio import Model
from diart.models import SegmentationModel
import dotenv
import os

hf_api = os.getenv("HF_API_KEY")
login(token=hf_api) # HF API token

# performed by Diart Org. for AMI corpus dataset
"""
tau-active  0.507 Speech vs Non-speech threshold
rho-update  0.006 Cluster centroid update threshold
delta-new  1.057  New speaker threshold

"""
# we performed hyper-params search for 12 hrs on AMI corpus dev dataset
"""

tau-active  0.5561998131
rho-update  0.9076818287
delta-new  0.7786825928

"""

# Model path to be pasted here
model_path = "/home/narayana/ML/spkr_diarize/architectural_expts/trained_models/wavlm_mfcc_fusion_finetuned_lr/epoch=25-DiarizationErrorRate=0.118334.ckpt"

# model loading
def seg_modelLoader():
    model = Model.from_pretrained(checkpoint=model_path)
    return model

seg_model = SegmentationModel(seg_modelLoader)


our_h_params1 = {"tau_active": 0.556,"rho_update":0.908,"delta_new" :0.779}
our_h_params2 = {"tau_active": 0.507,"rho_update":0.006,"delta_new" :0.75}

diart_h_params = {"tau_active": 0.507,"rho_update":0.006,"delta_new" :1.057}

config = SpeakerDiarizationConfig(
    segmentation=seg_model,
    step=0.5,
    latency=1, # between 0.5 to 5 seconds
    **diart_h_params
    # **our_h_params1
    # **our_h_params2

)
pipeline = SpeakerDiarization(config)

# audio_path = "/content/abjxc.wav"
# src = FileAudioSource(audio_path, sample_rate=16000) 

src = MicrophoneAudioSource() # Uncomment this line for streaming the data getting stream from mic
inference = StreamingInference(pipeline, src, do_plot=True) # True if for realt-time plotting (colab do not support this)
inference.attach_observers(RTTMWriter(src.uri, f"{src.uri}.rttm"))

prediction = inference()

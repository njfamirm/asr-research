import nemo.collections.asr as nemo_asr

# 1. Download and instantiate the Persian model
asr_model_name="nvidia/stt_fa_fastconformer_hybrid_large"
asr_model = nemo_asr.models.EncDecHybridRNNTCTCBPEModel.from_pretrained(model_name=asr_model_name)

audio_file_path = "voice_01.wav"
asr_model.transcribe([audio_file_path])

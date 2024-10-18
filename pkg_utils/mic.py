from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer, AudioConfig

speech_config = SpeechConfig(subscription="YOUR_SUBSCRIPTION_KEY", region="YOUR_REGION")
audio_config = AudioConfig(use_default_microphone=True)

try:
    recognizer = SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    print("SpeechRecognizer initialized successfully.")
except Exception as e:
    print(f"Failed to initialize SpeechRecognizer: {e}")
import pyaudio
import wave
import webrtcvad  # For voice activity detection
import boto3  # For AWS interaction
from botocore.exceptions import ClientError

# Configure AWS
rekognition = boto3.client('rekognition')

# Audio settings
CHUNK = 1024  # Size of each audio chunk
FORMAT = pyaudio.paInt16  # Audio format
CHANNELS = 1  # Single channel
RATE = 16000  # Sampling rate

# VAD settings
vad = webrtcvad.Vad()
aggressiveness = 3  # Adjust for noise level


def detect_sound(audio_data):
    """
    Uses Amazon Rekognition to detect a specific sound in an audio chunk.
    """
    try:
        response = rekognition.detect_custom_labels(
            Image={'Bytes': audio_data},
            ProjectVersionArn='your_rekognition_custom_model_arn'  # Replace with your custom model ARN
        )
        if 'CustomLabels' in response and len(response['CustomLabels']) > 0:
            return True
        else:
            return False
    except ClientError as e:
        print(f"Error with Rekognition: {e}")
        return False


def listen_and_count_sounds():
    """
    Listens for audio input, detects specific sounds using VAD and Rekognition, and counts occurrences.
    """
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    sound_count = 0

    while True:
        data = stream.read(CHUNK)
        is_speech = vad.is_speech(data, RATE, aggressiveness)

        if is_speech:
            if detect_sound(data):
                sound_count += 1
                print(f"Sound detected! Count: {sound_count}")

        # Add logic to exit listening loop (e.g., press a key)

    stream.stop_stream()
    stream.close()
    p.terminate()


if __name__ == "__main__":
    listen_and_count_sounds()
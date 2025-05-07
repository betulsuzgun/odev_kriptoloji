import wave
import numpy as np
import struct

def embed_message_in_audio(input_audio_path, output_audio_path, message):
    # Ses dosyasını aç
    with wave.open(input_audio_path, 'rb') as wav:
        params = wav.getparams()
        num_frames = params.nframes
        sample_rate = params.framerate
        num_channels = params.nchannels
        
        audio_data = wav.readframes(num_frames)
        audio_samples = np.frombuffer(audio_data, dtype=np.int16)

    # Mesajı ikili hale getir
    message_bin = ''.join(format(ord(c), '08b') for c in message)
    message_len = len(message_bin)

    # Audio üzerinde mesajı yerleştir
    for i in range(message_len):
        audio_samples[i] = (audio_samples[i] & 0xFFFE) | int(message_bin[i])

    # Gürültü filtreleme (basit bir örnek, daha gelişmiş filtreleme yapılabilir)
    audio_samples = np.clip(audio_samples, -32768, 32767)

    # Yeni ses dosyasını kaydet
    with wave.open(output_audio_path, 'wb') as wav:
        wav.setparams(params)
        wav.writeframes(audio_samples.tobytes())
    
    print("Mesaj başarıyla ses dosyasına yerleştirildi ve filtre uygulandı!")

# Kullanım örneği
embed_message_in_audio('input.wav', 'stego_audio.wav', 'Bu ses dosyasına gizli mesaj yerleştirildi!')

import numpy as np
import wave

def extract_message(stego_audio):
    with wave.open(stego_audio, 'rb') as wav:
        params = wav.getparams()
        frames = wav.readframes(params.nframes)
        samples = np.frombuffer(frames, dtype=np.int16)

    freq_data = np.fft.fft(samples)

    bits = ''
    for i in range(1, 1000):  # max 1000 bitlik alanı kontrol et
        phase = np.angle(freq_data[-(i+1)])
        bit = '0' if abs(phase) < np.pi/2 else '1'
        bits += bit

        if len(bits) % 8 == 0:
            chars = [chr(int(bits[j:j+8], 2)) for j in range(0, len(bits), 8)]
            msg = ''.join(chars)
            if "###" in msg:
                print("🔍 Çözülen Mesaj:", msg.split("###")[0])
                return

    print("❌ Mesaj bulunamadı.")

if __name__ == "__main__":
    extract_message("stego.wav")

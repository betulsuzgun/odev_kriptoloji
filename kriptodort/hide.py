import numpy as np
import wave

def message_to_bits(message):
    message += "###"  # Mesaj sonu işareti
    return ''.join(f"{ord(c):08b}" for c in message)

def embed_message(input_audio, output_audio, message):
    with wave.open(input_audio, 'rb') as wav:
        params = wav.getparams()
        frames = wav.readframes(params.nframes)
        samples = np.frombuffer(frames, dtype=np.int16)

    bits = message_to_bits(message)
    if len(bits) > len(samples) // 2:
        raise ValueError("Mesaj çok uzun!")

    # FFT (hızlı fourier dönüşümü)
    freq_data = np.fft.fft(samples)

    # Mesajı frekans bileşenlerinin fazlarına göm
    for i, bit in enumerate(bits):
        phase = np.angle(freq_data[-(i+2)])
        mag = np.abs(freq_data[-(i+2)])
        new_phase = 0 if bit == '0' else np.pi
        freq_data[-(i+2)] = mag * np.exp(1j * new_phase)

    # Geriye dönüştür (inverse FFT)
    modified_samples = np.fft.ifft(freq_data).real.astype(np.int16)

    with wave.open(output_audio, 'wb') as out:
        out.setparams(params)
        out.writeframes(modified_samples.tobytes())

    print("✅ Mesaj frekans bileşenlerine başarıyla gömüldü.")

if __name__ == "__main__":
    embed_message("input.wav", "stego.wav", "Frekanslara gizlenmiş mesaj")

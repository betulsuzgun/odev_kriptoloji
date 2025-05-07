import cv2
import numpy as np

def extract_message(stego_path):
    img = cv2.imread(stego_path, cv2.IMREAD_GRAYSCALE)
    h, w = img.shape
    bits = ""
    threshold = 0.3

    for bit_plane in range(7, -1, -1):
        plane = ((img >> bit_plane) & 1).astype(np.uint8)
        for i in range(0, h, 8):
            for j in range(0, w, 8):
                block = plane[i:i+8, j:j+8]
                if block.shape != (8, 8):
                    continue
                complexity = np.sum(block[:, :-1] != block[:, 1:]) + np.sum(block[:-1, :] != block[1:, :])
                total = 2 * block.shape[0] * (block.shape[1] - 1)
                if (complexity / total) >= threshold:
                    bits += ''.join(str(bit) for bit in block.flatten())

    message = ""
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8:
            break
        char = chr(int(byte, 2))
        message += char
        if message.endswith("###"):
            print("🔍 Çıkarılan Mesaj:", message[:-3])
            return

    print("⚠️ Mesaj sonu bulunamadı.")
    print("Tahmini mesaj:", message)

if __name__ == "__main__":
    extract_message("stego.png")
